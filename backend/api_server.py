"""
TMF921 Intent Translator - FastAPI Server
Supports both simulation mode and local LLM inference
"""

import os
import json
import logging
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from tmf921_translator_api import translate_intent, evaluate_system
from local_llm_engine import (
    LocalLLMEngine, LLMConfig, create_llm_engine,
    RECOMMENDED_MODELS, LLMProvider
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="TMF921 Intent Translator API",
    description="SOTA NL-to-TMF921 translation system with local LLM support",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global LLM engine (lazy initialization)
_llm_engine: Optional[LocalLLMEngine] = None

# ============== Request/Response Models ==============

class TranslateRequest(BaseModel):
    nl_intent: str = Field(..., description="Natural language intent to translate")
    use_local_llm: bool = Field(default=False, description="Use local LLM instead of simulation")
    llm_provider: Optional[str] = Field(default="ollama", description="LLM provider: ollama, llama_cpp, transformers")
    model_name: Optional[str] = Field(default="llama3", description="Model name to use")


class BatchTranslateRequest(BaseModel):
    nl_intents: List[str] = Field(..., description="List of NL intents to translate")
    use_local_llm: bool = Field(default=False)
    llm_provider: Optional[str] = Field(default="ollama")
    model_name: Optional[str] = Field(default="llama3")


class EvaluateRequest(BaseModel):
    dataset_size: int = Field(default=100, ge=10, le=1000)
    use_local_llm: bool = Field(default=False)


class LLMConfigRequest(BaseModel):
    provider: str = Field(default="ollama")
    model_name: str = Field(default="llama3")
    base_url: str = Field(default="http://localhost:11434")
    temperature: float = Field(default=0.1, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2048, ge=256, le=8192)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)


class TranslateResponse(BaseModel):
    id: str
    nl_intent: str
    nl_intent_normalized: str
    tmf921_mapping: dict
    tmf921_resource: dict
    intent_parameters: dict
    confidence: float
    translation_time_ms: float
    model_used: str
    provider: str
    simulation_mode: bool = False


class StatusResponse(BaseModel):
    status: str
    simulation_mode: bool
    llm_available: bool
    llm_provider: Optional[str]
    llm_model: Optional[str]
    gpu_available: bool
    gpu_name: Optional[str]
    gpu_memory_gb: Optional[float]


# ============== Helper Functions ==============

def get_llm_engine(config: Optional[LLMConfig] = None) -> LocalLLMEngine:
    """Get or create LLM engine singleton"""
    global _llm_engine
    if _llm_engine is None:
        _llm_engine = create_llm_engine(config)
    return _llm_engine


def check_gpu() -> dict:
    """Check GPU availability"""
    try:
        import torch
        if torch.cuda.is_available():
            return {
                "available": True,
                "name": torch.cuda.get_device_name(0),
                "memory_total_gb": torch.cuda.get_device_properties(0).total_memory / 1e9,
                "memory_allocated_gb": torch.cuda.memory_allocated(0) / 1e9,
            }
    except Exception as e:
        logger.warning(f"GPU check failed: {e}")

    return {"available": False, "name": None, "memory_total_gb": None}


# ============== API Endpoints ==============

@app.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "name": "TMF921 Intent Translator API",
        "version": "2.0.0",
        "description": "SOTA NL-to-TMF921 translation with local LLM support",
        "docs": "/docs"
    }


@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Get system status including LLM availability"""
    gpu_info = check_gpu()
    engine = get_llm_engine()

    return StatusResponse(
        status="online",
        simulation_mode=engine.provider == LLMProvider.SIMULATION,
        llm_available=engine.provider != LLMProvider.SIMULATION,
        llm_provider=engine.provider.value if engine.provider != LLMProvider.SIMULATION else None,
        llm_model=engine.config.model_name,
        gpu_available=gpu_info["available"],
        gpu_name=gpu_info.get("name"),
        gpu_memory_gb=gpu_info.get("memory_total_gb"),
    )


@app.post("/translate", response_model=TranslateResponse)
async def translate(
    request: TranslateRequest
):
    """Translate NL intent to TMF921 format"""
    try:
        if request.use_local_llm:
            # Use local LLM
            config = LLMConfig(
                provider=request.llm_provider or "ollama",
                model_name=request.model_name or "llama3",
            )
            engine = get_llm_engine(config)

            if engine.provider == LLMProvider.SIMULATION:
                raise HTTPException(
                    status_code=503,
                    detail="Local LLM not available. Please configure Ollama or install transformers."
                )

            result = engine.translate(request.nl_intent)
            return TranslateResponse(
                id=result.get("id", "llm-" + str(hash(request.nl_intent))),
                nl_intent=request.nl_intent,
                nl_intent_normalized=request.nl_intent.lower().strip(),
                tmf921_mapping={
                    "intent_type": result.get("intent_type", "Intent"),
                    "action": result.get("action", "POST"),
                    "expectation_type": result.get("expectation_type"),
                    "endpoint": result.get("endpoint", "/intent"),
                    "lifecycle_status": "Created",
                },
                tmf921_resource={},
                intent_parameters={},
                confidence=result.get("confidence", 0.9),
                translation_time_ms=result.get("inference_time_ms", 0),
                model_used=engine.config.model_name,
                provider=engine.provider.value,
                simulation_mode=False,
            )
        else:
            # Use simulation (rule-based)
            result = translate_intent(request.nl_intent)
            return TranslateResponse(
                simulation_mode=True,
                provider="simulation",
                **result
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Translation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/translate/batch")
async def translate_batch(request: BatchTranslateRequest):
    """Batch translate multiple NL intents"""
    results = []

    try:
        if request.use_local_llm:
            config = LLMConfig(
                provider=request.llm_provider or "ollama",
                model_name=request.model_name or "llama3",
            )
            engine = get_llm_engine(config)
            results = engine.batch_translate(request.nl_intents)
        else:
            for intent in request.nl_intents:
                result = translate_intent(intent)
                results.append(result)

        return {"results": results, "count": len(results)}

    except Exception as e:
        logger.error(f"Batch translation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/evaluate")
async def evaluate(request: EvaluateRequest):
    """Evaluate translation system"""
    try:
        metrics = evaluate_system(request.dataset_size)
        return metrics
    except Exception as e:
        logger.error(f"Evaluation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/llm/models")
async def get_llm_models():
    """Get recommended models for RTX 6000 ADA (50GB)"""
    gpu_info = check_gpu()
    memory_gb = gpu_info.get("memory_total_gb", 50)

    # Filter models by available VRAM
    recommendations = {}

    if memory_gb >= 40:
        # Can run 70B models
        recommendations["high_vram"] = {
            "memory": f"{memory_gb:.0f}GB available",
            "models": RECOMMENDED_MODELS["ollama"][1:3] + RECOMMENDED_MODELS["ollama"][3:4]
        }

    if memory_gb >= 8:
        # Can run 7B-8B models comfortably
        recommendations["medium_vram"] = {
            "memory": f"{memory_gb:.0f}GB available",
            "models": RECOMMENDED_MODELS["ollama"][:3] + [RECOMMENDED_MODELS["ollama"][4]]
        }

    if memory_gb >= 4:
        # Can run smaller models
        recommendations["low_vram"] = {
            "memory": f"{memory_gb:.0f}GB available",
            "models": [RECOMMENDED_MODELS["ollama"][4], RECOMMENDED_MODELS["ollama"][5]]
        }

    return {
        "gpu": gpu_info,
        "recommendations": recommendations,
        "setup_instructions": {
            "ollama": "1. Install: curl -fsSL https://ollama.ai/install.sh | sh\n2. Start: ollama serve\n3. Pull model: ollama pull llama3\n4. Or try: ollama pull mistral",
            "transformers": "1. Install: pip install transformers torch accelerate\n2. Ensure CUDA is available\n3. Model loads automatically to GPU",
        }
    }


@app.post("/llm/configure")
async def configure_llm(config: LLMConfigRequest):
    """Configure LLM settings"""
    global _llm_engine
    try:
        llm_config = LLMConfig(
            provider=config.provider,
            model_name=config.model_name,
            base_url=config.base_url,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            top_p=config.top_p,
        )

        _llm_engine = create_llm_engine(llm_config.__dict__)

        return {
            "status": "configured",
            "provider": _llm_engine.provider.value,
            "model": _llm_engine.config.model_name,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/llm/install/{model_name}")
async def install_model(model_name: str):
    """Install a model via Ollama"""
    global _llm_engine
    try:
        engine = get_llm_engine()
        if engine.provider != LLMProvider.OLLAMA:
            raise HTTPException(status_code=400, detail="Ollama not configured")

        success = engine.install_model(model_name)
        if success:
            return {"status": "installed", "model": model_name}
        else:
            raise HTTPException(status_code=500, detail="Installation failed")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============== Health Check ==============

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


# ============== Main ==============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

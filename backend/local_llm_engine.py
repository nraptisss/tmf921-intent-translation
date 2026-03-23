"""
TMF921 Intent Translator - Local LLM Engine
Supports Ollama, llama.cpp, and HuggingFace Transformers for local inference
"""

import json
import os
import re
import time
import logging
from typing import Optional, Dict, Any, List, Literal
from dataclasses import dataclass, field, asdict
from enum import Enum
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMProvider(Enum):
    """Supported LLM providers"""
    OLLAMA = "ollama"
    LLAMA_CPP = "llama_cpp"
    TRANSFORMERS = "transformers"
    SIMULATION = "simulation"  # Fallback to rule-based

@dataclass
class LLMConfig:
    """Configuration for local LLM"""
    provider: str = "simulation"
    model_name: str = "llama3"
    base_url: str = "http://localhost:11434"  # Ollama default
    temperature: float = 0.1
    max_tokens: int = 2048
    top_p: float = 0.9
    repeat_penalty: float = 1.1
    context_window: int = 8192
    gpu_layers: int = -1  # Use all available
    quantization: str = "q4_0"  # For llama.cpp

@dataclass
class LLMResponse:
    """Response from LLM"""
    text: str
    model: str
    provider: str
    tokens_used: int
    inference_time_ms: float
    finish_reason: str

class LocalLLMEngine:
    """
    Local LLM Engine for TMF921 Intent Translation
    Supports Ollama, llama.cpp, and HuggingFace Transformers
    """

    # TMF921 System Prompt for Intent Translation
    SYSTEM_PROMPT = """You are an expert TMF921 Intent Management translator for 5G/6G networks.

Your task is to translate Natural Language intents to TMF921 v5.0.0 format.

## TMF921 Intent Types:
1. **Intent** - Core intent resource for user expectations/requirements
2. **ProbeIntent** - For testing/probing intent feasibility
3. **IntentSpecification** - Template/specification for intents
4. **IntentReport** - Status/compliance reports

## HTTP Actions:
- **POST** - Create new intent
- **GET** - Query/retrieve intent
- **PATCH** - Update intent
- **DELETE** - Remove intent

## Expectation Types:
- **DeliveryExpectation** - Service delivery requirements
- **PropertyExpectation** - Property/characteristic requirements
- **ReportingExpectation** - Monitoring/reporting requirements

## 5G/6G Parameters:
- Latency: 5ms, 10ms, 12ms, 20ms, 50ms, 100ms
- Availability: 99.9%, 99.95%, 99.99%, 99.999%
- Throughput: 100Mbps, 500Mbps, 1Gbps, 10Gbps
- Service Types: NetworkSlice, VideoStreaming, IoTService, EdgeComputing, etc.

## Output Format:
Return a JSON object with:
- intent_type: The TMF921 intent type
- action: The HTTP action (POST/GET/PATCH/DELETE)
- expectation_type: The expectation type
- endpoint: The API endpoint
- service_type: The service type
- parameters: Key parameters extracted

Example input: "Create an intent to deliver 4K video streaming to 200 users in the stadium"

Respond ONLY with valid JSON, no markdown or explanation."""

    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig()
        self.provider = self._initialize_provider()
        self._test_connection()

    def _initialize_provider(self) -> LLMProvider:
        """Initialize the LLM provider based on config"""
        try:
            provider = LLMProvider(self.config.provider.lower())
        except ValueError:
            logger.warning(f"Unknown provider '{self.config.provider}', using simulation mode")
            provider = LLMProvider.SIMULATION

        if provider == LLMProvider.OLLAMA:
            return self._init_ollama()
        elif provider == LLMProvider.LLAMA_CPP:
            return self._init_llama_cpp()
        elif provider == LLMProvider.TRANSFORMERS:
            return self._init_transformers()
        else:
            return self._init_simulation()

    def _init_ollama(self):
        """Initialize Ollama client"""
        try:
            import ollama
            # Test connection
            try:
                ollama.list()
                logger.info(f"Ollama connected. Available models: {ollama.list()}")
            except Exception as e:
                logger.warning(f"Ollama not responding at {self.config.base_url}: {e}")

            self._client = ollama
            return LLMProvider.OLLAMA
        except ImportError:
            logger.warning("Ollama not installed. Install with: pip install ollama")
            return LLMProvider.SIMULATION

    def _init_llama_cpp(self):
        """Initialize llama.cpp (via ctransformers)"""
        try:
            from ctransformers import AutoModelForCausalLM
            logger.info(f"llama.cpp initialized for model: {self.config.model_name}")
            self._llm = None  # Lazy load
            return LLMProvider.LLAMA_CPP
        except ImportError:
            logger.warning("ctransformers not installed. Install with: pip install ctransformers")
            return LLMProvider.SIMULATION

    def _init_transformers(self):
        """Initialize HuggingFace Transformers with GPU"""
        try:
            import torch
            from transformers import AutoTokenizer, AutoModelForCausalLM

            if not torch.cuda.is_available():
                logger.warning("CUDA not available. Using CPU mode.")

            logger.info(f"Transformers initialized. CUDA available: {torch.cuda.is_available()}")
            if torch.cuda.is_available():
                logger.info(f"GPU: {torch.cuda.get_device_name(0)}")
                logger.info(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

            self._tokenizer = None  # Lazy load
            self._model = None  # Lazy load
            return LLMProvider.TRANSFORMERS
        except ImportError as e:
            logger.warning(f"Transformers not available: {e}")
            return LLMProvider.SIMULATION

    def _init_simulation(self):
        """Initialize simulation mode (rule-based fallback)"""
        logger.info("Using simulation mode (rule-based translation)")
        return LLMProvider.SIMULATION

    def _test_connection(self):
        """Test connection to LLM provider"""
        if self.provider == LLMProvider.OLLAMA:
            try:
                import ollama
                models = ollama.list()
                logger.info(f"Ollama connection successful. Models: {len(models.get('models', []))}")
            except Exception as e:
                logger.error(f"Ollama connection failed: {e}")

    def load_model(self):
        """Lazy load the model (call this before first inference)"""
        if self.provider == LLMProvider.LLAMA_CPP and self._llm is None:
            from ctransformers import AutoModelForCausalLM
            logger.info(f"Loading model: {self.config.model_name}")
            self._llm = AutoModelForCausalLM.from_pretrained(
                self.config.model_name,
                model_type="llama",
                gpu_layers=self.config.gpu_layers,
            )
            logger.info("Model loaded successfully")

        elif self.provider == LLMProvider.TRANSFORMERS and self._model is None:
            import torch
            from transformers import AutoTokenizer, AutoModelForCausalLM

            logger.info(f"Loading model: {self.config.model_name}")
            self._tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)

            # Load with GPU support
            self._model = AutoModelForCausalLM.from_pretrained(
                self.config.model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else "cpu",
                load_in_4bit=self.config.quantization == "q4_0",
            )
            logger.info("Model loaded successfully")

    def translate(self, nl_intent: str) -> Dict[str, Any]:
        """
        Translate NL intent to TMF921 format using LLM

        Args:
            nl_intent: Natural language intent string

        Returns:
            TMF921 translation dictionary
        """
        start_time = time.time()

        if self.provider == LLMProvider.OLLAMA:
            result = self._translate_ollama(nl_intent)
        elif self.provider == LLMProvider.LLAMA_CPP:
            result = self._translate_llama_cpp(nl_intent)
        elif self.provider == LLMProvider.TRANSFORMERS:
            result = self._translate_transformers(nl_intent)
        else:
            result = self._translate_simulation(nl_intent)

        inference_time = (time.time() - start_time) * 1000
        result['inference_time_ms'] = inference_time
        result['provider'] = self.provider.value
        result['model'] = self.config.model_name

        return result

    def _translate_ollama(self, nl_intent: str) -> Dict[str, Any]:
        """Translate using Ollama"""
        try:
            import ollama

            response = ollama.generate(
                model=self.config.model_name,
                prompt=f"{self.SYSTEM_PROMPT}\n\nInput: {nl_intent}\n\nOutput JSON:",
                options={
                    'temperature': self.config.temperature,
                    'num_predict': self.config.max_tokens,
                    'top_p': self.config.top_p,
                    'repeat_penalty': self.config.repeat_penalty,
                }
            )

            return self._parse_llm_response(response['response'])

        except Exception as e:
            logger.error(f"Ollama translation failed: {e}")
            return self._translate_simulation(nl_intent)

    def _translate_llama_cpp(self, nl_intent: str) -> Dict[str, Any]:
        """Translate using llama.cpp"""
        try:
            if self._llm is None:
                self.load_model()

            prompt = f"{self.SYSTEM_PROMPT}\n\nInput: {nl_intent}\n\nOutput JSON:"

            response = self._llm(
                prompt,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                repetition_penalty=self.config.repeat_penalty,
            )

            return self._parse_llm_response(response)

        except Exception as e:
            logger.error(f"llama.cpp translation failed: {e}")
            return self._translate_simulation(nl_intent)

    def _translate_transformers(self, nl_intent: str) -> Dict[str, Any]:
        """Translate using HuggingFace Transformers"""
        try:
            import torch

            if self._model is None:
                self.load_model()

            prompt = f"{self.SYSTEM_PROMPT}\n\nInput: {nl_intent}\n\nOutput JSON:"

            inputs = self._tokenizer(prompt, return_tensors="pt")
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}

            outputs = self._model.generate(
                **inputs,
                max_new_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                top_p=self.config.top_p,
                repetition_penalty=self.config.repeat_penalty,
                do_sample=True,
            )

            response = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Extract JSON from response
            response = response.split("Output JSON:")[-1].strip()

            return self._parse_llm_response(response)

        except Exception as e:
            logger.error(f"Transformers translation failed: {e}")
            return self._translate_simulation(nl_intent)

    def _translate_simulation(self, nl_intent: str) -> Dict[str, Any]:
        """Rule-based simulation fallback"""
        # Use the existing simulation logic
        from tmf921_translator_api import translate_intent
        result = translate_intent(nl_intent)
        return {
            'intent_type': result['tmf921_mapping']['intent_type'],
            'action': result['tmf921_mapping']['action'],
            'expectation_type': result['tmf921_mapping']['expectation_type'],
            'endpoint': result['tmf921_mapping']['endpoint'],
            'service_type': result['intent_parameters']['service_type'],
            'parameters': {
                'latency': result['intent_parameters']['latency'],
                'throughput': result['intent_parameters']['throughput'],
                'availability': result['intent_parameters']['availability'],
                'quality_level': result['intent_parameters']['quality_level'],
                'max_participants': result['intent_parameters']['max_participants'],
            },
            'confidence': result['confidence'],
            'simulation_mode': True,
        }

    def _parse_llm_response(self, response_text: str) -> Dict[str, Any]:
        """Parse LLM response to extract JSON"""
        # Clean up response - remove markdown code blocks if present
        response_text = response_text.strip()
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
        response_text = response_text.strip()

        # Try to find JSON object in response
        try:
            # Find first { and last }
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end > start:
                json_str = response_text[start:end]
                data = json.loads(json_str)
                return data
        except json.JSONDecodeError:
            pass

        # If parsing fails, use simulation as fallback
        logger.warning("LLM response parsing failed, using simulation fallback")
        return self._translate_simulation("")

    def batch_translate(self, intents: List[str]) -> List[Dict[str, Any]]:
        """Translate multiple intents"""
        results = []
        for intent in intents:
            result = self.translate(intent)
            results.append(result)
        return results

    def get_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available models based on provider"""
        models = []

        if self.provider == LLMProvider.OLLAMA:
            try:
                import ollama
                response = ollama.list()
                for model in response.get('models', []):
                    models.append({
                        'name': model.get('name', ''),
                        'size': model.get('size', 0),
                        'modified': model.get('modified_at', ''),
                    })
            except Exception as e:
                logger.error(f"Failed to list Ollama models: {e}")

        return models

    def install_model(self, model_name: str) -> bool:
        """Install a model (Ollama)"""
        if self.provider == LLMProvider.OLLAMA:
            try:
                import ollama
                logger.info(f"Installing model: {model_name}")
                ollama.pull(model_name)
                logger.info(f"Model {model_name} installed successfully")
                return True
            except Exception as e:
                logger.error(f"Failed to install model: {e}")
                return False
        return False


def create_llm_engine(config: Optional[Dict[str, Any]] = None) -> LocalLLMEngine:
    """Factory function to create LLM engine"""
    if config:
        llm_config = LLMConfig(**config)
    else:
        # Try to detect best available provider
        llm_config = LLMConfig()

        # Check for Ollama
        try:
            import ollama
            ollama.list()
            llm_config.provider = "ollama"
            return LocalLLMEngine(llm_config)
        except:
            pass

        # Check for CUDA
        try:
            import torch
            if torch.cuda.is_available():
                llm_config.provider = "transformers"
                return LocalLLMEngine(llm_config)
        except:
            pass

        # Fallback to simulation
        llm_config.provider = "simulation"

    return LocalLLMEngine(llm_config)


# Recommended models for RTX 6000 ADA (50GB VRAM)
RECOMMENDED_MODELS = {
    "ollama": [
        {"name": "llama3", "size": "4.7GB", "description": "Llama 3 8B - Fast and capable"},
        {"name": "llama3:70b", "size": "40GB", "description": "Llama 3 70B - Best quality"},
        {"name": "mistral", "size": "4.1GB", "description": "Mistral 7B - Excellent for tasks"},
        {"name": "mixtral", "size": "26GB", "description": "Mixtral 8x7B - Mixture of experts"},
        {"name": "phi3", "size": "2.3GB", "description": "Phi-3 Mini - Small and efficient"},
        {"name": "gemma:7b", "size": "4.8GB", "description": "Gemma 7B - Google's model"},
    ],
    "huggingface": [
        {"name": "meta-llama/Meta-Llama-3-8B-Instruct", "size": "~8GB", "description": "Llama 3 8B Instruct"},
        {"name": "meta-llama/Meta-Llama-3-70B-Instruct", "size": "~40GB", "description": "Llama 3 70B (needs VRAM)"},
        {"name": "mistralai/Mistral-7B-Instruct-v0.2", "size": "~7GB", "description": "Mistral 7B v0.2"},
        {"name": "mistralai/Mixtral-8x7B-Instruct-v0.1", "size": "~26GB", "description": "Mixtral 8x7B"},
        {"name": "microsoft/Phi-3-mini-128k-instruct", "size": "~7GB", "description": "Phi-3 Mini 128K"},
    ]
}


if __name__ == "__main__":
    # Test the LLM engine
    print("=" * 60)
    print("TMF921 Local LLM Engine Test")
    print("=" * 60)

    # Create engine
    engine = create_llm_engine()
    print(f"\nProvider: {engine.provider.value}")
    print(f"Model: {engine.config.model_name}")

    # Test translation
    test_intents = [
        "Create an intent to deliver 4K video streaming to 200 users",
        "Probe system for low latency connectivity capability",
        "Generate compliance report for network slice",
    ]

    print("\nTranslation Tests:")
    for intent in test_intents:
        print(f"\n[Input] {intent}")
        result = engine.translate(intent)
        print(f"[Output] Type: {result.get('intent_type', 'N/A')}, Action: {result.get('action', 'N/A')}")
        print(f"         Time: {result.get('inference_time_ms', 0):.0f}ms")

import React from 'react';
import { useTranslation } from '../contexts/TranslationContext';
import {
  Code,
  CheckCircle2,
  Copy,
  Download,
  Clock,
  Zap,
  ArrowRight,
  FileJson,
  Database,
  Activity
} from 'lucide-react';

export const OutputPanel: React.FC = () => {
  const { currentTranslation, isTranslating } = useTranslation();

  if (isTranslating) {
    return (
      <div className="h-full flex flex-col items-center justify-center bg-slate-800/50 backdrop-blur-sm">
        <div className="relative">
          <div className="absolute inset-0 bg-cyan-500/20 blur-3xl rounded-full"></div>
          <div className="relative">
            <div className="w-16 h-16 border-4 border-cyan-500/30 border-t-cyan-500 rounded-full animate-spin"></div>
          </div>
        </div>
        <div className="mt-6 text-center">
          <h3 className="text-lg font-medium text-slate-200">Processing with LLM...</h3>
          <p className="text-sm text-slate-400 mt-1">Analyzing intent semantics and mapping to TMF921</p>
        </div>
      </div>
    );
  }

  if (!currentTranslation) {
    return (
      <div className="h-full flex flex-col items-center justify-center bg-slate-800/50 backdrop-blur-sm border-l border-slate-700/50 p-8">
        <div className="relative mb-6">
          <div className="absolute inset-0 bg-cyan-500/10 blur-2xl rounded-full"></div>
          <div className="relative bg-slate-800/80 p-6 rounded-2xl border border-slate-700/50">
            <Code className="w-12 h-12 text-cyan-400/60" />
          </div>
        </div>
        <h3 className="text-xl font-medium text-slate-200 mb-2">No Translation Yet</h3>
        <p className="text-sm text-slate-400 text-center max-w-md">
          Enter a natural language intent and click translate to see the TMF921 representation
        </p>
        <div className="mt-8 grid grid-cols-2 gap-4 max-w-lg">
          <div className="flex items-center gap-2 text-sm text-slate-500">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <span>Intent Type Detection</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-slate-500">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <span>Action Classification</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-slate-500">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <span>Parameter Extraction</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-slate-500">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <span>JSON-LD Generation</span>
          </div>
        </div>
      </div>
    );
  }

  const { tmf921_mapping, tmf921_resource, intent_parameters, confidence, translation_time_ms, model_used } = currentTranslation;

  return (
    <div className="h-full flex flex-col bg-slate-800/50 backdrop-blur-sm border-l border-slate-700/50 overflow-hidden">
      <div className="p-4 border-b border-slate-700/50 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h2 className="text-lg font-semibold text-slate-100">TMF921 Translation Result</h2>
          <div className="flex items-center gap-1 px-2 py-0.5 bg-emerald-500/10 border border-emerald-500/20 rounded-full">
            <Zap className="w-3 h-3 text-emerald-400" />
            <span className="text-xs text-emerald-400 font-medium">{Math.round(confidence * 100)}%</span>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <button className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-700/50 rounded-lg transition-all">
            <Copy className="w-4 h-4" />
          </button>
          <button className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-700/50 rounded-lg transition-all">
            <Download className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {/* Original Intent */}
        <div className="bg-slate-900/50 border border-slate-700/50 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-2">
            <ArrowRight className="w-4 h-4 text-cyan-400" />
            <span className="text-sm font-medium text-slate-300">Original Natural Language Intent</span>
          </div>
          <p className="text-slate-200">{currentTranslation.nl_intent}</p>
        </div>

        {/* Mapping Summary */}
        <div className="grid grid-cols-3 gap-3">
          <div className="bg-slate-900/50 border border-slate-700/50 rounded-xl p-3">
            <div className="flex items-center gap-2 mb-1">
              <Database className="w-4 h-4 text-purple-400" />
              <span className="text-xs text-slate-400">Intent Type</span>
            </div>
            <p className="text-sm font-medium text-purple-400">{tmf921_mapping.intent_type}</p>
          </div>
          <div className="bg-slate-900/50 border border-slate-700/50 rounded-xl p-3">
            <div className="flex items-center gap-2 mb-1">
              <Activity className="w-4 h-4 text-cyan-400" />
              <span className="text-xs text-slate-400">Action</span>
            </div>
            <p className="text-sm font-medium text-cyan-400">{tmf921_mapping.action}</p>
          </div>
          <div className="bg-slate-900/50 border border-slate-700/50 rounded-xl p-3">
            <div className="flex items-center gap-2 mb-1">
              <FileJson className="w-4 h-4 text-amber-400" />
              <span className="text-xs text-slate-400">Endpoint</span>
            </div>
            <p className="text-sm font-medium text-amber-400">{tmf921_mapping.endpoint}</p>
          </div>
        </div>

        {/* Resource Details */}
        <div className="bg-slate-900/50 border border-slate-700/50 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-3">
            <Database className="w-4 h-4 text-cyan-400" />
            <span className="text-sm font-medium text-slate-300">TMF921 Resource Structure</span>
          </div>
          <div className="space-y-2 font-mono text-xs">
            <div className="flex items-start gap-2">
              <span className="text-slate-500 min-w-[100px]">id:</span>
              <span className="text-emerald-400">{tmf921_resource.id}</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-slate-500 min-w-[100px]">name:</span>
              <span className="text-blue-400">{tmf921_resource.name}</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-slate-500 min-w-[100px]">version:</span>
              <span className="text-purple-400">{tmf921_resource.version}</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-slate-500 min-w-[100px]">priority:</span>
              <span className="text-amber-400">{tmf921_resource.priority}</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-slate-500 min-w-[100px]">context:</span>
              <span className="text-cyan-400">{tmf921_resource.context}</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-slate-500 min-w-[100px]">isBundle:</span>
              <span className="text-pink-400">{tmf921_resource.isBundle.toString()}</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-slate-500 min-w-[100px]">lifestyleStatus:</span>
              <span className="text-emerald-400">{tmf921_resource.lifestyleStatus}</span>
            </div>
          </div>
        </div>

        {/* Intent Parameters */}
        <div className="bg-slate-900/50 border border-slate-700/50 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-3">
            <Activity className="w-4 h-4 text-cyan-400" />
            <span className="text-sm font-medium text-slate-300">Intent Parameters</span>
          </div>
          <div className="grid grid-cols-2 gap-3 text-xs">
            <div>
              <span className="text-slate-500">Service Type:</span>
              <span className="ml-2 text-slate-300">{intent_parameters.service_type}</span>
            </div>
            <div>
              <span className="text-slate-500">Quality Level:</span>
              <span className="ml-2 text-slate-300">{intent_parameters.quality_level}</span>
            </div>
            <div>
              <span className="text-slate-500">Latency:</span>
              <span className="ml-2 text-slate-300">{intent_parameters.latency}</span>
            </div>
            <div>
              <span className="text-slate-500">Throughput:</span>
              <span className="ml-2 text-slate-300">{intent_parameters.throughput}</span>
            </div>
            <div>
              <span className="text-slate-500">Availability:</span>
              <span className="ml-2 text-slate-300">{intent_parameters.availability}</span>
            </div>
            <div>
              <span className="text-slate-500">Max Participants:</span>
              <span className="ml-2 text-slate-300">{intent_parameters.max_participants}</span>
            </div>
          </div>
        </div>

        {/* JSON-LD Expression */}
        <div className="bg-slate-900/50 border border-slate-700/50 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-3">
            <Code className="w-4 h-4 text-cyan-400" />
            <span className="text-sm font-medium text-slate-300">JSON-LD Expression</span>
          </div>
          <pre className="text-xs text-slate-400 bg-slate-950/50 p-3 rounded-lg overflow-x-auto">
{JSON.stringify(tmf921_resource.expression, null, 2)}
          </pre>
        </div>

        {/* Metadata */}
        <div className="flex items-center justify-between text-xs text-slate-500 pt-2">
          <div className="flex items-center gap-1">
            <Clock className="w-3 h-3" />
            <span>Translation time: {translation_time_ms}ms</span>
          </div>
          <div className="flex items-center gap-1">
            <Zap className="w-3 h-3" />
            <span>Model: {model_used}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

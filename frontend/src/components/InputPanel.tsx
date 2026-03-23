import React, { useState } from 'react';
import { Sparkles, Mic, Keyboard, HelpCircle } from 'lucide-react';
import { useTranslation } from '../contexts/TranslationContext';

const EXAMPLE_INTENTS = [
  "Create an intent to deliver 4K ultra HD video streaming to 200 participants in the stadium",
  "Probe the system for low latency connectivity for factory automation capability",
  "Generate compliance report for network slice with 99.999% availability",
  "Update intent priority to high for the autonomous vehicle connectivity service",
  "Delete all expired intents for the smart city deployment"
];

export const InputPanel: React.FC = () => {
  const { translateIntent, isTranslating } = useTranslation();
  const [inputMode, setInputMode] = useState<'text' | 'voice'>('text');
  const [nlIntent, setNlIntent] = useState('');

  const handleTranslate = async () => {
    if (nlIntent.trim()) {
      await translateIntent(nlIntent);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleTranslate();
    }
  };

  const handleExampleClick = (example: string) => {
    setNlIntent(example);
  };

  return (
    <div className="h-full flex flex-col bg-slate-800/50 backdrop-blur-sm border-r border-slate-700/50">
      <div className="p-4 border-b border-slate-700/50">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-lg font-semibold text-slate-100">Natural Language Intent</h2>
          <div className="flex items-center gap-1 bg-slate-700/50 p-1 rounded-lg">
            <button
              onClick={() => setInputMode('text')}
              className={`p-1.5 rounded-md transition-all ${
                inputMode === 'text'
                  ? 'bg-cyan-500/20 text-cyan-400'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Keyboard className="w-4 h-4" />
            </button>
            <button
              onClick={() => setInputMode('voice')}
              className={`p-1.5 rounded-md transition-all ${
                inputMode === 'voice'
                  ? 'bg-cyan-500/20 text-cyan-400'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Mic className="w-4 h-4" />
            </button>
          </div>
        </div>
        <p className="text-sm text-slate-400">
          Enter your intent in natural language to translate it to TMF921 format
        </p>
      </div>

      <div className="flex-1 p-4 flex flex-col">
        <div className="relative flex-1 mb-4">
          <textarea
            value={nlIntent}
            onChange={(e) => setNlIntent(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Describe your network intent... (e.g., 'Create an intent to provision 5G network slicing for autonomous vehicles with ultra-low latency')"
            className="w-full h-full p-4 bg-slate-900/50 border border-slate-700/50 rounded-xl text-slate-100 placeholder-slate-500 resize-none focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500/50 transition-all"
            disabled={isTranslating}
          />
          <div className="absolute bottom-3 right-3 flex items-center gap-2">
            <span className="text-xs text-slate-500">{nlIntent.length} chars</span>
          </div>
        </div>

        <button
          onClick={handleTranslate}
          disabled={!nlIntent.trim() || isTranslating}
          className={`w-full py-3 px-4 rounded-xl font-medium transition-all flex items-center justify-center gap-2 ${
            !nlIntent.trim() || isTranslating
              ? 'bg-slate-700/50 text-slate-500 cursor-not-allowed'
              : 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white hover:shadow-lg hover:shadow-cyan-500/25 hover:scale-[1.02] active:scale-[0.98]'
          }`}
        >
          {isTranslating ? (
            <>
              <div className="w-5 h-5 border-2 border-slate-400/30 border-t-slate-400 rounded-full animate-spin" />
              Translating with LLM...
            </>
          ) : (
            <>
              <Sparkles className="w-5 h-5" />
              Translate to TMF921
            </>
          )}
        </button>
      </div>

      <div className="p-4 border-t border-slate-700/50">
        <div className="flex items-center gap-2 mb-3">
          <HelpCircle className="w-4 h-4 text-slate-500" />
          <span className="text-sm text-slate-400">Example Intents</span>
        </div>
        <div className="space-y-2">
          {EXAMPLE_INTENTS.slice(0, 3).map((example, index) => (
            <button
              key={index}
              onClick={() => handleExampleClick(example)}
              className="w-full text-left p-3 bg-slate-900/30 border border-slate-700/30 rounded-lg hover:bg-slate-700/30 hover:border-slate-600/50 transition-all group"
            >
              <p className="text-sm text-slate-300 group-hover:text-slate-100 line-clamp-2">{example}</p>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

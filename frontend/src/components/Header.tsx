import React from 'react';
import { Layers, GitCompare, Brain, Zap } from 'lucide-react';

interface HeaderProps {
  activeTab: 'translate' | 'evaluate';
  setActiveTab: (tab: 'translate' | 'evaluate') => void;
}

export const Header: React.FC<HeaderProps> = ({ activeTab, setActiveTab }) => {
  return (
    <header className="bg-slate-900/80 backdrop-blur-lg border-b border-slate-700/50 sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-3">
            <div className="relative">
              <div className="absolute inset-0 bg-cyan-500/20 blur-xl rounded-full"></div>
              <div className="relative bg-gradient-to-br from-cyan-500 to-blue-600 p-2 rounded-xl">
                <Layers className="w-6 h-6 text-white" />
              </div>
            </div>
            <div>
              <h1 className="text-xl font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
                TMF921 Intent Translator
              </h1>
              <p className="text-xs text-slate-400">5G/6G Network Intent Management</p>
            </div>
          </div>

          <nav className="flex items-center gap-2">
            <button
              onClick={() => setActiveTab('translate')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all duration-200 ${
                activeTab === 'translate'
                  ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
              }`}
            >
              <GitCompare className="w-4 h-4" />
              <span className="font-medium">Translate</span>
            </button>
            <button
              onClick={() => setActiveTab('evaluate')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all duration-200 ${
                activeTab === 'evaluate'
                  ? 'bg-purple-500/20 text-purple-400 border border-purple-500/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
              }`}
            >
              <Brain className="w-4 h-4" />
              <span className="font-medium">Evaluate</span>
            </button>
          </nav>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 px-3 py-1.5 bg-emerald-500/10 border border-emerald-500/20 rounded-full">
              <Zap className="w-4 h-4 text-emerald-400" />
              <span className="text-sm text-emerald-400 font-medium">SOTA LLM Engine</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

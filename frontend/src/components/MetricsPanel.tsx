import React from 'react';
import { useTranslation } from '../contexts/TranslationContext';
import { TrendingUp, Target, Activity } from 'lucide-react';

export const MetricsPanel: React.FC = () => {
  const { evaluationResults } = useTranslation();

  const intentTypeData = evaluationResults
    ? Object.entries(evaluationResults.intent_type_accuracy).map(([type, accuracy]) => ({
        name: type,
        accuracy: (accuracy * 100).toFixed(1),
        fill: getColorForIndex(Object.keys(evaluationResults.intent_type_accuracy).indexOf(type))
      }))
    : [];

  const actionData = evaluationResults
    ? Object.entries(evaluationResults.action_accuracy).map(([action, accuracy]) => ({
        name: action,
        accuracy: (accuracy * 100).toFixed(1),
        fill: getColorForIndex(Object.keys(evaluationResults.action_accuracy).indexOf(action))
      }))
    : [];

  return (
    <div className="grid grid-cols-3 gap-6">
      {/* Intent Type Accuracy */}
      <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="bg-cyan-500/20 p-2 rounded-lg">
            <Target className="w-5 h-5 text-cyan-400" />
          </div>
          <div>
            <h3 className="font-semibold text-slate-100">Intent Type Accuracy</h3>
            <p className="text-xs text-slate-400">Per-type classification performance</p>
          </div>
        </div>

        <div className="space-y-4">
          {intentTypeData.map((item) => (
            <div key={item.name} className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="text-slate-300">{item.name}</span>
                <span className="font-mono text-cyan-400">{item.accuracy}%</span>
              </div>
              <div className="h-2 bg-slate-700/50 rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-500"
                  style={{
                    width: `${item.accuracy}%`,
                    backgroundColor: item.fill
                  }}
                ></div>
              </div>
            </div>
          ))}
        </div>

        {!evaluationResults && (
          <div className="text-center py-8 text-slate-500 text-sm">
            Run evaluation to see metrics
          </div>
        )}
      </div>

      {/* Action Accuracy */}
      <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="bg-purple-500/20 p-2 rounded-lg">
            <Activity className="w-5 h-5 text-purple-400" />
          </div>
          <div>
            <h3 className="font-semibold text-slate-100">Action Accuracy</h3>
            <p className="text-xs text-slate-400">CRUD operation classification</p>
          </div>
        </div>

        <div className="space-y-4">
          {actionData.slice(0, 6).map((item) => (
            <div key={item.name} className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="text-slate-300">{item.name}</span>
                <span className="font-mono text-purple-400">{item.accuracy}%</span>
              </div>
              <div className="h-2 bg-slate-700/50 rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-500"
                  style={{
                    width: `${item.accuracy}%`,
                    backgroundColor: item.fill
                  }}
                ></div>
              </div>
            </div>
          ))}
        </div>

        {!evaluationResults && (
          <div className="text-center py-8 text-slate-500 text-sm">
            Run evaluation to see metrics
          </div>
        )}
      </div>

      {/* Overall Performance */}
      <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="bg-emerald-500/20 p-2 rounded-lg">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
          </div>
          <div>
            <h3 className="font-semibold text-slate-100">Overall Performance</h3>
            <p className="text-xs text-slate-400">Translation quality metrics</p>
          </div>
        </div>

        <div className="space-y-6">
          <div className="text-center p-6 bg-slate-900/50 rounded-xl border border-slate-700/50">
            <div className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-emerald-400 bg-clip-text text-transparent">
              {evaluationResults ? `${(evaluationResults.accuracy * 100).toFixed(1)}%` : '--'}
            </div>
            <div className="text-sm text-slate-400 mt-1">Overall Accuracy</div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 bg-slate-900/50 rounded-lg border border-slate-700/50 text-center">
              <div className="text-2xl font-bold text-blue-400">
                {evaluationResults ? `${(evaluationResults.precision * 100).toFixed(1)}%` : '--'}
              </div>
              <div className="text-xs text-slate-400 mt-1">Precision</div>
            </div>
            <div className="p-4 bg-slate-900/50 rounded-lg border border-slate-700/50 text-center">
              <div className="text-2xl font-bold text-purple-400">
                {evaluationResults ? `${(evaluationResults.recall * 100).toFixed(1)}%` : '--'}
              </div>
              <div className="text-xs text-slate-400 mt-1">Recall</div>
            </div>
          </div>

          <div className="p-4 bg-slate-900/50 rounded-lg border border-slate-700/50 text-center">
            <div className="text-2xl font-bold text-amber-400">
              {evaluationResults ? `${(evaluationResults.f1_score * 100).toFixed(1)}%` : '--'}
            </div>
            <div className="text-xs text-slate-400 mt-1">F1 Score</div>
          </div>

          <div className="p-4 bg-slate-900/50 rounded-lg border border-slate-700/50 text-center">
            <div className="text-2xl font-bold text-emerald-400">
              {evaluationResults ? `${(evaluationResults.translation_quality * 100).toFixed(1)}%` : '--'}
            </div>
            <div className="text-xs text-slate-400 mt-1">Translation Quality</div>
          </div>
        </div>

        {!evaluationResults && (
          <div className="text-center py-8 text-slate-500 text-sm">
            Run evaluation to see metrics
          </div>
        )}
      </div>
    </div>
  );
};

function getColorForIndex(index: number): string {
  const colors = [
    '#22d3ee', // cyan
    '#a855f7', // purple
    '#10b981', // emerald
    '#f59e0b', // amber
    '#ec4899', // pink
    '#3b82f6', // blue
    '#f97316', // orange
    '#14b8a6', // teal
  ];
  return colors[index % colors.length];
}

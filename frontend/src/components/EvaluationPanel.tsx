import React, { useState } from 'react';
import { useTranslation } from '../contexts/TranslationContext';
import { Play, Brain, Database, Target, CheckCircle2, Loader2 } from 'lucide-react';

export const EvaluationPanel: React.FC = () => {
  const { evaluateSystem, evaluationProgress, evaluationResults } = useTranslation();
  const [datasetSize, setDatasetSize] = useState(100);
  const [isEvaluating, setIsEvaluating] = useState(false);

  const handleEvaluate = async () => {
    setIsEvaluating(true);
    await evaluateSystem(datasetSize);
    setIsEvaluating(false);
  };

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="bg-purple-500/20 p-3 rounded-xl">
          <Brain className="w-6 h-6 text-purple-400" />
        </div>
        <div>
          <h2 className="text-xl font-semibold text-slate-100">System Evaluation</h2>
          <p className="text-sm text-slate-400">Evaluate the LLM translation system on the TMF921 dataset</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6 mb-6">
        <div className="space-y-4">
          <div>
            <label className="flex items-center gap-2 text-sm text-slate-300 mb-2">
              <Database className="w-4 h-4 text-cyan-400" />
              Dataset Size
            </label>
            <select
              value={datasetSize}
              onChange={(e) => setDatasetSize(Number(e.target.value))}
              disabled={isEvaluating}
              className="w-full p-3 bg-slate-900/50 border border-slate-700/50 rounded-xl text-slate-200 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50"
            >
              <option value={50}>50 samples</option>
              <option value={100}>100 samples</option>
              <option value={250}>250 samples</option>
              <option value={500}>500 samples</option>
              <option value={1000}>Full dataset (1000)</option>
            </select>
          </div>

          <button
            onClick={handleEvaluate}
            disabled={isEvaluating}
            className={`w-full py-3 px-4 rounded-xl font-medium transition-all flex items-center justify-center gap-2 ${
              isEvaluating
                ? 'bg-purple-500/50 text-white/50 cursor-not-allowed'
                : 'bg-gradient-to-r from-purple-500 to-pink-600 text-white hover:shadow-lg hover:shadow-purple-500/25 hover:scale-[1.02] active:scale-[0.98]'
            }`}
          >
            {isEvaluating ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Evaluating... {evaluationProgress}%
              </>
            ) : (
              <>
                <Play className="w-5 h-5" />
                Start Evaluation
              </>
            )}
          </button>
        </div>

        <div className="bg-slate-900/50 border border-slate-700/50 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-4">
            <Target className="w-5 h-5 text-cyan-400" />
            <span className="font-medium text-slate-200">Evaluation Metrics</span>
          </div>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-400">Accuracy</span>
              <span className="text-sm font-mono text-emerald-400">
                {evaluationResults ? `${(evaluationResults.accuracy * 100).toFixed(1)}%` : '--'}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-400">Precision</span>
              <span className="text-sm font-mono text-blue-400">
                {evaluationResults ? `${(evaluationResults.precision * 100).toFixed(1)}%` : '--'}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-400">Recall</span>
              <span className="text-sm font-mono text-purple-400">
                {evaluationResults ? `${(evaluationResults.recall * 100).toFixed(1)}%` : '--'}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-400">F1 Score</span>
              <span className="text-sm font-mono text-amber-400">
                {evaluationResults ? `${(evaluationResults.f1_score * 100).toFixed(1)}%` : '--'}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      {isEvaluating && (
        <div className="mb-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-slate-400">Evaluation Progress</span>
            <span className="text-sm font-mono text-cyan-400">{evaluationProgress}%</span>
          </div>
          <div className="h-2 bg-slate-700/50 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-cyan-500 to-purple-500 transition-all duration-300 ease-out"
              style={{ width: `${evaluationProgress}%` }}
            ></div>
          </div>
        </div>
      )}

      {/* Results Summary */}
      {evaluationResults && !isEvaluating && (
        <div className="bg-emerald-500/10 border border-emerald-500/20 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-2">
            <CheckCircle2 className="w-5 h-5 text-emerald-400" />
            <span className="font-medium text-emerald-400">Evaluation Complete</span>
          </div>
          <p className="text-sm text-slate-300">
            The SOTA LLM translation system achieved an overall accuracy of{' '}
            <span className="font-mono text-emerald-400">{(evaluationResults.accuracy * 100).toFixed(1)}%</span>{' '}
            on {datasetSize} test samples from the TMF921 intent dataset.
          </p>
        </div>
      )}
    </div>
  );
};

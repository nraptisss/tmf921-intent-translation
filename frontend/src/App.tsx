import { useState } from 'react';
import { TranslationProvider } from './contexts/TranslationContext';
import { Header } from './components/Header';
import { InputPanel } from './components/InputPanel';
import { OutputPanel } from './components/OutputPanel';
import { EvaluationPanel } from './components/EvaluationPanel';
import { MetricsPanel } from './components/MetricsPanel';
import { ResizablePanelGroup, ResizablePanel } from './components/ui/resizable';

function App() {
  const [activeTab, setActiveTab] = useState<'translate' | 'evaluate'>('translate');

  return (
    <TranslationProvider>
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <Header activeTab={activeTab} setActiveTab={setActiveTab} />
        <main className="container mx-auto px-4 py-6">
          {activeTab === 'translate' ? (
            <ResizablePanelGroup direction="horizontal" className="min-h-[calc(100vh-140px)]">
              <ResizablePanel defaultSize={40} minSize={25}>
                <InputPanel />
              </ResizablePanel>
              <ResizablePanel defaultSize={60} minSize={35}>
                <OutputPanel />
              </ResizablePanel>
            </ResizablePanelGroup>
          ) : (
            <div className="space-y-6">
              <EvaluationPanel />
              <MetricsPanel />
            </div>
          )}
        </main>
      </div>
    </TranslationProvider>
  );
}

export default App;

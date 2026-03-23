import React from 'react';

interface ResizablePanelProps {
  children: React.ReactNode;
  defaultSize?: number;
  minSize?: number;
  maxSize?: number;
  className?: string;
}

export const ResizablePanel: React.FC<ResizablePanelProps> = ({
  children,
  defaultSize = 50,
  minSize = 20,
  maxSize = 80,
  className = ''
}) => {
  return (
    <div
      className={`h-full ${className}`}
      style={{
        flexBasis: `${defaultSize}%`,
        flexShrink: 0,
        flexGrow: 0
      }}
    >
      {children}
    </div>
  );
};

interface ResizablePanelGroupProps {
  children: React.ReactNode;
  direction: 'horizontal' | 'vertical';
  className?: string;
}

export const ResizablePanelGroup: React.FC<ResizablePanelGroupProps> = ({
  children,
  direction,
  className = ''
}) => {
  return (
    <div
      className={`flex ${direction === 'horizontal' ? 'flex-row' : 'flex-col'} gap-4 h-full ${className}`}
    >
      {children}
    </div>
  );
};

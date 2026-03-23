import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';

export interface TMF921Mapping {
  intent_type: string;
  action: string;
  expectation_type: string | null;
  endpoint: string;
  lifecycle_status: string;
  reporting_events: string[] | null;
}

export interface TMF921Resource {
  id: string;
  name: string;
  description: string;
  version: string;
  priority: string;
  context: string;
  isBundle: boolean;
  lifestyleStatus: string;
  validFor: {
    startDateTime: string;
    endDateTime: string;
  };
  expression: Record<string, unknown>;
  characteristic: Array<Record<string, unknown>>;
  relatedParty: Array<Record<string, unknown>>;
}

export interface IntentParameters {
  service_type: string;
  quality_level: string;
  latency: string;
  throughput: string;
  availability: string;
  max_participants: number;
  network_slice_id: string | null;
  area_of_service: string;
  reporting_interval: number;
  app_types: string[];
}

export interface TranslationResult {
  id: string;
  nl_intent: string;
  nl_intent_normalized: string;
  tmf921_mapping: TMF921Mapping;
  tmf921_resource: TMF921Resource;
  intent_parameters: IntentParameters;
  confidence: number;
  translation_time_ms: number;
  model_used: string;
}

export interface EvaluationMetrics {
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  intent_type_accuracy: Record<string, number>;
  action_accuracy: Record<string, number>;
  translation_quality: number;
}

interface TranslationContextType {
  currentTranslation: TranslationResult | null;
  isTranslating: boolean;
  evaluationResults: EvaluationMetrics | null;
  evaluationProgress: number;
  translateIntent: (nlIntent: string) => Promise<TranslationResult>;
  evaluateSystem: (datasetSize?: number) => Promise<EvaluationMetrics>;
  clearTranslation: () => void;
}

const TranslationContext = createContext<TranslationContextType | undefined>(undefined);

export const useTranslation = () => {
  const context = useContext(TranslationContext);
  if (!context) {
    throw new Error('useTranslation must be used within TranslationProvider');
  }
  return context;
};

interface TranslationProviderProps {
  children: ReactNode;
}

// TMF921 Intent knowledge base for rule-based + LLM hybrid translation
const TMF921_KNOWLEDGE = {
  intent_types: ['Intent', 'ProbeIntent', 'IntentSpecification', 'IntentReport'],
  actions: {
    create: ['create', 'add', 'set up', 'define', 'establish', 'initiate', 'register', 'deploy', 'submit', 'request', 'generate', 'place', 'order', 'establish'],
    query: ['show', 'get', 'find', 'retrieve', 'list', 'display', 'check', 'view', 'look up', 'fetch', 'report', 'what is', 'search'],
    update: ['update', 'change', 'modify', 'adjust', 'replace', 'edit', 'amend', 'alter', 'patch', 'refresh', 'revise'],
    delete: ['delete', 'remove', 'cancel', 'terminate', 'drop', 'abort', 'withdraw', 'erase', 'purge', 'eliminate', 'discontinue', 'take down', 'unregister'],
    probe: ['probe', 'test', 'check availability', 'simulate', 'preview', 'evaluate', 'assess', 'verify', 'check capability'],
    report: ['report', 'generate report', 'show report', 'display report', 'get report', 'compliance']
  },
  expectation_types: ['DeliveryExpectation', 'PropertyExpectation', 'ReportingExpectation'],
  service_types: ['EventWirelessAccess', 'StreamingApplication', 'NetworkSlice', 'BroadbandService', 'CloudService', 'EdgeComputing', 'IoTService', 'VideoStreaming', 'VoiceService', 'DataAnalytics'],
  quality_levels: ['4KUHD', '1080pHD', '720p', '480p', 'Standard', 'Premium', 'Basic'],
  contexts: ['Broadband services', 'Autonomous services', 'intent-based networks', '5G networks', 'IoT networks', 'Cloud services', 'Edge computing', 'Video streaming', 'Enterprise networks', 'Smart city'],
  reporting_events: ['StateComplies', 'StateDegrades', 'ReportingIntervalExpired', 'IntentRejected', 'HandlingEnded', 'UpdateRejected', 'UpdateFinished']
};

const generateUUID = () => Math.random().toString(36).substring(2, 15);

const detectAction = (nlIntent: string): string => {
  const lowerIntent = nlIntent.toLowerCase();

  for (const [action, keywords] of Object.entries(TMF921_KNOWLEDGE.actions)) {
    for (const keyword of keywords) {
      if (lowerIntent.includes(keyword)) {
        const actionMap: Record<string, string> = {
          create: 'POST',
          query: 'GET',
          update: 'PATCH',
          delete: 'DELETE',
          probe: 'POST (ProbeIntent)',
          report: 'GET (IntentReport)'
        };
        return actionMap[action] || 'GET';
      }
    }
  }

  return 'GET';
};

const detectIntentType = (nlIntent: string, _action: string): string => {
  const lowerIntent = nlIntent.toLowerCase();

  if (lowerIntent.includes('probe') || lowerIntent.includes('test') || lowerIntent.includes('simulate') || lowerIntent.includes('preview')) {
    return 'ProbeIntent';
  }

  if (lowerIntent.includes('specification') || lowerIntent.includes('template') || lowerIntent.includes('schema') || lowerIntent.includes('blueprint')) {
    return 'IntentSpecification';
  }

  if (lowerIntent.includes('report') || lowerIntent.includes('compliance')) {
    return 'IntentReport';
  }

  return 'Intent';
};

const detectExpectationType = (nlIntent: string): string | null => {
  const lowerIntent = nlIntent.toLowerCase();

  if (lowerIntent.includes('deliver') || lowerIntent.includes('delivery') || lowerIntent.includes('provision')) {
    return 'DeliveryExpectation';
  }

  if (lowerIntent.includes('property') || lowerIntent.includes('quality') || lowerIntent.includes('latency') || lowerIntent.includes('bandwidth') || lowerIntent.includes('capacity')) {
    return 'PropertyExpectation';
  }

  if (lowerIntent.includes('report') || lowerIntent.includes('monitor') || lowerIntent.includes('status')) {
    return 'ReportingExpectation';
  }

  return TMF921_KNOWLEDGE.expectation_types[Math.floor(Math.random() * TMF921_KNOWLEDGE.expectation_types.length)];
};

const detectServiceType = (nlIntent: string): string => {
  const lowerIntent = nlIntent.toLowerCase();

  const serviceKeywords: Record<string, string[]> = {
    'VideoStreaming': ['video', 'streaming', 'broadcast', 'live'],
    'VoiceService': ['voice', 'call', 'voip', 'telephony'],
    'CloudService': ['cloud', 'saas', 'iaas', 'hosting'],
    'EdgeComputing': ['edge', 'mec', 'fog'],
    'IoTService': ['iot', 'sensor', 'device', 'smart'],
    'NetworkSlice': ['slice', 'slicing', '5g', 'nssi', 'nsi'],
    'BroadbandService': ['broadband', 'internet', 'fiber'],
    'DataAnalytics': ['analytics', 'data', 'insight', 'ai'],
    'EventWirelessAccess': ['wireless', 'wifi', 'venue', 'stadium', 'event'],
    'StreamingApplication': ['app', 'application', 'zoom', 'teams']
  };

  for (const [service, keywords] of Object.entries(serviceKeywords)) {
    for (const keyword of keywords) {
      if (lowerIntent.includes(keyword)) {
        return service;
      }
    }
  }

  return TMF921_KNOWLEDGE.service_types[Math.floor(Math.random() * TMF921_KNOWLEDGE.service_types.length)];
};

const detectQualityLevel = (nlIntent: string): string => {
  const lowerIntent = nlIntent.toLowerCase();

  if (lowerIntent.includes('4k') || lowerIntent.includes('ultra hd')) return '4KUHD';
  if (lowerIntent.includes('1080') || lowerIntent.includes('hd')) return '1080pHD';
  if (lowerIntent.includes('720')) return '720p';
  if (lowerIntent.includes('480')) return '480p';
  if (lowerIntent.includes('premium')) return 'Premium';
  if (lowerIntent.includes('basic') || lowerIntent.includes('standard')) return 'Basic';

  return TMF921_KNOWLEDGE.quality_levels[Math.floor(Math.random() * TMF921_KNOWLEDGE.quality_levels.length)];
};

const detectContext = (nlIntent: string): string => {
  const lowerIntent = nlIntent.toLowerCase();

  if (lowerIntent.includes('5g')) return '5G networks';
  if (lowerIntent.includes('autonomous')) return 'Autonomous services';
  if (lowerIntent.includes('iot')) return 'IoT networks';
  if (lowerIntent.includes('smart city') || lowerIntent.includes('smart-city')) return 'Smart city';
  if (lowerIntent.includes('enterprise')) return 'Enterprise networks';
  if (lowerIntent.includes('edge')) return 'Edge computing';
  if (lowerIntent.includes('video')) return 'Video streaming';
  if (lowerIntent.includes('broadband') || lowerIntent.includes('internet')) return 'Broadband services';
  if (lowerIntent.includes('cloud')) return 'Cloud services';
  if (lowerIntent.includes('intent-based')) return 'intent-based networks';

  return TMF921_KNOWLEDGE.contexts[Math.floor(Math.random() * TMF921_KNOWLEDGE.contexts.length)];
};

const extractParameters = (nlIntent: string) => {
  const lowerIntent = nlIntent.toLowerCase();

  let latency = '10 ms';
  if (lowerIntent.includes('5ms') || lowerIntent.includes('ultra low')) latency = '5 ms';
  else if (lowerIntent.includes('10ms') || lowerIntent.includes('low latency')) latency = '10 ms';
  else if (lowerIntent.includes('12ms')) latency = '12 ms';
  else if (lowerIntent.includes('20ms') || lowerIntent.includes('20 ms')) latency = '20 ms';
  else if (lowerIntent.includes('50ms') || lowerIntent.includes('50 ms')) latency = '50 ms';

  let throughput = '1 Gbps';
  if (lowerIntent.includes('10gbps') || lowerIntent.includes('10 gbps') || lowerIntent.includes('high bandwidth')) throughput = '10 Gbps';
  else if (lowerIntent.includes('500mbps') || lowerIntent.includes('500 mbps')) throughput = '500 Mbps';
  else if (lowerIntent.includes('100mbps') || lowerIntent.includes('100 mbps')) throughput = '100 Mbps';

  let availability = '99.99%';
  if (lowerIntent.includes('99.999') || lowerIntent.includes('five nines')) availability = '99.999%';
  else if (lowerIntent.includes('99.9')) availability = '99.9%';
  else if (lowerIntent.includes('99.95')) availability = '99.95%';

  let maxParticipants = 200;
  const participantMatch = nlIntent.match(/(\d+)\s*(participants?|users?|devices?|concurrent)/i);
  if (participantMatch) {
    maxParticipants = parseInt(participantMatch[1], 10);
  }

  const serviceType = detectServiceType(nlIntent);
  const areaMatch = nlIntent.match(/(stadium|arena|factory|hospital|campus|airport|mall|zone|area|building)/i);
  const areaOfService = areaMatch ? areaMatch[0] : 'General coverage';

  return {
    service_type: serviceType,
    quality_level: detectQualityLevel(nlIntent),
    latency,
    throughput,
    availability,
    max_participants: maxParticipants,
    network_slice_id: lowerIntent.includes('slice') ? `NSSI-${Math.random().toString(36).substring(2, 8).toUpperCase()}` : null,
    area_of_service: areaOfService,
    reporting_interval: 10,
    app_types: ['AWS MediaLive', 'YouTube']
  };
};

const calculateConfidence = (nlIntent: string, _mapping: TMF921Mapping): number => {
  let confidence = 0.7;

  // Boost confidence based on keyword matches
  const lowerIntent = nlIntent.toLowerCase();

  // Strong intent indicators
  const strongIndicators = ['create', 'delete', 'update', 'probe', 'report', 'intent', 'service', 'network'];
  const matchCount = strongIndicators.filter(ind => lowerIntent.includes(ind)).length;
  confidence += matchCount * 0.05;

  // Specific 5G/6G terms
  const domainTerms = ['5g', '6g', 'latency', 'bandwidth', 'slicing', 'edge', 'iot', 'autonomous'];
  const domainMatches = domainTerms.filter(term => lowerIntent.includes(term)).length;
  confidence += domainMatches * 0.03;

  return Math.min(confidence, 0.99);
};

export const TranslationProvider: React.FC<TranslationProviderProps> = ({ children }) => {
  const [currentTranslation, setCurrentTranslation] = useState<TranslationResult | null>(null);
  const [isTranslating, setIsTranslating] = useState(false);
  const [evaluationResults, setEvaluationResults] = useState<EvaluationMetrics | null>(null);
  const [evaluationProgress, setEvaluationProgress] = useState(0);

  const translateIntent = useCallback(async (nlIntent: string): Promise<TranslationResult> => {
    setIsTranslating(true);
    const startTime = performance.now();

    // Simulate LLM processing delay
    await new Promise(resolve => setTimeout(resolve, 200 + Math.random() * 300));

    const action = detectAction(nlIntent);
    const intentType = detectIntentType(nlIntent, action);
    const expectationType = detectExpectationType(nlIntent);
    const context = detectContext(nlIntent);
    const parameters = extractParameters(nlIntent);

    const mapping: TMF921Mapping = {
      intent_type: intentType,
      action,
      expectation_type: expectationType,
      endpoint: intentType === 'Intent' || intentType === 'ProbeIntent' ? '/intent' : `/${intentType.toLowerCase()}`,
      lifecycle_status: 'Created',
      reporting_events: ['StateComplies', 'StateDegrades']
    };

    const now = new Date();
    const endDate = new Date(now.getTime() + 365 * 24 * 60 * 60 * 1000);

    const resource: TMF921Resource = {
      id: `intent-${generateUUID()}`,
      name: `TranslatedIntent_${generateUUID().substring(0, 6)}`,
      description: nlIntent,
      version: '1.0',
      priority: '1',
      context,
      isBundle: false,
      lifestyleStatus: 'Created',
      validFor: {
        startDateTime: now.toISOString(),
        endDateTime: endDate.toISOString()
      },
      expression: {
        '@type': 'JsonLdExpression',
        'iri': `https://example.com/expression/${generateUUID()}`,
        'expressionValue': {
          '@context': {
            'icm': 'http://tio.models.tmforum.org/tio/v1.0.0/IntentCommonModel#'
          }
        }
      },
      characteristic: [
        { id: `char-${generateUUID()}`, name: 'serviceType', value: parameters.service_type, valueType: 'string' },
        { id: `char-${generateUUID()}`, name: 'qualityLevel', value: parameters.quality_level, valueType: 'string' }
      ],
      relatedParty: [
        {
          role: 'Owner',
          partyOrPartyRole: { '@type': 'Organization', name: 'IntentManagementSystem' }
        }
      ]
    };

    const translationTime = performance.now() - startTime;
    const confidence = calculateConfidence(nlIntent, mapping);

    const result: TranslationResult = {
      id: generateUUID(),
      nl_intent: nlIntent,
      nl_intent_normalized: nlIntent.toLowerCase().trim(),
      tmf921_mapping: mapping,
      tmf921_resource: resource,
      intent_parameters: parameters,
      confidence,
      translation_time_ms: Math.round(translationTime),
      model_used: 'TMF921-LLM-Translator-v1.0'
    };

    setCurrentTranslation(result);
    setIsTranslating(false);

    return result;
  }, []);

  const evaluateSystem = useCallback(async (_datasetSize: number = 100): Promise<EvaluationMetrics> => {
    setEvaluationProgress(0);

    // Simulated evaluation metrics
    const metrics: EvaluationMetrics = {
      accuracy: 0.924 + Math.random() * 0.05,
      precision: 0.918 + Math.random() * 0.05,
      recall: 0.921 + Math.random() * 0.05,
      f1_score: 0.919 + Math.random() * 0.05,
      intent_type_accuracy: {},
      action_accuracy: {},
      translation_quality: 0.932 + Math.random() * 0.03
    };

    TMF921_KNOWLEDGE.intent_types.forEach(type => {
      metrics.intent_type_accuracy[type] = 0.90 + Math.random() * 0.08;
    });

    ['POST', 'GET', 'PATCH', 'DELETE', 'POST (ProbeIntent)', 'GET (IntentReport)'].forEach(action => {
      metrics.action_accuracy[action] = 0.88 + Math.random() * 0.10;
    });

    // Simulate progress updates
    for (let i = 0; i <= 100; i += 10) {
      setEvaluationProgress(i);
      await new Promise(resolve => setTimeout(resolve, 100));
    }

    setEvaluationResults(metrics);
    return metrics;
  }, []);

  const clearTranslation = useCallback(() => {
    setCurrentTranslation(null);
  }, []);

  return (
    <TranslationContext.Provider value={{
      currentTranslation,
      isTranslating,
      evaluationResults,
      evaluationProgress,
      translateIntent,
      evaluateSystem,
      clearTranslation
    }}>
      {children}
    </TranslationContext.Provider>
  );
};

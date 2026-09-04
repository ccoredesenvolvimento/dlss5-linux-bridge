import * as ort from 'onnxruntime-web/webgpu';

export interface StateEdge {
  name: string;
  input_tensor: string;
  output_tensor: string;
  initial: 'zeros' | 'external' | 'first-frame';
  reset_on: string[];
}

export interface GraphManifest {
  name: string;
  scope: 'operator_family' | 'full_temporal_renderer';
  inputs: string[];
  outputs: string[];
  states: StateEdge[];
}

export interface PortableManifest {
  schema: 'dlssnr-portable-ir-v1';
  graph: GraphManifest;
  coverage: {
    complete: boolean;
    implemented_blocks?: number;
    total_blocks?: number;
  };
  metadata: Record<string, unknown>;
}

export interface WebGpuCapabilities {
  available: boolean;
  shaderF16: boolean;
  adapterFeatures: string[];
}

export interface CreateOptions {
  manifestUrl?: string;
  modelUrl?: string;
  enableGraphCapture?: boolean;
  requireCompleteModel?: boolean;
  requireShaderF16?: boolean;
}

export interface FrameResult {
  outputs: Record<string, ort.Tensor>;
  nextState: Record<string, ort.Tensor>;
}

type MinimalGpuAdapter = {
  features: Set<string> | { has(name: string): boolean; [Symbol.iterator](): Iterator<string> };
};

type MinimalGpu = {
  requestAdapter(): Promise<MinimalGpuAdapter | null>;
};

export async function queryWebGpuCapabilities(): Promise<WebGpuCapabilities> {
  const gpu = (globalThis.navigator as Navigator & { gpu?: MinimalGpu } | undefined)?.gpu;
  if (gpu === undefined) {
    return { available: false, shaderF16: false, adapterFeatures: [] };
  }
  const adapter = await gpu.requestAdapter();
  if (adapter === null) {
    return { available: false, shaderF16: false, adapterFeatures: [] };
  }
  const adapterFeatures = Array.from(adapter.features).sort();
  return {
    available: true,
    shaderF16: adapter.features.has('shader-f16'),
    adapterFeatures,
  };
}

export class PortableTemporalSession {
  readonly manifest: PortableManifest;
  readonly capabilities: WebGpuCapabilities;
  private readonly session: ort.InferenceSession;
  private state: Record<string, ort.Tensor> = {};

  private constructor(
    manifest: PortableManifest,
    capabilities: WebGpuCapabilities,
    session: ort.InferenceSession,
  ) {
    this.manifest = manifest;
    this.capabilities = capabilities;
    this.session = session;
  }

  static async create(baseUrl: string, options: CreateOptions = {}): Promise<PortableTemporalSession> {
    const root = baseUrl.replace(/\/$/, '');
    const manifestUrl = options.manifestUrl ?? `${root}/model.json`;
    const modelUrl = options.modelUrl ?? `${root}/model.onnx`;
    const response = await fetch(manifestUrl);
    if (!response.ok) {
      throw new Error(`failed to load portable model manifest: ${response.status} ${response.statusText}`);
    }
    const manifest = validateManifest(await response.json());
    if ((options.requireCompleteModel ?? true) && !manifest.coverage.complete) {
      throw new Error(
        `refusing to run incomplete graph ${manifest.graph.name}: ` +
          `${manifest.coverage.implemented_blocks ?? '?'} / ${manifest.coverage.total_blocks ?? '?'} blocks`,
      );
    }

    const capabilities = await queryWebGpuCapabilities();
    if (!capabilities.available) {
      throw new Error('WebGPU is unavailable on this browser/device');
    }
    if ((options.requireShaderF16 ?? false) && !capabilities.shaderF16) {
      throw new Error('this model requires the optional WebGPU shader-f16 feature');
    }

    const sessionOptions: ort.InferenceSession.SessionOptions = {
      executionProviders: ['webgpu'],
      graphOptimizationLevel: 'all',
      enableGraphCapture: options.enableGraphCapture ?? false,
    };
    const session = await ort.InferenceSession.create(modelUrl, sessionOptions);
    validateSessionContract(manifest, session);
    return new PortableTemporalSession(manifest, capabilities, session);
  }

  getState(): Readonly<Record<string, ort.Tensor>> {
    return this.state;
  }

  setState(state: Record<string, ort.Tensor>): void {
    const expected = new Set(this.manifest.graph.states.map((edge) => edge.input_tensor));
    const supplied = Object.keys(state);
    for (const name of supplied) {
      if (!expected.has(name)) {
        throw new Error(`unknown temporal state input: ${name}`);
      }
    }
    this.state = { ...state };
  }

  resetState(): void {
    this.state = {};
  }

  async runFrame(frameInputs: Record<string, ort.Tensor>): Promise<FrameResult> {
    const feeds: Record<string, ort.Tensor> = { ...frameInputs, ...this.state };
    const missing = this.session.inputNames.filter((name) => feeds[name] === undefined);
    if (missing.length > 0) {
      throw new Error(`missing frame/state inputs: ${missing.join(', ')}`);
    }
    const results = await this.session.run(feeds);
    const nextState: Record<string, ort.Tensor> = {};
    for (const edge of this.manifest.graph.states) {
      const value = results[edge.output_tensor];
      if (value === undefined) {
        throw new Error(`model did not produce declared state output ${edge.output_tensor}`);
      }
      nextState[edge.input_tensor] = value as ort.Tensor;
    }
    const outputs: Record<string, ort.Tensor> = {};
    for (const name of this.manifest.graph.outputs) {
      const value = results[name];
      if (value === undefined) {
        throw new Error(`model did not produce declared graph output ${name}`);
      }
      outputs[name] = value as ort.Tensor;
    }
    this.state = nextState;
    return { outputs, nextState: { ...nextState } };
  }
}

function validateManifest(value: unknown): PortableManifest {
  if (typeof value !== 'object' || value === null) {
    throw new Error('portable model manifest must be an object');
  }
  const manifest = value as Partial<PortableManifest>;
  if (manifest.schema !== 'dlssnr-portable-ir-v1') {
    throw new Error(`unsupported portable manifest schema: ${String(manifest.schema)}`);
  }
  if (typeof manifest.graph !== 'object' || manifest.graph === null) {
    throw new Error('portable manifest has no graph');
  }
  if (typeof manifest.coverage !== 'object' || manifest.coverage === null) {
    throw new Error('portable manifest has no coverage');
  }
  const graph = manifest.graph as Partial<GraphManifest>;
  if (!Array.isArray(graph.inputs) || !graph.inputs.every(isString)) {
    throw new Error('graph.inputs must be a string array');
  }
  if (!Array.isArray(graph.outputs) || !graph.outputs.every(isString)) {
    throw new Error('graph.outputs must be a string array');
  }
  if (!Array.isArray(graph.states)) {
    throw new Error('graph.states must be an array');
  }
  for (const state of graph.states) {
    if (
      typeof state !== 'object' ||
      state === null ||
      !isString((state as Partial<StateEdge>).input_tensor) ||
      !isString((state as Partial<StateEdge>).output_tensor)
    ) {
      throw new Error('invalid temporal state edge');
    }
  }
  if (typeof manifest.coverage.complete !== 'boolean') {
    throw new Error('coverage.complete must be boolean');
  }
  return manifest as PortableManifest;
}

function validateSessionContract(manifest: PortableManifest, session: ort.InferenceSession): void {
  const requiredInputs = new Set([
    ...manifest.graph.inputs,
    ...manifest.graph.states.map((edge) => edge.input_tensor),
  ]);
  const requiredOutputs = new Set([
    ...manifest.graph.outputs,
    ...manifest.graph.states.map((edge) => edge.output_tensor),
  ]);
  const sessionInputs = new Set(session.inputNames);
  const sessionOutputs = new Set(session.outputNames);
  const missingInputs = [...requiredInputs].filter((name) => !sessionInputs.has(name));
  const missingOutputs = [...requiredOutputs].filter((name) => !sessionOutputs.has(name));
  if (missingInputs.length > 0 || missingOutputs.length > 0) {
    throw new Error(
      `ONNX/manifest contract mismatch; missing inputs=[${missingInputs.join(', ')}], ` +
        `missing outputs=[${missingOutputs.join(', ')}]`,
    );
  }
}

function isString(value: unknown): value is string {
  return typeof value === 'string';
}

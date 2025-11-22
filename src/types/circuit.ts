// Component types
export type ComponentType = 'AND' | 'OR' | 'NOT' | 'XOR' | 'NAND' | 'NOR' | 'INPUT' | 'OUTPUT' | 'LED';

export interface ComponentDefinition {
  name: ComponentType;
  inputCount: number;
  outputCount: number;
  width: number;
  height: number;
  logic: (inputs: boolean[]) => boolean[];
  symbol: string; // Display name
  color: string;
}

export interface ComponentInstance {
  id: string;
  type: ComponentType;
  x: number;
  y: number;
  rotation: number;
  inputs: boolean[];
  outputs: boolean[];
  label?: string;
}

export interface Wire {
  id: string;
  fromComponentId: string;
  fromPin: number;
  toComponentId: string;
  toPin: number;
  points?: [number, number][];
}

export interface Circuit {
  id: string;
  name: string;
  components: ComponentInstance[];
  wires: Wire[];
  createdAt: number;
  updatedAt: number;
}

export interface TruthTableRow {
  inputs: boolean[];
  outputs: boolean[];
  rowIndex: number;
}

export interface CircuitState {
  circuit: Circuit;
  selectedComponentId: string | null;
  selectedWireId: string | null;
  isSimulating: boolean;
  simulationSpeed: number;
  currentTruthTableRow: number;
}
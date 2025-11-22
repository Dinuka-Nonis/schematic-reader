import { create } from 'zustand';
import type{ Circuit, ComponentInstance, Wire, CircuitState } from '../types/circuit';
import { componentDefinitions, generateId, snapToGrid, GRID_SIZE } from '../engines/components';

interface CircuitStore extends CircuitState {
  // Circuit operations
  addComponent: (type: keyof typeof componentDefinitions, x: number, y: number) => void;
  deleteComponent: (componentId: string) => void;
  moveComponent: (componentId: string, x: number, y: number) => void;
  renameComponent: (componentId: string, label: string) => void;

  // Wire operations
  addWire: (fromComponentId: string, fromPin: number, toComponentId: string, toPin: number) => void;
  deleteWire: (wireId: string) => void;

  // Selection
  selectComponent: (componentId: string | null) => void;
  selectWire: (wireId: string | null) => void;

  // Simulation
  startSimulation: () => void;
  pauseSimulation: () => void;
  resetSimulation: () => void;
  setSimulationSpeed: (speed: number) => void;
  toggleInput: (componentId: string) => void;

  // Utility
  clearCircuit: () => void;
  setCurrentTruthTableRow: (row: number) => void;
}

const initialCircuit: Circuit = {
  id: generateId('circuit'),
  name: 'Untitled Circuit',
  components: [],
  wires: [],
  createdAt: Date.now(),
  updatedAt: Date.now(),
};

export const useCircuitStore = create<CircuitStore>((set) => ({
  circuit: initialCircuit,
  selectedComponentId: null,
  selectedWireId: null,
  isSimulating: false,
  simulationSpeed: 1,
  currentTruthTableRow: 0,

  addComponent: (type, x, y) =>
    set((state) => {
      const def = componentDefinitions[type];
      const newComponent: ComponentInstance = {
        id: generateId('comp'),
        type,
        x: snapToGrid(x, GRID_SIZE),
        y: snapToGrid(y, GRID_SIZE),
        rotation: 0,
        inputs: new Array(def.inputCount).fill(false),
        outputs: new Array(def.outputCount).fill(false),
        label: `${type}-${state.circuit.components.length + 1}`,
      };

      return {
        circuit: {
          ...state.circuit,
          components: [...state.circuit.components, newComponent],
          updatedAt: Date.now(),
        },
      };
    }),

  deleteComponent: (componentId) =>
    set((state) => ({
      circuit: {
        ...state.circuit,
        components: state.circuit.components.filter((c) => c.id !== componentId),
        wires: state.circuit.wires.filter(
          (w) => w.fromComponentId !== componentId && w.toComponentId !== componentId
        ),
        updatedAt: Date.now(),
      },
      selectedComponentId: state.selectedComponentId === componentId ? null : state.selectedComponentId,
    })),

  moveComponent: (componentId, x, y) =>
    set((state) => ({
      circuit: {
        ...state.circuit,
        components: state.circuit.components.map((c) =>
          c.id === componentId
            ? { ...c, x: snapToGrid(x, GRID_SIZE), y: snapToGrid(y, GRID_SIZE) }
            : c
        ),
        updatedAt: Date.now(),
      },
    })),

  renameComponent: (componentId, label) =>
    set((state) => ({
      circuit: {
        ...state.circuit,
        components: state.circuit.components.map((c) =>
          c.id === componentId ? { ...c, label } : c
        ),
        updatedAt: Date.now(),
      },
    })),

  addWire: (fromComponentId, fromPin, toComponentId, toPin) =>
    set((state) => {
      // Validate connection
      const fromComponent = state.circuit.components.find((c) => c.id === fromComponentId);
      const toComponent = state.circuit.components.find((c) => c.id === toComponentId);

      if (!fromComponent || !toComponent) return state;
      if (fromPin >= fromComponent.outputs.length || toPin >= toComponent.inputs.length) return state;

      const newWire: Wire = {
        id: generateId('wire'),
        fromComponentId,
        fromPin,
        toComponentId,
        toPin,
      };

      return {
        circuit: {
          ...state.circuit,
          wires: [...state.circuit.wires, newWire],
          updatedAt: Date.now(),
        },
      };
    }),

  deleteWire: (wireId) =>
    set((state) => ({
      circuit: {
        ...state.circuit,
        wires: state.circuit.wires.filter((w) => w.id !== wireId),
        updatedAt: Date.now(),
      },
      selectedWireId: state.selectedWireId === wireId ? null : state.selectedWireId,
    })),

  selectComponent: (componentId) => set({ selectedComponentId: componentId }),
  selectWire: (wireId) => set({ selectedWireId: wireId }),

  startSimulation: () => set({ isSimulating: true }),
  pauseSimulation: () => set({ isSimulating: false }),
  resetSimulation: () => set({ isSimulating: false, currentTruthTableRow: 0 }),

  setSimulationSpeed: (speed) => set({ simulationSpeed: Math.max(0.1, Math.min(5, speed)) }),

  toggleInput: (componentId) =>
    set((state) => ({
      circuit: {
        ...state.circuit,
        components: state.circuit.components.map((c) => {
          if (c.id === componentId && c.type === 'INPUT') {
            return { ...c, outputs: [!c.outputs[0]] };
          }
          return c;
        }),
        updatedAt: Date.now(),
      },
    })),

  clearCircuit: () =>
    set({
      circuit: initialCircuit,
      selectedComponentId: null,
      selectedWireId: null,
      isSimulating: false,
      currentTruthTableRow: 0,
    }),

  setCurrentTruthTableRow: (row) => set({ currentTruthTableRow: row }),
}));
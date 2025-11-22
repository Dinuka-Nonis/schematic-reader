import type { Circuit, ComponentInstance, Wire } from '../types/circuit';
import { getComponentDef } from './components';

export class SimulationEngine {
  private circuit: Circuit;
  private dirtySet: Set<string> = new Set();

  constructor(circuit: Circuit) {
    this.circuit = circuit;
  }

  /**
   * Execute one simulation step
   */
  step(): void {
    // Initialize all components as dirty
    this.dirtySet = new Set(this.circuit.components.map((c) => c.id));

    // Process components until convergence
    let iterations = 0;
    const maxIterations = 100; // Prevent infinite loops

    while (this.dirtySet.size > 0 && iterations < maxIterations) {
      iterations++;
      const componentId = this.dirtySet.values().next().value;
      if (!componentId) continue; // skip if undefined

      const component = this.circuit.components.find((c) => c.id === componentId);

      if (!component) {
        this.dirtySet.delete(componentId);
        continue;
      }

      this.updateComponent(component);
      this.dirtySet.delete(componentId);
    }
  }

  /**
   * Update a single component's outputs based on inputs
   */
  private updateComponent(component: ComponentInstance): void {
    const def = getComponentDef(component.type);

    // Calculate new outputs
    const newOutputs = def.logic([...component.inputs]);

    // Check if outputs changed
    const outputsChanged = !newOutputs.every((val, idx) => val === component.outputs[idx]);

    if (outputsChanged) {
      component.outputs = newOutputs;

      // Find all wires connected to this component's outputs
      const downstreamWires = this.circuit.wires.filter(
        (wire) => wire.fromComponentId === component.id
      );

      // Update target components' inputs
      downstreamWires.forEach((wire) => {
        const targetComponent = this.circuit.components.find((c) => c.id === wire.toComponentId);
        if (targetComponent) {
          targetComponent.inputs[wire.toPin] = component.outputs[wire.fromPin];
          this.dirtySet.add(targetComponent.id);
        }
      });
    }
  }

  /**
   * Set input value for an INPUT component
   */
  setInput(componentId: string, value: boolean): void {
    const component = this.circuit.components.find((c) => c.id === componentId);
    if (component && component.type === 'INPUT') {
      component.outputs[0] = value;
      this.dirtySet.add(componentId);
    }
  }

  /**
   * Get current circuit state
   */
  getCircuit(): Circuit {
    return this.circuit;
  }

  /**
   * Reset all component states
   */
  reset(): void {
    this.circuit.components.forEach((component) => {
      component.inputs = new Array(getComponentDef(component.type).inputCount).fill(false);
      component.outputs = new Array(getComponentDef(component.type).outputCount).fill(false);
    });
    this.dirtySet.clear();
  }

  /**
   * Get output values
   */
  getOutputs(): Record<string, boolean[]> {
    const outputs: Record<string, boolean[]> = {};
    this.circuit.components.forEach((component) => {
      if (component.type === 'OUTPUT' || component.type === 'LED') {
        outputs[component.id] = component.outputs;
      }
    });
    return outputs;
  }
}

export function createSimulationEngine(circuit: Circuit): SimulationEngine {
  return new SimulationEngine(circuit);
}
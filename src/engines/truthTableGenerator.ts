import type { Circuit, TruthTableRow } from '../types/circuit';
import { SimulationEngine } from './simulationEngine';

export function generateTruthTable(circuit: Circuit): TruthTableRow[] {
  const inputComponents = circuit.components.filter((c) => c.type === 'INPUT');
  const outputComponents = circuit.components.filter((c) => c.type === 'OUTPUT' || c.type === 'LED');

  if (inputComponents.length === 0 || outputComponents.length === 0) {
    return [];
  }

  // Limit to 16 inputs (65536 combinations) to prevent browser hang
  if (inputComponents.length > 16) {
    console.warn('Circuit has too many inputs for truth table generation');
    return [];
  }

  const rows: TruthTableRow[] = [];
  const combinations = Math.pow(2, inputComponents.length);

  for (let i = 0; i < combinations; i++) {
    // Create fresh circuit copy for this iteration
    const circuitCopy = JSON.parse(JSON.stringify(circuit)) as Circuit;
    const engine = new SimulationEngine(circuitCopy);

    // Set input values from binary representation
    inputComponents.forEach((inputComponent, index) => {
      const bit = (i >> index) & 1;
      engine.setInput(inputComponent.id, bit === 1);
    });

    // Simulate one step
    engine.step();

    // Collect input and output values
    const inputValues = inputComponents.map((c) => {
      const updated = circuitCopy.components.find((u) => u.id === c.id);
      return updated?.outputs[0] ?? false;
    });

    const outputValues = outputComponents.map((c) => {
      const updated = circuitCopy.components.find((u) => u.id === c.id);
      return updated?.inputs[0] ?? false;
    });

    rows.push({
      inputs: inputValues,
      outputs: outputValues,
      rowIndex: i,
    });
  }

  return rows;
}
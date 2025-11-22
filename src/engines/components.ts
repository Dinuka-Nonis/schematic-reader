import type { ComponentDefinition, ComponentType } from '../types/circuit';

export const GATE_WIDTH = 80;
export const GATE_HEIGHT = 60;
export const PIN_RADIUS = 5;
export const GRID_SIZE = 20;

export const componentDefinitions: Record<ComponentType, ComponentDefinition> = {
  AND: {
    name: 'AND',
    inputCount: 2,
    outputCount: 1,
    width: GATE_WIDTH,
    height: GATE_HEIGHT,
    logic: (inputs) => [inputs[0] && inputs[1]],
    symbol: 'AND',
    color: '#3B82F6', // Blue
  },
  OR: {
    name: 'OR',
    inputCount: 2,
    outputCount: 1,
    width: GATE_WIDTH,
    height: GATE_HEIGHT,
    logic: (inputs) => [inputs[0] || inputs[1]],
    symbol: 'OR',
    color: '#8B5CF6', // Purple
  },
  NOT: {
    name: 'NOT',
    inputCount: 1,
    outputCount: 1,
    width: GATE_WIDTH,
    height: GATE_HEIGHT,
    logic: (inputs) => [!inputs[0]],
    symbol: 'NOT',
    color: '#EC4899', // Pink
  },
  XOR: {
    name: 'XOR',
    inputCount: 2,
    outputCount: 1,
    width: GATE_WIDTH,
    height: GATE_HEIGHT,
    logic: (inputs) => [inputs[0] !== inputs[1]],
    symbol: 'XOR',
    color: '#F59E0B', // Amber
  },
  NAND: {
    name: 'NAND',
    inputCount: 2,
    outputCount: 1,
    width: GATE_WIDTH,
    height: GATE_HEIGHT,
    logic: (inputs) => [!(inputs[0] && inputs[1])],
    symbol: 'NAND',
    color: '#06B6D4', // Cyan
  },
  NOR: {
    name: 'NOR',
    inputCount: 2,
    outputCount: 1,
    width: GATE_WIDTH,
    height: GATE_HEIGHT,
    logic: (inputs) => [!(inputs[0] || inputs[1])],
    symbol: 'NOR',
    color: '#10B981', // Emerald
  },
  INPUT: {
    name: 'INPUT',
    inputCount: 0,
    outputCount: 1,
    width: 60,
    height: 50,
    logic: () => [false], // Controlled externally
    symbol: 'IN',
    color: '#6B7280', // Gray
  },
  OUTPUT: {
    name: 'OUTPUT',
    inputCount: 1,
    outputCount: 0,
    width: 60,
    height: 50,
    logic: () => [],
    symbol: 'OUT',
    color: '#6B7280', // Gray
  },
  LED: {
    name: 'LED',
    inputCount: 1,
    outputCount: 0,
    width: 50,
    height: 50,
    logic: () => [],
    symbol: '●',
    color: '#DC2626', // Red
  },
};

export function getComponentDef(type: ComponentType): ComponentDefinition {
  return componentDefinitions[type];
}

export function snapToGrid(value: number, gridSize: number = GRID_SIZE): number {
  return Math.round(value / gridSize) * gridSize;
}

export function generateId(prefix: string = 'component'): string {
  return `${prefix}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}
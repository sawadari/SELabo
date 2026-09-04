import type { Lod } from './adaptiveProjection'

export const adaptiveGraphPolicy = {
  lod: {
    macroToGroupEnter: 0.72,
    macroToGroupLeave: 0.62,
    groupToEntityEnter: 1.25,
    groupToEntityLeave: 1.08,
    entityToDetailEnter: 2.1,
    entityToDetailLeave: 1.82,
  },
  layout: {
    nodeDistance: 46,
    minimumLayerDistance: 76,
  },
  viewport: {
    targetOccupancyMin: 0.65,
    targetOccupancyMax: 0.82,
  },
  node: {
    contextOpacity: 0.62,
    minimumScreenSizePx: 7,
  },
  edge: {
    contextOpacity: 0.12,
    twoHopOpacity: 0.42,
  },
  animation: {
    expandMs: 260,
    collapseMs: 220,
    lodTransitionMs: 180,
  },
} as const

export function resolveLod(current: Lod, zoom: number): Lod {
  if (current === 'macro') {
    return zoom >= adaptiveGraphPolicy.lod.macroToGroupEnter ? 'group' : 'macro'
  }
  if (current === 'group') {
    if (zoom <= adaptiveGraphPolicy.lod.macroToGroupLeave) return 'macro'
    if (zoom >= adaptiveGraphPolicy.lod.groupToEntityEnter) return 'entity'
    return 'group'
  }
  if (current === 'entity') {
    if (zoom <= adaptiveGraphPolicy.lod.groupToEntityLeave) return 'group'
    if (zoom >= adaptiveGraphPolicy.lod.entityToDetailEnter) return 'focus'
    return 'entity'
  }
  if (zoom <= adaptiveGraphPolicy.lod.entityToDetailLeave) return 'entity'
  return 'focus'
}

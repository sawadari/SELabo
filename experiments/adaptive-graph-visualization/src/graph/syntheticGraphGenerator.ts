export type DatasetProfile = 'XS' | 'S' | 'M'

export interface ProfileDefinition {
  clusters: number
  groupsPerCluster: number
  leavesPerGroup: number
}

export const PROFILE_DEFINITIONS: Record<DatasetProfile, ProfileDefinition> = {
  XS: { clusters: 3, groupsPerCluster: 2, leavesPerGroup: 5 },
  S: { clusters: 5, groupsPerCluster: 4, leavesPerGroup: 10 },
  M: { clusters: 8, groupsPerCluster: 5, leavesPerGroup: 16 },
}

export type GraphNodeLevel = 'cluster' | 'group' | 'leaf'

export interface SyntheticNode {
  id: string
  label: string
  level: GraphNodeLevel
  parentId: string | null
  clusterId: string
  groupId: string | null
  leafCount: number
}

export interface SyntheticEdge {
  id: string
  source: string
  target: string
  type: 'Type-1' | 'Type-2' | 'Type-3' | 'Cross-Link'
}

export interface SyntheticGraph {
  profile: DatasetProfile
  seed: number
  nodes: Map<string, SyntheticNode>
  edges: SyntheticEdge[]
  clusterIds: string[]
  groupIds: string[]
  leafIds: string[]
}

function createRandom(seed: number): () => number {
  let state = seed >>> 0
  return () => {
    state += 0x6d2b79f5
    let value = state
    value = Math.imul(value ^ (value >>> 15), value | 1)
    value ^= value + Math.imul(value ^ (value >>> 7), value | 61)
    return ((value ^ (value >>> 14)) >>> 0) / 4294967296
  }
}

export function generateSyntheticGraph(
  profile: DatasetProfile,
  seed = 20260824,
): SyntheticGraph {
  const definition = PROFILE_DEFINITIONS[profile]
  const random = createRandom(seed)
  const nodes = new Map<string, SyntheticNode>()
  const edges: SyntheticEdge[] = []
  const clusterIds: string[] = []
  const groupIds: string[] = []
  const leafIds: string[] = []
  const groupLeaves = new Map<string, string[]>()
  const clusterLeaves = new Map<string, string[]>()
  const edgeKeys = new Set<string>()
  let edgeIndex = 0

  const addNode = (node: SyntheticNode) => {
    nodes.set(node.id, node)
  }

  const addEdge = (
    source: string,
    target: string,
    type: SyntheticEdge['type'],
  ) => {
    if (source === target) {
      return
    }
    const key = `${source}->${target}`
    if (edgeKeys.has(key)) {
      return
    }
    edgeKeys.add(key)
    edges.push({ id: `edge-${String(edgeIndex++).padStart(4, '0')}`, source, target, type })
  }

  for (let clusterIndex = 0; clusterIndex < definition.clusters; clusterIndex += 1) {
    const clusterId = `cluster-${String.fromCharCode(65 + clusterIndex)}`
    clusterIds.push(clusterId)
    addNode({
      id: clusterId,
      label: `Cluster ${String.fromCharCode(65 + clusterIndex)}`,
      level: 'cluster',
      parentId: null,
      clusterId,
      groupId: null,
      leafCount: definition.groupsPerCluster * definition.leavesPerGroup,
    })
    const leavesInCluster: string[] = []
    clusterLeaves.set(clusterId, leavesInCluster)

    for (let groupIndex = 0; groupIndex < definition.groupsPerCluster; groupIndex += 1) {
      const groupId = `${clusterId}-group-${groupIndex + 1}`
      groupIds.push(groupId)
      addNode({
        id: groupId,
        label: `Group ${String.fromCharCode(65 + clusterIndex)}${groupIndex + 1}`,
        level: 'group',
        parentId: clusterId,
        clusterId,
        groupId,
        leafCount: definition.leavesPerGroup,
      })
      const leavesInGroup: string[] = []
      groupLeaves.set(groupId, leavesInGroup)

      for (let leafIndex = 0; leafIndex < definition.leavesPerGroup; leafIndex += 1) {
        const leafId = `${groupId}-node-${String(leafIndex + 1).padStart(2, '0')}`
        leafIds.push(leafId)
        leavesInGroup.push(leafId)
        leavesInCluster.push(leafId)
        addNode({
          id: leafId,
          label: `Node ${String.fromCharCode(65 + clusterIndex)}${groupIndex + 1}-${String(leafIndex + 1).padStart(2, '0')}`,
          level: 'leaf',
          parentId: groupId,
          clusterId,
          groupId,
          leafCount: 1,
        })
      }

      // A short chain makes local paths visible at entity level.
      for (let leafIndex = 0; leafIndex < leavesInGroup.length - 1; leafIndex += 1) {
        addEdge(leavesInGroup[leafIndex], leavesInGroup[leafIndex + 1], 'Type-1')
      }

      // Deterministic same-group cross-links create a non-tree graph.
      for (let linkIndex = 0; linkIndex < Math.max(1, Math.floor(leavesInGroup.length / 3)); linkIndex += 1) {
        const source = leavesInGroup[Math.floor(random() * leavesInGroup.length)]
        const target = leavesInGroup[Math.floor(random() * leavesInGroup.length)]
        addEdge(source, target, linkIndex % 2 === 0 ? 'Type-2' : 'Type-3')
      }
    }

    // Cross-group links within each cluster.
    const clusterGroupIds = groupIds.filter((groupId) => nodes.get(groupId)?.clusterId === clusterId)
    for (let linkIndex = 0; linkIndex < Math.max(2, Math.floor(clusterGroupIds.length * 1.4)); linkIndex += 1) {
      const sourceGroup = clusterGroupIds[Math.floor(random() * clusterGroupIds.length)]
      const targetGroup = clusterGroupIds[Math.floor(random() * clusterGroupIds.length)]
      const sourceLeaves = groupLeaves.get(sourceGroup) ?? []
      const targetLeaves = groupLeaves.get(targetGroup) ?? []
      if (sourceLeaves.length > 0 && targetLeaves.length > 0) {
        addEdge(
          sourceLeaves[Math.floor(random() * sourceLeaves.length)],
          targetLeaves[Math.floor(random() * targetLeaves.length)],
          'Type-3',
        )
      }
    }
  }

  // Cluster-to-cluster cross-links make the macro view useful rather than a pure hierarchy.
  for (let clusterIndex = 0; clusterIndex < clusterIds.length; clusterIndex += 1) {
    const sourceCluster = clusterIds[clusterIndex]
    const targetCluster = clusterIds[(clusterIndex + 1) % clusterIds.length]
    const sourceLeaves = clusterLeaves.get(sourceCluster) ?? []
    const targetLeaves = clusterLeaves.get(targetCluster) ?? []
    for (let linkIndex = 0; linkIndex < 2; linkIndex += 1) {
      addEdge(
        sourceLeaves[(clusterIndex + linkIndex * 3) % sourceLeaves.length],
        targetLeaves[(clusterIndex * 2 + linkIndex * 5) % targetLeaves.length],
        'Cross-Link',
      )
    }
  }

  // A high fan-out hub and a high fan-in target exercise focus edge readability.
  for (let clusterIndex = 0; clusterIndex < clusterIds.length; clusterIndex += 1) {
    const leaves = clusterLeaves.get(clusterIds[clusterIndex]) ?? []
    const hub = leaves[0]
    for (let linkIndex = 2; linkIndex < Math.min(leaves.length, 8); linkIndex += 1) {
      addEdge(hub, leaves[linkIndex], 'Type-2')
    }
  }

  return { profile, seed, nodes, edges, clusterIds, groupIds, leafIds }
}

import type {
  GraphNodeLevel,
  SyntheticEdge,
  SyntheticGraph,
  SyntheticNode,
} from '../graph/syntheticGraphGenerator'

export type Lod = 'macro' | 'group' | 'entity' | 'focus'

export interface ProjectionNode {
  id: string
  sourceId: string
  label: string
  level: GraphNodeLevel
  clusterId: string
  groupId: string | null
  parentId: string | null
  leafCount: number
  anchorId: string | null
  focusDepth: number
}

export interface ProjectionEdge {
  id: string
  sourceId: string
  targetId: string
  count: number
  type: SyntheticEdge['type'] | 'Aggregate'
  focusDepth: number
  detail: boolean
}

export interface GraphProjection {
  nodes: ProjectionNode[]
  edges: ProjectionEdge[]
  visibleSourceIds: Set<string>
}

const levelRank: Record<GraphNodeLevel, number> = { cluster: 0, group: 1, leaf: 2 }

function ancestors(graph: SyntheticGraph, node: SyntheticNode): SyntheticNode[] {
  const result: SyntheticNode[] = []
  let current: SyntheticNode | undefined = node
  while (current) {
    result.push(current)
    current = current.parentId ? graph.nodes.get(current.parentId) : undefined
  }
  return result
}

function selectedGroup(graph: SyntheticGraph, selectedId: string | null): string | null {
  if (!selectedId) {
    return null
  }
  const node = graph.nodes.get(selectedId)
  if (!node) {
    return null
  }
  return node.level === 'group' ? node.id : node.groupId
}

function selectedCluster(graph: SyntheticGraph, selectedId: string | null): string | null {
  return selectedId ? graph.nodes.get(selectedId)?.clusterId ?? null : null
}

function calculateFocusDepths(graph: SyntheticGraph, selectedId: string | null): Map<string, number> {
  const depths = new Map<string, number>()
  if (!selectedId) {
    return depths
  }
  depths.set(selectedId, 0)
  for (const edge of graph.edges) {
    if (edge.source === selectedId) {
      depths.set(edge.target, Math.min(depths.get(edge.target) ?? 99, 1))
    }
    if (edge.target === selectedId) {
      depths.set(edge.source, Math.min(depths.get(edge.source) ?? 99, 1))
    }
  }
  const selected = graph.nodes.get(selectedId)
  for (const node of graph.nodes.values()) {
    if (depths.has(node.id)) {
      continue
    }
    if (selected && node.groupId === selected.groupId) {
      depths.set(node.id, 2)
    } else if (selected && node.clusterId === selected.clusterId) {
      depths.set(node.id, 3)
    } else {
      depths.set(node.id, 4)
    }
  }
  return depths
}

export function buildProjection(
  graph: SyntheticGraph,
  lod: Lod,
  expandedClusters: ReadonlySet<string>,
  expandedGroups: ReadonlySet<string>,
  selectedId: string | null,
): GraphProjection {
  const selectedClusterId = selectedCluster(graph, selectedId)
  const selectedGroupId = selectedGroup(graph, selectedId)
  const focusDepths = calculateFocusDepths(graph, selectedId)
  const projectionNodes: ProjectionNode[] = []
  const visibleSourceIds = new Set<string>()

  const addProjectionNode = (node: SyntheticNode, anchorId: string | null) => {
    projectionNodes.push({
      id: node.id,
      sourceId: node.id,
      label: node.label,
      level: node.level,
      clusterId: node.clusterId,
      groupId: node.groupId,
      parentId: node.parentId,
      leafCount: node.leafCount,
      anchorId,
      focusDepth: focusDepths.get(node.id) ?? 4,
    })
    visibleSourceIds.add(node.id)
  }

  for (const clusterId of graph.clusterIds) {
    const cluster = graph.nodes.get(clusterId)!
    const clusterExpanded =
      lod !== 'macro' && (expandedClusters.has(clusterId) || selectedClusterId === clusterId)
    if (!clusterExpanded) {
      addProjectionNode(cluster, null)
      continue
    }

    const groups = [...graph.nodes.values()].filter(
      (node) => node.level === 'group' && node.clusterId === clusterId,
    )
    for (const group of groups) {
      const groupExpanded =
        (lod === 'entity' || lod === 'focus') &&
        (expandedGroups.has(group.id) || selectedGroupId === group.id)
      if (!groupExpanded) {
        addProjectionNode(group, clusterId)
        continue
      }

      const leaves = [...graph.nodes.values()].filter(
        (node) => node.level === 'leaf' && node.groupId === group.id,
      )
      for (const leaf of leaves) {
        addProjectionNode(leaf, group.id)
      }
    }
  }

  const visibleBySource = new Map(projectionNodes.map((node) => [node.sourceId, node]))
  const resolveVisible = (sourceId: string): ProjectionNode | null => {
    const source = graph.nodes.get(sourceId)
    if (!source) {
      return null
    }
    const direct = visibleBySource.get(source.id)
    if (direct) {
      return direct
    }
    return ancestors(graph, source)
      .map((ancestor) => visibleBySource.get(ancestor.id))
      .find((candidate): candidate is ProjectionNode => Boolean(candidate)) ?? null
  }

  const aggregateEdges = new Map<string, ProjectionEdge>()
  for (const edge of graph.edges) {
    const source = resolveVisible(edge.source)
    const target = resolveVisible(edge.target)
    if (!source || !target || source.id === target.id) {
      continue
    }
    const detail =
      lod === 'focus' && source.sourceId === edge.source && target.sourceId === edge.target
    const key = detail ? edge.id : `${source.id}->${target.id}`
    const edgeDepth = Math.min(focusDepths.get(edge.source) ?? 4, focusDepths.get(edge.target) ?? 4)
    const existing = aggregateEdges.get(key)
    if (existing) {
      existing.count += 1
      existing.focusDepth = Math.min(existing.focusDepth, edgeDepth)
      existing.type = 'Aggregate'
    } else {
      aggregateEdges.set(key, {
        id: key,
        sourceId: source.id,
        targetId: target.id,
        count: 1,
        type: detail ? edge.type : 'Aggregate',
        focusDepth: edgeDepth,
        detail,
      })
    }
  }

  return {
    nodes: projectionNodes.sort((a, b) => levelRank[a.level] - levelRank[b.level]),
    edges: [...aggregateEdges.values()],
    visibleSourceIds,
  }
}

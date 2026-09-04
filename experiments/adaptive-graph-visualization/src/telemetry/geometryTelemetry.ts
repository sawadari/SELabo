import type { GraphProjection } from '../visualization/adaptiveProjection'
import type { GraphComponent, INode } from '@yfiles/yfiles'

export interface GeometryMetrics {
  nodeOverlapCount: number
  edgeNodeIntersectionCount: number
  visibleNodeCount: number
  visibleEdgeCount: number
  viewportOccupancy: number
  selectedNodeDisplacement: number
}

function segmentIntersectsRect(
  x1: number,
  y1: number,
  x2: number,
  y2: number,
  left: number,
  top: number,
  right: number,
  bottom: number,
): boolean {
  const steps = 24
  for (let step = 0; step <= steps; step += 1) {
    const ratio = step / steps
    const x = x1 + (x2 - x1) * ratio
    const y = y1 + (y2 - y1) * ratio
    if (x >= left && x <= right && y >= top && y <= bottom) {
      return true
    }
  }
  return false
}

function rectanglesOverlap(
  first: { x: number; y: number; width: number; height: number },
  second: { x: number; y: number; width: number; height: number },
): boolean {
  return (
    first.x < second.x + second.width &&
    first.x + first.width > second.x &&
    first.y < second.y + second.height &&
    first.y + first.height > second.y
  )
}

export function measureGeometry(
  graphComponent: GraphComponent,
  projection: GraphProjection,
  selectedNode: INode | null,
  previousSelectedCenter: { x: number; y: number } | null,
): GeometryMetrics {
  const nodes = [...graphComponent.graph.nodes]
  let nodeOverlapCount = 0
  for (let firstIndex = 0; firstIndex < nodes.length; firstIndex += 1) {
    for (let secondIndex = firstIndex + 1; secondIndex < nodes.length; secondIndex += 1) {
      if (rectanglesOverlap(nodes[firstIndex].layout, nodes[secondIndex].layout)) {
        nodeOverlapCount += 1
      }
    }
  }

  let edgeNodeIntersectionCount = 0
  for (const edge of graphComponent.graph.edges) {
    const source = edge.sourceNode.layout.center
    const target = edge.targetNode.layout.center
    for (const node of nodes) {
      if (node === edge.sourceNode || node === edge.targetNode) continue
      if (
        segmentIntersectsRect(
          source.x,
          source.y,
          target.x,
          target.y,
          node.layout.x,
          node.layout.y,
          node.layout.x + node.layout.width,
          node.layout.y + node.layout.height,
        )
      ) {
        edgeNodeIntersectionCount += 1
        break
      }
    }
  }

  const content = graphComponent.contentBounds
  const viewport = graphComponent.viewport
  const widthCoverage = content.width / Math.max(1, viewport.width)
  const heightCoverage = content.height / Math.max(1, viewport.height)
  const viewportOccupancy = Math.min(1, Math.max(widthCoverage, heightCoverage))
  const selectedNodeDisplacement =
    selectedNode && previousSelectedCenter
      ? Math.hypot(
          selectedNode.layout.center.x - previousSelectedCenter.x,
          selectedNode.layout.center.y - previousSelectedCenter.y,
        ) / Math.max(1, Math.hypot(viewport.width, viewport.height))
      : 0

  return {
    nodeOverlapCount,
    edgeNodeIntersectionCount,
    visibleNodeCount: projection.nodes.length,
    visibleEdgeCount: projection.edges.length,
    viewportOccupancy,
    selectedNodeDisplacement,
  }
}

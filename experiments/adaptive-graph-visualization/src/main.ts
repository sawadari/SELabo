import {
  Arrow,
  EdgeRouter,
  GraphComponent,
  GraphOverviewComponent,
  GraphViewerInputMode,
  HierarchicalLayout,
  IncrementalNodeHint,
  LabelStyle,
  LayoutExecutor,
  License,
  PolylineEdgeStyle,
  Rect,
  ShapeNodeStyle,
  type INode,
} from '@yfiles/yfiles'
import licenseData from './license.json'
import {
  generateSyntheticGraph,
  PROFILE_DEFINITIONS,
  type DatasetProfile,
  type GraphNodeLevel,
  type SyntheticGraph,
} from './graph/syntheticGraphGenerator'
import {
  buildProjection,
  type GraphProjection,
  type Lod,
  type ProjectionNode,
} from './visualization/adaptiveProjection'
import { adaptiveGraphPolicy, resolveLod } from './visualization/policy'
import { measureGeometry, type GeometryMetrics } from './telemetry/geometryTelemetry'
import './styles.css'
import appShell from './app-shell.html?raw'

License.value = licenseData
LayoutExecutor.ensure()

document.querySelector<HTMLElement>('#app')!.innerHTML = appShell

const graphElement = document.querySelector<HTMLElement>('#graph-component')!
const overviewElement = document.querySelector<HTMLElement>('#overview-component')!
const graphComponent = new GraphComponent(graphElement)
const overviewComponent = new GraphOverviewComponent(overviewElement, graphComponent)
const inputMode = new GraphViewerInputMode()
inputMode.clickableItems = 'node'
graphComponent.inputMode = inputMode
graphComponent.contentMargins = [48, 48, 48, 48]
graphComponent.animatedViewportChanges = 'none'

const profileSelect = document.querySelector<HTMLSelectElement>('#dataset-profile')!
const lodSelect = document.querySelector<HTMLSelectElement>('#lod-mode')!
const fitButton = document.querySelector<HTMLButtonElement>('#fit-graph')!
const focusButton = document.querySelector<HTMLButtonElement>('#focus-selection')!
const collapseButton = document.querySelector<HTMLButtonElement>('#collapse-all')!
const refreshButton = document.querySelector<HTMLButtonElement>('#refresh-seed')!
const statusElement = document.querySelector<HTMLElement>('#status')!
const selectedElement = document.querySelector<HTMLElement>('#selected-node')!
const lodBadge = document.querySelector<HTMLElement>('#lod-badge')!
const graphSummary = document.querySelector<HTMLElement>('#graph-summary')!
const metricsElement = document.querySelector<HTMLElement>('#metrics')!
const inspectorElement = document.querySelector<HTMLElement>('#inspector')!
const zoomValue = document.querySelector<HTMLElement>('#zoom-value')!
const workspaceInstructionElement = document.querySelector<HTMLElement>('#workspace-instruction')!
const scenarioSummaryElement = document.querySelector<HTMLElement>('#scenario-summary')!
const useCaseButtons = {
  overview: document.querySelector<HTMLButtonElement>('#usecase-overview')!,
  investigate: document.querySelector<HTMLButtonElement>('#usecase-investigate')!,
  stress: document.querySelector<HTMLButtonElement>('#usecase-stress')!,
}

interface Position {
  x: number
  y: number
}

type UseCase = 'overview' | 'investigate' | 'stress' | 'custom'

const LOD_LABELS: Record<Lod, string> = {
  macro: '全体',
  group: '関係',
  entity: '詳細',
  focus: '注目',
}

const LEVEL_LABELS: Record<GraphNodeLevel, string> = {
  cluster: 'クラスタ',
  group: 'グループ',
  leaf: 'ノード',
}

const USE_CASE_LABELS: Record<UseCase, string> = {
  overview: '全体像を見る',
  investigate: '1つを掘り下げる',
  stress: '大量データを試す',
  custom: 'カスタム設定',
}

const COLORS = {
  cluster: { fill: '#0f766e', stroke: '#5eead4', text: '#ecfeff' },
  group: { fill: '#4338ca', stroke: '#a5b4fc', text: '#eef2ff' },
  leaf: { fill: '#dbeafe', stroke: '#60a5fa', text: '#172554' },
  context: { fill: '#cbd5e1', stroke: '#94a3b8', text: '#475569' },
  selected: { fill: '#f59e0b', stroke: '#fde68a', text: '#451a03' },
}

function levelSize(level: GraphNodeLevel, context: boolean): { width: number; height: number } {
  if (context) return { width: 44, height: 24 }
  if (level === 'cluster') return { width: 152, height: 58 }
  if (level === 'group') return { width: 112, height: 42 }
  return { width: 82, height: 32 }
}

function nodeColor(level: GraphNodeLevel, context: boolean, selected: boolean) {
  if (selected) return COLORS.selected
  if (context) return COLORS.context
  return COLORS[level]
}

function formatNodeLabel(node: ProjectionNode, lod: Lod): string {
  if (lod === 'macro' && node.level === 'cluster') {
    return `${node.label}\n${node.leafCount} nodes`
  }
  if (node.level !== 'leaf') {
    return `${node.label}\n${node.leafCount} nodes`
  }
  return node.label
}

function edgeOpacity(depth: number, lod: Lod): number {
  if (lod !== 'focus') return lod === 'macro' ? 0.58 : 0.72
  if (depth === 0) return 1
  if (depth === 1) return 0.86
  if (depth === 2) return adaptiveGraphPolicy.edge.twoHopOpacity
  return adaptiveGraphPolicy.edge.contextOpacity
}

function edgeColor(depth: number, lod: Lod): string {
  if (depth === 0) return '#f59e0b'
  if (lod !== 'focus') return '#64748b'
  if (depth === 1) return '#38bdf8'
  if (depth === 2) return '#64748b'
  return '#475569'
}

function withAlpha(hex: string, opacity: number): string {
  const alpha = Math.round(Math.max(0, Math.min(1, opacity)) * 255)
    .toString(16)
    .padStart(2, '0')
  return `${hex}${alpha}`
}

class AdaptiveGraphController {
  private graphData: SyntheticGraph
  private projection: GraphProjection = { nodes: [], edges: [], visibleSourceIds: new Set() }
  private profile: DatasetProfile = 'S'
  private lod: Lod = 'macro'
  private lodMode: 'auto' | Lod = 'auto'
  private scenario: UseCase = 'overview'
  private selectedId: string | null = null
  private expandedClusters = new Set<string>()
  private expandedGroups = new Set<string>()
  private previousPositions = new Map<string, Position>()
  private previousSelectedCenter: Position | null = null
  private renderQueue = Promise.resolve()
  private useFreshLayout = true
  private metrics: GeometryMetrics = {
    nodeOverlapCount: 0,
    edgeNodeIntersectionCount: 0,
    visibleNodeCount: 0,
    visibleEdgeCount: 0,
    viewportOccupancy: 0,
    selectedNodeDisplacement: 0,
  }
  private renderVersion = 0

  constructor() {
    this.graphData = generateSyntheticGraph(this.profile)
  }

  async initialize(): Promise<void> {
    await this.enqueueRender(false)
    graphComponent.fitGraphBounds()
    this.updateUi()
  }

  async setProfile(profile: DatasetProfile): Promise<void> {
    this.scenario = 'custom'
    await this.resetGraph(profile, 'auto')
  }

  async applyUseCase(useCase: Exclude<UseCase, 'custom'>): Promise<void> {
    this.scenario = useCase
    this.updateUi()
    if (useCase === 'overview') {
      await this.resetGraph('S', 'macro')
      return
    }
    if (useCase === 'investigate') {
      await this.resetGraph('S', 'auto')
      await this.focusSelection()
      return
    }
    await this.resetGraph('M', 'auto')
  }

  private async resetGraph(profile: DatasetProfile, mode: 'auto' | Lod): Promise<void> {
    this.profile = profile
    this.graphData = generateSyntheticGraph(profile)
    this.lod = mode === 'auto' ? 'macro' : mode
    this.lodMode = mode
    this.selectedId = null
    this.expandedClusters.clear()
    this.expandedGroups.clear()
    this.previousPositions.clear()
    this.useFreshLayout = true
    await this.enqueueRender(false)
    graphComponent.fitGraphBounds()
    profileSelect.value = profile
    lodSelect.value = mode
    this.updateUi()
  }

  async setLodMode(mode: 'auto' | Lod): Promise<void> {
    this.scenario = 'custom'
    this.lodMode = mode
    if (mode !== 'auto') {
      this.lod = mode
      this.ensureExpansionForLod()
      await this.enqueueRender(true)
      graphComponent.fitGraphBounds()
    }
    this.updateUi()
  }

  async handleNode(nodeTag: ProjectionNode, doubleClick: boolean): Promise<void> {
    this.selectedId = nodeTag.sourceId
    this.previousSelectedCenter = this.getSelectedNodeCenter()
    if (doubleClick) {
      if (nodeTag.level === 'cluster') {
        if (this.expandedClusters.has(nodeTag.sourceId)) {
          this.expandedClusters.delete(nodeTag.sourceId)
        } else {
          this.expandedClusters.add(nodeTag.sourceId)
        }
        this.lod = this.lod === 'macro' ? 'group' : this.lod
      } else if (nodeTag.level === 'group') {
        if (this.expandedGroups.has(nodeTag.sourceId)) {
          this.expandedGroups.delete(nodeTag.sourceId)
        } else {
          this.expandedGroups.add(nodeTag.sourceId)
        }
        this.expandedClusters.add(nodeTag.clusterId)
        this.lod = this.lod === 'macro' || this.lod === 'group' ? 'entity' : this.lod
      } else {
        this.lod = 'focus'
        this.expandedClusters.add(nodeTag.clusterId)
        if (nodeTag.groupId) this.expandedGroups.add(nodeTag.groupId)
      }
      this.lodMode = this.lod
      lodSelect.value = this.lod
    }
    await this.enqueueRender(true)
    if (doubleClick) {
      graphComponent.fitGraphBounds()
    }
  }

  async focusSelection(): Promise<void> {
    this.scenario = 'investigate'
    let selected = this.graphData.nodes.get(this.selectedId ?? '')
    if (!selected || selected.level !== 'leaf') {
      const firstLeaf = [...this.graphData.nodes.values()].find(
        (node) => node.level === 'leaf' && (!selected || node.clusterId === selected.clusterId),
      )
      this.selectedId = firstLeaf?.id ?? this.graphData.leafIds[0] ?? null
      selected = this.graphData.nodes.get(this.selectedId ?? '')
    }
    if (selected) {
      this.expandedClusters.add(selected.clusterId)
      if (selected.groupId) this.expandedGroups.add(selected.groupId)
    }
    this.lod = 'focus'
    this.lodMode = 'focus'
    lodSelect.value = 'focus'
    await this.enqueueRender(true)
    this.zoomSelectedNode()
  }

  async collapseAll(): Promise<void> {
    this.expandedClusters.clear()
    this.expandedGroups.clear()
    this.selectedId = null
    this.lod = 'macro'
    this.lodMode = 'auto'
    this.useFreshLayout = true
    await this.enqueueRender(true)
    graphComponent.fitGraphBounds()
  }

  async refreshSeed(): Promise<void> {
    this.graphData = generateSyntheticGraph(this.profile, this.graphData.seed + 1)
    this.selectedId = null
    this.expandedClusters.clear()
    this.expandedGroups.clear()
    this.lod = 'macro'
    this.useFreshLayout = true
    await this.enqueueRender(false)
    graphComponent.fitGraphBounds()
  }

  handleZoomChanged(): void {
    zoomValue.textContent = `${graphComponent.zoom.toFixed(2)}×`
    if (this.lodMode === 'auto') {
      const nextLod = resolveLod(this.lod, graphComponent.zoom)
      if (nextLod !== this.lod) {
        this.lod = nextLod
        this.ensureExpansionForLod()
        void this.enqueueRender(true)
      }
    }
    this.updateUi()
  }

  private ensureExpansionForLod(): void {
    const selected = this.graphData.nodes.get(this.selectedId ?? '')
    if (this.lod === 'group' || this.lod === 'entity' || this.lod === 'focus') {
      this.expandedClusters.add(selected?.clusterId ?? this.graphData.clusterIds[0])
    }
    if (this.lod === 'entity' || this.lod === 'focus') {
      const groupId = selected?.groupId ?? this.graphData.groupIds[0]
      if (groupId) this.expandedGroups.add(groupId)
    }
  }

  private getSelectedNodeCenter(): Position | null {
    if (!this.selectedId) return null
    const node = [...graphComponent.graph.nodes].find(
      (candidate) => (candidate.tag as ProjectionNode | undefined)?.sourceId === this.selectedId,
    )
    return node ? { x: node.layout.center.x, y: node.layout.center.y } : null
  }

  private async render(animate: boolean): Promise<void> {
    const version = ++this.renderVersion
    this.capturePositions()
    const previousProjection = this.projection
    this.projection = buildProjection(
      this.graphData,
      this.lod,
      this.expandedClusters,
      this.expandedGroups,
      this.selectedId,
    )
    const graph = graphComponent.graph
    const positionsBeforeRender = new Map(this.previousPositions)
    const collapsedPositions = new Map<string, Position>()
    const collapsedPositionCounts = new Map<string, number>()
    for (const previousNode of previousProjection.nodes) {
      const position = positionsBeforeRender.get(previousNode.id)
      const parentId = previousNode.level === 'leaf'
        ? previousNode.groupId
        : previousNode.level === 'group'
          ? previousNode.clusterId
          : null
      if (!position || !parentId) continue
      const current = collapsedPositions.get(parentId) ?? { x: 0, y: 0 }
      const count = collapsedPositionCounts.get(parentId) ?? 0
      collapsedPositions.set(parentId, {
        x: (current.x * count + position.x) / (count + 1),
        y: (current.y * count + position.y) / (count + 1),
      })
      collapsedPositionCounts.set(parentId, count + 1)
    }
    const siblingsByAnchor = new Map<string, ProjectionNode[]>()
    for (const nodeProjection of this.projection.nodes) {
      if (!nodeProjection.anchorId) continue
      const siblings = siblingsByAnchor.get(nodeProjection.anchorId) ?? []
      siblings.push(nodeProjection)
      siblingsByAnchor.set(nodeProjection.anchorId, siblings)
    }
    graph.clear()
    graph.nodeDefaults.labels.style = new LabelStyle({
      font: '12px Segoe UI',
      textFill: '#0f172a',
      padding: [3, 6],
    })
    graph.edgeDefaults.labels.style = new LabelStyle({
      font: '11px Segoe UI',
      textFill: '#e2e8f0',
      backgroundFill: '#07111fcc',
      padding: [2, 4],
    })

    const nodeMap = new Map<string, INode>()
    const incrementalNodeIds = new Set(
      this.projection.nodes
        .filter((nodeProjection) => !positionsBeforeRender.has(nodeProjection.id))
        .map((nodeProjection) => nodeProjection.id),
    )
    for (const [index, nodeProjection] of this.projection.nodes.entries()) {
      const context = this.lod === 'focus' && nodeProjection.focusDepth >= 3
      const selected = nodeProjection.sourceId === this.selectedId
      const size = levelSize(nodeProjection.level, context)
      const color = nodeColor(nodeProjection.level, context, selected)
      const storedPosition = positionsBeforeRender.get(nodeProjection.id)
      const collapsedPosition = collapsedPositions.get(nodeProjection.id)
      const anchorPosition = nodeProjection.anchorId
        ? positionsBeforeRender.get(nodeProjection.anchorId)
        : undefined
      const siblings = nodeProjection.anchorId ? siblingsByAnchor.get(nodeProjection.anchorId) ?? [] : []
      const siblingIndex = siblings.findIndex((sibling) => sibling.id === nodeProjection.id)
      const position = storedPosition ?? collapsedPosition ?? (anchorPosition && siblingIndex >= 0
        ? {
            x: anchorPosition.x + (nodeProjection.level === 'leaf' ? 120 : 138),
            y: anchorPosition.y + (siblingIndex - (siblings.length - 1) / 2) *
              (nodeProjection.level === 'leaf' ? 48 : 66),
          }
        : {
            x: (index % 7) * 180,
            y: Math.floor(index / 7) * 110,
          })
      const node = graph.createNode({
        layout: new Rect(position.x - size.width / 2, position.y - size.height / 2, size.width, size.height),
        style: new ShapeNodeStyle({
          shape: nodeProjection.level === 'leaf' ? 'round-rectangle' : 'round-rectangle',
          fill: color.fill,
          stroke: `2px ${color.stroke}`,
        }),
        tag: nodeProjection,
        labels: [formatNodeLabel(nodeProjection, this.lod)],
      })
      graph.setStyle(node.labels.get(0), new LabelStyle({
        font: `${selected ? 13 : nodeProjection.level === 'cluster' ? 13 : 11}px Segoe UI`,
        textFill: color.text,
        padding: [3, 6],
      }))
      nodeMap.set(nodeProjection.id, node)
    }

    for (const edgeProjection of this.projection.edges) {
      const source = nodeMap.get(edgeProjection.sourceId)
      const target = nodeMap.get(edgeProjection.targetId)
      if (!source || !target) continue
      const opacity = edgeOpacity(edgeProjection.focusDepth, this.lod)
      const color = withAlpha(edgeColor(edgeProjection.focusDepth, this.lod), opacity)
      const edge = graph.createEdge({
        source,
        target,
        style: new PolylineEdgeStyle({
          stroke: `${edgeProjection.detail ? 2.4 : Math.max(1.2, Math.min(4, 1 + edgeProjection.count * 0.35))}px ${color}`,
          targetArrow: new Arrow({ type: 'triangle', fill: color, stroke: color }),
        }),
        tag: edgeProjection,
      })
      if (edgeProjection.count > 1 || this.lod === 'macro' || this.lod === 'group') {
        graph.addLabel(edge, String(edgeProjection.count))
      }
    }

    const needsLayout = this.useFreshLayout || incrementalNodeIds.size > 0
    if (needsLayout) {
      const layout = new HierarchicalLayout({
        layoutOrientation: 'left-to-right',
        nodeDistance: adaptiveGraphPolicy.layout.nodeDistance,
        minimumLayerDistance: adaptiveGraphPolicy.layout.minimumLayerDistance,
        fromSketchMode: !this.useFreshLayout,
      })
      const layoutData = layout.createLayoutData()
      if (!this.useFreshLayout) {
        layoutData.incrementalNodeHints = (node) => {
          const tag = node.tag as ProjectionNode | undefined
          return tag && incrementalNodeIds.has(tag.id)
            ? IncrementalNodeHint.INCREMENTAL_WITH_LAYERS_FROM_SKETCH
            : IncrementalNodeHint.FROM_SKETCH
        }
        layoutData.incrementalEdges = (edge) => {
          const sourceTag = edge.sourceNode.tag as ProjectionNode | undefined
          const targetTag = edge.targetNode.tag as ProjectionNode | undefined
          return Boolean(
            (sourceTag && incrementalNodeIds.has(sourceTag.id)) ||
            (targetTag && incrementalNodeIds.has(targetTag.id)),
          )
        }
      }
      await graphComponent.applyLayoutAnimated({
        layout,
        layoutData,
        animationDuration: animate ? `${adaptiveGraphPolicy.animation.expandMs}ms` : 0,
        animateViewport: false,
      })
      this.useFreshLayout = false
    }
    if (version !== this.renderVersion) return
    graph.applyLayout(new EdgeRouter({ stopDuration: '100ms', minimumNodeToEdgeDistance: 10 }))
    this.selectCurrentNode()
    this.metrics = measureGeometry(
      graphComponent,
      this.projection,
      this.getSelectedGraphNode(),
      this.previousSelectedCenter,
    )
    this.updateUi()
  }

  private enqueueRender(animate: boolean): Promise<void> {
    this.renderQueue = this.renderQueue.catch(() => undefined).then(() => this.render(animate))
    return this.renderQueue
  }

  private capturePositions(): void {
    this.previousPositions.clear()
    for (const node of graphComponent.graph.nodes) {
      const tag = node.tag as ProjectionNode | undefined
      if (tag) {
        this.previousPositions.set(tag.id, { x: node.layout.center.x, y: node.layout.center.y })
      }
    }
  }

  private getSelectedGraphNode(): INode | null {
    return (
      [...graphComponent.graph.nodes].find(
        (node) => (node.tag as ProjectionNode | undefined)?.sourceId === this.selectedId,
      ) ?? null
    )
  }

  private selectCurrentNode(): void {
    graphComponent.selection.clear()
    const selected = this.getSelectedGraphNode()
    if (selected) {
      inputMode.setSelected(selected, true)
      graphComponent.currentItem = selected
    }
  }

  private zoomSelectedNode(): void {
    const selected = this.getSelectedGraphNode()
    if (selected) {
      graphComponent.zoomTo(1.35, selected.layout.center)
    }
  }

  private updateUi(): void {
    const profile = PROFILE_DEFINITIONS[this.profile]
    const selected = this.graphData.nodes.get(this.selectedId ?? '')
    const selectedProjection = this.projection.nodes.find((node) => node.sourceId === this.selectedId)
    const selectedLevel: GraphNodeLevel = selectedProjection?.level ?? selected?.level ?? 'cluster'
    const selectedLeafCount = selectedProjection?.leafCount ?? selected?.leafCount ?? 0
    const selectedLabel = selectedProjection?.label ?? selected?.label ?? '未選択'
    const nextAction = selectedLevel === 'cluster'
      ? 'ダブルクリックでグループを表示'
      : selectedLevel === 'group'
        ? 'ダブルクリックで配下のノードを表示'
        : this.lod === 'focus'
          ? '周辺を表示中 · ダブルクリックで注目表示を切り替え'
          : '「選択したノードの周辺を見る」で周辺を表示'
    const scenarioLabel = USE_CASE_LABELS[this.scenario]
    scenarioSummaryElement.textContent = scenarioLabel
    focusButton.textContent = selected ? '選択したノードの周辺を見る' : '最初のノードを掘り下げる'
    lodSelect.value = this.lodMode
    Object.entries(useCaseButtons).forEach(([key, button]) => {
      button.classList.toggle('is-active', key === this.scenario)
    })
    statusElement.textContent = `${scenarioLabel} · ${this.lodMode === 'auto' ? '自動' : '固定'} · seed ${this.graphData.seed}`
    lodBadge.textContent = `LOD ${LOD_LABELS[this.lod]}`
    selectedElement.textContent = selected?.label ?? '未選択'
    graphSummary.textContent = `クラスタ ${profile.clusters} · グループ ${profile.clusters * profile.groupsPerCluster} · ノード ${profile.clusters * profile.groupsPerCluster * profile.leavesPerGroup}`
    zoomValue.textContent = `${graphComponent.zoom.toFixed(2)}×`
    if (selected) {
      const visibility = selectedProjection ? '現在の表示にあります' : '親ノードとしてまとめて表示中'
      inspectorElement.innerHTML = `<div class="inspector-title">選択中</div><strong>${selectedLabel}</strong><span>${LEVEL_LABELS[selectedLevel]} · 配下 ${selectedLeafCount} ノード</span><span>状態: ${visibility}</span><span>注目深度: ${selectedProjection?.focusDepth ?? '-'} </span><span class="inspector-next">次の操作: ${nextAction}</span>`
    } else {
      inspectorElement.innerHTML = `<div class="inspector-title">ここに表示されます</div><strong>ノードをクリックしてください</strong><span>選択したノードの種類、配下の数、次にできる操作を表示します。</span><span class="inspector-next">ヒント: ダブルクリックで階層を開けます。</span>`
    }
    const instruction = !selected
      ? 'ノードをクリックすると、右側に詳細が表示されます'
      : selectedLevel === 'cluster'
        ? `${selectedLabel}を選択中 · ダブルクリックでグループを表示`
        : selectedLevel === 'group'
          ? `${selectedLabel}を選択中 · ダブルクリックでノードを表示`
          : this.lod === 'focus'
            ? `${selectedLabel}を注目中 · ダブルクリックで注目表示を切り替え`
            : `${selectedLabel}を選択中 · 「選択したノードの周辺を見る」で周辺を表示`
    workspaceInstructionElement.textContent = instruction
    metricsElement.innerHTML = [
      ['見えているノード', this.metrics.visibleNodeCount],
      ['見えているエッジ', this.metrics.visibleEdgeCount],
      ['ノードの重なり', this.metrics.nodeOverlapCount],
      ['エッジの交差', this.metrics.edgeNodeIntersectionCount],
      ['画面の占有率', `${Math.round(this.metrics.viewportOccupancy * 100)}%`],
      ['選択位置の変化', this.metrics.selectedNodeDisplacement.toFixed(3)],
    ]
      .map(([label, value]) => `<div class="metric"><span>${label}</span><strong>${value}</strong></div>`)
      .join('')
  }
}

const controller = new AdaptiveGraphController()
let pendingNodeClick: number | null = null
let suppressNodeClicksUntil = 0

inputMode.addEventListener('item-clicked', (event) => {
  const node = event.item as INode | null
  const tag = node?.tag as ProjectionNode | undefined
  if (!tag) return
  if (Date.now() < suppressNodeClicksUntil) return
  if (pendingNodeClick !== null) window.clearTimeout(pendingNodeClick)
  pendingNodeClick = window.setTimeout(() => {
    pendingNodeClick = null
    void controller.handleNode(tag, false)
  }, 220)
})

inputMode.addEventListener('item-left-double-clicked', (event) => {
  const node = event.item as INode | null
  const tag = node?.tag as ProjectionNode | undefined
  if (!tag) return
  suppressNodeClicksUntil = Date.now() + 400
  if (pendingNodeClick !== null) {
    window.clearTimeout(pendingNodeClick)
    pendingNodeClick = null
  }
  event.handled = true
  window.setTimeout(() => void controller.handleNode(tag, true), 0)
})

graphComponent.addEventListener('zoom-changed', () => controller.handleZoomChanged())

profileSelect.addEventListener('change', () => {
  void controller.setProfile(profileSelect.value as DatasetProfile)
})
lodSelect.addEventListener('change', () => {
  void controller.setLodMode(lodSelect.value as 'auto' | Lod)
})
fitButton.addEventListener('click', () => graphComponent.fitGraphBounds())
focusButton.addEventListener('click', () => void controller.focusSelection())
collapseButton.addEventListener('click', () => void controller.collapseAll())
refreshButton.addEventListener('click', () => void controller.refreshSeed())
useCaseButtons.overview.addEventListener('click', () => void controller.applyUseCase('overview'))
useCaseButtons.investigate.addEventListener('click', () => void controller.applyUseCase('investigate'))
useCaseButtons.stress.addEventListener('click', () => void controller.applyUseCase('stress'))

void controller.initialize()

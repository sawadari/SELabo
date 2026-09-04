# 実験4：Adaptive Graph Visualization

Synthetic Graphを対象に、yFiles for HTMLで階層的なグラフ投影、Semantic Zoom、Focus表示、エッジ可読性を検証する実験です。

## 実装範囲

- yFiles `GraphComponent`、`GraphOverviewComponent`、`HierarchicalLayout`、`EdgeRouter`
- XS / S / M の決定的なSynthetic Graph生成（既定はS、seed変更可能）
- Macro / Group / Entity / Focusの4段階LOD
- Auto LODのヒステリシス閾値（拡大時と縮小時で閾値を分離）
- クラスタ・グループ・リーフのクリック選択とダブルクリック展開／折りたたみ
- エッジ集約、Focus深度に応じた太さ・透明度・ラベル表示
- ノード重なり、エッジとノードの交差、表示数、viewport coverage、選択ノード移動量の計測

## 起動

```powershell
cd experiments/adaptive-graph-visualization
npm install
npm run dev
```

ブラウザで表示されたURLを開きます。ビルド確認は次のコマンドです。

```powershell
npm run build
```

## 画面の使い方

画面左の「まず試す」から目的を選ぶと、目的に合ったデータ量と表示レベルで開始できます。

- `全体像を見る`：クラスタ同士のつながりを確認します。
- `1つを掘り下げる`：最初のノードを選択し、その周辺をFocus表示します。
- `大量データを試す`：Mサイズのデータでレイアウトと可読性を確認します。

グラフ上では、ノードをクリックすると右側に詳細が表示されます。ダブルクリックでクラスタ、グループ、ノードの階層を順に開きます。展開時は、表示中のノード同士の相対関係を保ちながら、新しい要素のために必要な範囲だけ周囲を再配置します。マウスホイールでAuto LODの表示レベルを切り替えられ、表示レベルやデータ量を細かく変更したい場合は、左側の「詳細設定」を開いてください。

## yFilesの導入

この実験は、公開npmレジストリのプレースホルダではなく、yFiles Dev Suiteから取得した評価版パッケージを使用します。

1. `npx --yes yfiles-dev-suite login` でログインします。
2. `npx --yes yfiles-dev-suite ui` を起動し、yFiles for HTMLの評価版をダウンロードします。
3. 取得したtarballを `yfiles/yfiles-31.0.2+eval-dev.tgz` として置き、`npm install --save .\yfiles\yfiles-31.0.2+eval-dev.tgz` を実行します。
4. 評価版フォルダーの `lib/license.json` を `src/license.json` にコピーします。

`yfiles/` と `src/license.json` はライセンス上の理由でGit管理対象外です。評価版では画面に評価ウォーターマークが表示されます。製品利用時は、契約済みライセンスに置き換え、ライセンスファイルをリポジトリへ公開しないでください。

## 確認手順

1. `全体像を見る` を選び、`LOD 全体` と5クラスタの表示を確認します。
2. グラフ上の `Cluster A` をダブルクリックし、`LOD 関係` へ展開します。
3. 表示されたグループをダブルクリックし、`LOD 詳細` へ展開します。
4. ノードをクリックして、右側のInspectorに選択情報が表示されることを確認します。
5. `選択したノードの周辺を見る` を押し、`LOD 注目` で周辺ノードが表示されることを確認します。
6. `大量データを試す` を選び、Mサイズ（640ノード）のレイアウト負荷を確認します。

## 未実装・制約

- 現在の入力データはSynthetic Graphのみです。実際のSysML、要求、設計データとの接続は次段階です。
- yFilesの評価ライセンスを使用しているため、評価期間と利用条件はDev Suiteの契約に従います。
- geometry metricsはPoC用の軽量計測です。大規模データの性能評価では別途ベンチマークを追加します。

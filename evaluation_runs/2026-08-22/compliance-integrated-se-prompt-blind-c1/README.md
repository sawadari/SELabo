# C1-blind参考run（効果判定から除外）

このdirectoryは、既存評価ファイルを読ませずに同じ製品担当サブエージェントを再利用した途中runである。担当履歴自体は隔離できないため、厳密なblind条件を満たさない。

- スマート扇風機と懐中電灯の出力は参考記録として保持する。
- モバイルバッテリーは最小モデルへ移行する前に中断したため、入力だけを保持する。
- 件数、Gate、Compliance Layerの効果判定には使用しない。

履歴を引き継がない新規サブエージェントによる正本評価は、[strict C1-blind](../compliance-integrated-se-prompt-blind-c1-strict/README.md)を参照する。

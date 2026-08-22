# Applicability and Obligation Register

## Normative Statement

| ID | Provision | 種別 | 様相 | 主体 | 条件 | 行為／性質 | 対象 | 限界 | 解釈状態 |
|---|---|---|---|---|---|---|---|---|---|
| NRM-DENAN-0001 | PRV-DENAN-0001 | normative | obligation | 届出事業者候補 | 構成品がDENAN対象電気用品である場合 | 対象電気用品を技術上の基準に適合させる | 対象電気用品 | — | ai_candidate |
| NRM-CSPSA-0001 | PRV-CSPSA-0001 | normative | obligation | 消費生活用製品の製造または輸入事業者候補 | 重大製品事故が発生したことを知った場合 | 消費者庁へ報告する | 重大製品事故情報 | 10日以内との公式説明 | ai_candidate |

## Applicability Assessment（適用性評価コンテキスト・判断候補・拘束根拠・再評価トリガー）

| ID | Normative Statement | コンテキスト | 判断候補 | 拘束根拠 | 理由 | 人確認状態 | 確認者 | 確認日時 | 再評価トリガー |
|---|---|---|---|---|---|---|---|---|---|
| APP-DENAN-0001 | NRM-DENAN-0001 | {'jurisdiction': '日本（探索仮定）', 'market': '日本の一般消費者市場（探索仮定）', 'product_classification': '携帯照明。電池・充電構成未決定', 'intended_use': '成人が暗所を一時的に照らす', 'configuration_ref': 'CFG-0001', 'lifecycle_stage': 'development'} | uncertain | direct_regulation | リチウムイオン蓄電池と直流電源装置は候補だが、電池仕様、同梱構成、販売単位、事業者役割が不明。 | pending | — | — | 市場決定<br>電池BOM決定<br>充電器同梱決定<br>製造輸入主体決定<br>原典改正 |
| APP-CSPSA-0001 | NRM-CSPSA-0001 | {'jurisdiction': '日本（探索仮定）', 'market': '日本の一般消費者市場（探索仮定）', 'product_classification': '一般消費者向け携帯照明候補', 'intended_use': '成人が暗所を一時的に照らす', 'configuration_ref': 'CFG-0001', 'lifecycle_stage': 'operation'} | uncertain | direct_regulation | 一般消費者用途は候補だが、法上の製品該当性、除外、製造輸入主体が未確認。 | pending | — | — | 市場・用途変更<br>製造輸入主体決定<br>対象除外または報告制度改正 |

## Obligation

| ID | 種別 | 義務主体候補 | 対象 | 条件 | 必要結果 | 状態 |
|---|---|---|---|---|---|---|
| OBL-DENAN-0001 | mandatory | 届出事業者候補 | CFG-0001中のDENAN対象構成品候補 | APP-DENAN-0001を権限者が適用ありと確認した場合 | 対象構成品が人により確定した技術基準に適合する | candidate |
| OBL-CSPSA-0001 | mandatory | 日本の製造または輸入事業者候補 | 重大製品事故の識別・報告プロセス | 適用性を権限者が確認し、重大製品事故を知った場合 | 人が確定した期限と手続で消費者庁へ報告する | candidate |

## 人の確認バックログ

- APP-DENAN-0001: リチウムイオン蓄電池と直流電源装置は候補だが、電池仕様、同梱構成、販売単位、事業者役割が不明。
- APP-CSPSA-0001: 一般消費者用途は候補だが、法上の製品該当性、除外、製造輸入主体が未確認。

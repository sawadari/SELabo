# ACC-0001 / VER-0001 の投影。これは候補初稿であり、実施済み・合格済み・受入済みを示さない。
# 正本参照: 10_se_model.json（物理入力: representative_model.json）

Feature: 保全依頼受付の受入条件
  # acceptance_criteria.id: ACC-0001
  # requirement_refs: REQ-0001
  # verification_refs: VER-0001
  # pass_rule: VER-0001が合格すること
  Scenario: 有効な保全依頼を送信したとき受付結果が表示される
    Given 利用者が保全依頼登録画面を利用できる
    When 有効な保全依頼を送信する
    Then 受付結果が表示される
    And VER-0001が合格すること

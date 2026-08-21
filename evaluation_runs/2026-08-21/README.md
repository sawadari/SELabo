# 3製品のQ&A評価実行

## 目的

`hierarchical-se-prompt`を、スマート扇風機、懐中電灯、モバイルバッテリーの3製品に適用し、Q&Aから40点初稿候補へ移る流れを確認する実験です。

第三者向けに、会話からどのような初稿と課題が得られたかを物語形式で説明したHTMLも用意しています。

- [第三者向けストーリー説明（HTML）](third_party_story.html)

## 実行方法

1. 製品ごとに、目的、利用者、使用環境、重視点、制約、未確定事項をQ&Aで整理する。
2. Q&Aの回答を、`01_CORE_PROMPT.md`と設定・Schemaと一緒に使う。
3. 生成物を、生成担当とは別のサブエージェントが`17_FORTY_POINT_GATE.md`と`18_AI_EVALUATION_PROTOCOL.md`で評価する。

今回のQ&Aは実際の製品担当者への聞き取りではなく、評価手順をそろえるための合成入力です。したがって、Q&Aの内容を`user_confirmed`や`baselined`へ昇格させません。

## 製品別ファイル

- [スマート扇風機](smart-fan/chat_and_candidate.md)
- [懐中電灯](flashlight/chat_and_candidate.md)
- [モバイルバッテリー](mobile-battery/chat_and_candidate.md)

## 評価結果

独立評価サブエージェントの判定は、3製品とも`below_reviewable`でした。主な共通Findingは、Traceが参照するNeed IDの未定義と、Behavior／Structure／V&V候補への由来・状態属性の不足です。

- [スマート扇風機の独立レビュー](smart-fan/independent_review.md)：安全停止、静音条件、通信断の確認が必要
- [懐中電灯の独立レビュー](flashlight/independent_review.md)：低電池時の突然消灯、過熱、環境条件の確認が必要
- [モバイルバッテリーの独立レビュー](mobile-battery/independent_review.md)：充電側保護、電池異常、輸送・法規Traceの確認が必要

完全なBundle／ZIP、JSON Schema検証、SysMLツール検証、実機試験、法規確認は、この実行の範囲外です。

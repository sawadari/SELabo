# 参考資料と設計判断の関係

## この文書の目的

この文書は、プロンプト内の考え方が何を参考にしているかを説明します。

ただし、このプロンプトが国際規格や業界規格へ正式に適合していると証明する文書ではありません。L0～L7という区分、40点初稿、ZIPでの出力などは、この実験で考えた方法です。

## 参考資料の種類

参考資料を、次の四つに分けています。

| 種類 | 何を表すか | 使い方 |
|---|---|---|
| A | 国際規格、国内規格、正式仕様 | 用語や基本的な考え方の根拠にする |
| B | 公的機関や専門団体のハンドブック | 実務での進め方や確認方法の参考にする |
| C | 論文や専門書 | 文章パターンや問題の見つけ方の参考にする |
| D | この実験独自の判断 | 一回実行、40点初稿、ファイル構成などに使う |

Aの資料に基づく項目でも、このプロンプトだけで規格適合になるわけではありません。

## 1. SE全体の流れ

### 参考にした資料

- ISO/IEC/IEEE 15288:2023
- INCOSE Systems Engineering Handbook, Fifth Edition
- NASA Systems Engineering Handbook

### プロンプトへ取り入れたこと

- 利害関係者、ニーズ、要求、設計、試験をつなげる。
- システムの企画から廃棄までを考える。
- システム全体だけでなく、構成要素にも同じ考え方を使えるようにする。
- 機械とソフトウェアだけでなく、人、データ、手順、設備、材料も扱う。
- リスク、意思決定、変更を記録する。

### 注意

ISO/IEC/IEEE 15288は、L0～L7という階層を定めていません。L0～L7は、この実験で情報を整理しやすくするための順番です。

## 2. ニーズと要求

### 参考にした資料

- ISO/IEC/IEEE 29148:2018
- INCOSE Guide for Writing Requirements, Version 4
- NASA Systems Engineering Handbook
- Pohl and Rupp, Requirements Engineering Fundamentals
- Wiegers and Beatty, Software Requirements

### プロンプトへ取り入れたこと

- 利害関係者が望むことを「ニーズ」とする。
- システムが満たすことを「要求」とする。
- 要求ごとに、理由、情報源、上位のニーズ、確認方法を残す。
- 一つの要求へ、別々の義務を詰め込みすぎない。
- 誰が責任を持つ要求かを明記する。
- 数値には単位、範囲、許容差を付ける。
- 曖昧な要求を、削除せず問題として残す。

### 注意

要求文が読みやすいだけでは、良い要求とは限りません。必要性、実現可能性、試験方法、他の要求との矛盾も確認する必要があります。

## 3. 要求文の形と曖昧表現

### 参考にした資料

- MavinほかによるEARS
- Femmerほかによるrequirements smellsの研究
- Cockburn, Writing Effective Use Cases

### プロンプトへ取り入れたこと

- 条件、出来事、主体、動作を分けて書く。
- `適切に`、`迅速に`、`必要に応じて`など、判断基準が分からない言葉を検出する。
- `など`や`その他`のように、範囲が決まらない列挙を避ける。
- ユースケース名を、画面操作や内部処理ではなく、利用者が達成する目的で付ける。

EARSの英語表現をそのまま訳すのではなく、日本語でも意味が分かる形へ変えています。

## 4. 設計を誰にどう見せるか

### 参考にした資料

- ISO/IEC/IEEE 42010:2022

### プロンプトへ取り入れたこと

- システムの設計そのものと、設計を説明する文書や図を分ける。
- 図ごとに、見る人、目的、答えたい質問を決める。
- 図へ表示するものと、省略するものを決める。

SysMLの図の種類を選ぶだけでは、読み手の疑問に答えられる図にはなりません。

## 5. SysML 1.x

### 参考にした資料

- OMG Systems Modeling Language Version 1.7
- OMG Unified Modeling Language Version 2.5.1
- NASA Systems Modeling Handbook for Systems Engineering

### プロンプトへ取り入れたこと

- 要求、構造、動作、状態、接続、試験をSysML 1.xへ対応付ける。
- 中心となるSEモデルJSONを正本とし、SysML仕様をその表示先の一つとする。
- 利害関係者、ニーズ、リスク、判断などを、SysML標準要素だと決めつけない。
- 必要な場合は、独自ステレオタイプの候補として分ける。ステレオタイプとは、モデル要素を目的別に分類し、追加情報を持たせる仕組みです。

### 注意

XMIは、モデリングツール間でデータを交換するための形式です。ツールやバージョンによって違いがあるため、ツールが決まっていない状態では、直接読み込めるモデルファイルを保証しません。

## 6. 日本語技術文書

### 参考にした資料

- JIS Z 8301:2019
- ISO/IEC Directives, Part 2
- 文化庁「公用文作成の考え方」
- BIPM SI Brochure
- JTF日本語標準スタイルガイド

### プロンプトへ取り入れたこと

- 必須、禁止、推奨、許可、能力を区別する。
- 注記、理由、例へ、必須要求を隠さない。
- 主語と述語を対応させる。
- 用語、数字、単位の書き方をそろえる。

### この実験独自の判断

- ニーズは、基本的に`～したい`と書く。
- システム要求は、基本的に`～する`と書き、`normative_level`で必須かどうかを示す。
- 契約文書などでは、必要に応じて`～しなければならない`へ切り替える。
- 機能名は、`対象を動詞の辞書形`で付ける。

これらは、JISやISOが唯一の正解として定めた命名方法ではありません。

## 7. AIへの指示と品質管理

### 参考にした資料

- OpenAI Prompt engineering guide
- OpenAIのカスタムGPT向け指示作成ガイド
- Whiteほか, A Prompt Pattern Catalog
- Reynolds and McDonell, Prompt Programming for Large Language Models
- JSON Schema
- NIST AI RMF 1.0とGenerative AI Profile

### プロンプトへ取り入れたこと

- 目的、入力、優先順位、手順、出力を分けて書く。
- AIの推測を、人が確認した事実と分ける。
- 同じ情報を複数文書で別々に作らず、一つのJSONから作る。
- AIの内部思考や反復回数ではなく、完成したファイルを検査する。
- できなかった検査を、実施済みと書かない。

## 8. 40点Gateと独立評価

今回の調査を受け、生成後の評価を別レイヤとして追加しました。

- `40点`を採点値ではなく、`below_reviewable`、`reviewable_40_candidate`、`overspecified_beyond_40`のGateにする。
- 根拠のない高影響数値、未管理の重大矛盾、承認済みと誤表示したAI推測をHard Blockerにする。
- GeneratorとReviewerを分け、複数Reviewerは議論ではなく独立Findingを作り、Meta-Judgeが統合する。
- 日本語の文章品質と、要求の意味的妥当性を別の評価軸にする。
- 人は作成者の代わりではなく、Decision AuthorityとValidation Authorityとして承認を行う。

この判断は、LLMの自己評価にある偏りと、要求生成の品質が文脈に依存するという調査結果を、SELaboの実験で測定可能な形にしたものです。`17_FORTY_POINT_GATE.md`、`18_AI_EVALUATION_PROTOCOL.md`、`19_EXPERIMENT_PLAN.md`に手順を分けています。

## 9. 参照情報の更新

ISO/IEC/IEEE 29148:2018は、[ISOの標準ページ](https://www.iso.org/standard/72089.html)でstatusを確認してください。調査時点では「International Standard to be revised」と表示されていました。改訂後の要求工学規則を、この実験のルールが自動的に満たすとは解釈しません。

ChatGPTのGPT作成・共有・公開条件は、アカウント種別とワークスペース権限で変わります。配布時は[OpenAI Help Centerの共有・公開ガイド](https://help.openai.com/en/articles/8798878)を確認してください。

## 主な参考文献

### 規格と正式仕様

1. [ISO/IEC/IEEE 15288:2023](https://www.iso.org/standard/81702.html)
2. [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html)
3. [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html)
4. ISO/IEC/IEEE 24765:2017
5. [OMG SysML 1.7](https://www.omg.org/spec/SysML/1.7/About-SysML)
6. [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/About-UML)
7. JIS Z 8301:2019
8. [ISO/IEC Directives, Part 2](https://www.iso.org/sites/directives/current/part2/index.xhtml)
9. [BIPM SI Brochure](https://www.bipm.org/en/publications/si-brochure)

### ハンドブックと公的ガイド

10. INCOSE Systems Engineering Handbook, Fifth Edition, 2023
11. INCOSE Guide for Writing Requirements, Version 4, 2023
12. [NASA Systems Engineering Handbook](https://ntrs.nasa.gov/citations/20170001761)
13. 文化庁「公用文作成の考え方」, 2022
14. JTF日本語標準スタイルガイド
15. NIST AI Risk Management Framework 1.0
16. NIST AI 600-1, Generative AI Profile

### 論文と専門書

17. Mavinほか, Easy Approach to Requirements Syntax, 2009
18. Femmerほか, Rapid quality assurance with requirements smells, 2017
19. Cockburn, Writing Effective Use Cases, 2000
20. Pohl and Rupp, Requirements Engineering Fundamentals, 2015
21. Wiegers and Beatty, Software Requirements, 2013
22. Whiteほか, A Prompt Pattern Catalog, 2023
23. Reynolds and McDonell, Prompt Programming for Large Language Models, 2021

### OpenAI公式資料

24. [Prompt engineering](https://platform.openai.com/docs/guides/prompt-engineering)
25. [Key guidelines for writing instructions for custom GPTs](https://help.openai.com/en/articles/9358033-key-guidelines-for-writing-instructions-for-custom-gpts)
26. [Creating a GPT](https://help.openai.com/en/articles/8554397-creating-a-gpt)
27. [Building and publishing a GPT](https://help.openai.com/en/articles/8798878-building-and-publishing-a-gpt)
28. [Apps SDK documentation](https://developers.openai.com/apps-sdk/)
29. [Apps SDK submission documentation](https://developers.openai.com/apps-sdk/deploy/submission)

## 利用時の注意

- 規格への適合確認には、組織が正規に入手した最新版を使ってください。
- 自動車、航空、医療、鉄道などでは、その分野の規格も追加で必要です。
- AIの出力はレビュー候補であり、安全認証、契約合意、設計承認の代わりにはなりません。
- 自然言語の検査だけでは、数値の妥当性や物理的な実現可能性を確認できません。

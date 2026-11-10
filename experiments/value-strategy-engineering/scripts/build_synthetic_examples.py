#!/usr/bin/env python3
"""Produce deliberately fictional examples for structure tests; do not use for market evidence."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def elem(id,title,description,viewpoints,**kw):
    obj={'id':id,'title':title,'description':description,'origin':'ai_generic_seed','claim_state':'assumed',
         'decision_state':'proposed','validity_state':'active','confidence':'low','source_refs':[],
         'viewpoints':viewpoints,'rationale':'架空ケースの分析から生成した検証前の候補であり、実世界の事実ではない。',
         'human_confirmation_required':True}
    obj.update(kw)
    return obj

def rel(n,src,target,rtype,basis='架空ケースにおけるレビュー用の候補関係。',**kw):
    return {'id':f'REL-{n:04}','source_id':src,'target_id':target,'relation_type':rtype,'basis':basis,'certainty':'hypothesized',**kw}

def source(sid,title,statement):
    return {'id':sid,'title':title,'source_type':'conversation','classification':'source_data','origin':'user_explicit',
        'statement':statement,'locator':None,'recorded_at':None,'is_synthetic':True,'reliability':'unknown','permission_status':'approved_for_processing',
        'limitations':'研究用の架空シナリオ。顧客調査の記録ではない。'}

def base(slug,subject,domain,purpose,sources):
    return {
      'meta':{'artifact_type':'vse_candidate_model','schema_version':'1.0.0','target_subject':subject,
              'domain':domain,'language':'ja','target_maturity':'reviewable_candidate_40',
              'source_of_truth_status':'candidate_semantic_source_of_truth',
              'generated_at':None,'synthetic_case':True,'project_slug':slug},
      'scope':{'subject':subject,'purpose':purpose,'in_scope':['顧客課題の仮説','価値提案候補','戦略代替案','初期の検証計画'],
               'out_of_scope':['実顧客への調査実施','市場規模やROIの確定','正式な投資承認'],
               'controlled_by_organization':['提案の内容','自社の営業・提供体制の候補'],
               'external_and_uncontrolled':['顧客の購買判断','競合行動','外部環境'],
               'time_horizon':'企画初期（具体的な期間は未確認）'},
      'source_fragments':sources,'glossary':[{'term':'現状維持案','definition':'新たなサービス購入/投資を行わない比較基準。','aliases':['status quo']}],
      **{k:[] for k in ['objectives','actors','problems','values','hypotheses','alternatives','capabilities','decisions','interventions','evidence','outcomes','risks','experiments']},
      'relations':[],'open_questions':[],'findings':[],'change_log':[],
      'quality_summary':{'gate_state':'reviewable_40_candidate','review_tier':'J0',
          'checks':[{'rule_id':'Q-GAT-01','status':'pass_with_provisional_assumption',
                     'detail':'架空の初期入力に対し問題・複数代替案・反証計画がある。実需要は未検証。'}],
          'not_performed':['実顧客へのインタビュー','市場規模の検証','因果効果の実測','実在専門家によるレビュー','独立LLM Reviewer'],
          'limitations':['架空ケースの構造テストであり、実在顧客に有効とは限らない。'],
          'linguistic_quality':'not_assessed','semantic_validity':'unknown_with_reason'}}

def b2b():
 d=base('b2b_alm','架空の製造業顧客向けALM定着改善サービスの企画','b2b_consulting',
        '顧客が抱える可能性のある課題を整理し、現状維持を含めて提案候補と検証行動を比較する。',
        [source('SRC-0001','架空ケースの前提','製造業でALMを導入済みだが、教育やマニュアルの準備後も利用定着が進まないという架空の相談がある。'),
         source('SRC-0002','架空ケースの補助仮定','一部の顧客では文書管理や他のモデリングツールとの二重管理が懸念されると仮定する。')])
 d['objectives']=[elem('OBJ-0001','顧客課題に適合する提案機会を特定する','営業受注だけでなく顧客の改善可能性と検証を優先する。',['V0','V5'],source_refs=['SRC-0001'],origin='user_explicit',claim_state='stated',success_criteria=['課題を顧客の事実として確認','現状維持を含む代替案の議論を開始'])]
 d['actors']=[
   elem('ACT-0001','顧客の開発担当者','日常的にALMの入力と参照を担当する人。',['V1','V2'],actor_role='end_user',control_boundary='external',buying_role=['user']),
   elem('ACT-0002','顧客の管理者','導入目的と投資判断に関与する可能性のある人。',['V1','V5'],actor_role='budget_owner_candidate',control_boundary='external',buying_role=['budget_owner','approver']),
   elem('ACT-0003','自社のコンサルティング担当','診断・改善提案を検討する担当。',['V1','V6'],actor_role='consultant',control_boundary='internal',buying_role=['none']),
   elem('ACT-0004','顧客の購買担当','発注・契約条件を確認する可能性のある人。',['V1','V6'],actor_role='procurement',control_boundary='external',buying_role=['procurement']),
   elem('ACT-0005','自社の事業責任者','サービス投資と提供範囲の判断候補者。',['V0','V5'],actor_role='decision_authority_candidate',control_boundary='internal',buying_role=['none'])]
 d['problems']=[
  elem('PRB-0001','ALM利用が定着しない','利用者が既存業務の中でALMを使い続けられない可能性がある。',['V0','V2'],source_refs=['SRC-0001'],current_state='導入・教育済みとされるが利用が不十分',desired_state='利用者と管理者が業務上の成果を得ながら運用できる',customer_actor_id='ACT-0001',importance_unverified=True),
  elem('PRB-0002','既存文書・モデルとの二重管理','情報管理の責任分担が不明な場合に入力負荷が高まる可能性がある。',['V2','V3'],source_refs=['SRC-0002'],current_state='既存文書やモデルとの連携状況が不明',desired_state='情報の管理責任と参照元が明確',customer_actor_id='ACT-0001',importance_unverified=True)]
 d['values']=[elem('VAL-0001','利用負荷の削減と業務の見通し','顧客が情報の重複や確認作業を減らせるかを検討する。',['V3','V4'],beneficiary_actor_ids=['ACT-0001','ACT-0002'],value_measure='業務完了時間・重複登録・追跡可能性（いずれも測定方法未確定）',comparison_baseline='現在の業務運用')]
 d['hypotheses']=[
  elem('HYP-0001','操作習熟不足の仮説','操作理解の不足が利用定着の主要障害であるという候補。',['V2','V3'],hypothesis_kind='descriptive',prediction='利用者は基礎操作の不明点を多く挙げる。',falsification_condition='操作に問題がなく、業務設計が主障害という証拠が多い。',verification_plan='匿名化した利用者ヒアリングと操作観察。',alternative_explanations=['役割不明','二重管理']),
  elem('HYP-0002','業務責任の曖昧さの仮説','業務の入口・出口や役割分担が曖昧なことが継続利用を阻害するという候補。',['V2','V3'],hypothesis_kind='causal',prediction='定着できない工程では担当・完了基準を説明できない。',falsification_condition='責任・完了基準が明確でも定着が同程度に低い。',verification_plan='作業手順・成果物と担当者の整合レビュー。',alternative_explanations=['操作習熟不足','重複登録']),
  elem('HYP-0003','二重登録負担の仮説','既存ツールとの情報重複が運用負担を増大させるという候補。',['V2','V3'],hypothesis_kind='causal',prediction='同一情報を複数手段へ入力する事例が見つかる。',falsification_condition='入力重複がほぼ無く、別原因で利用を避けている。',verification_plan='実際の成果物フローを匿名化して観察。',alternative_explanations=['ツール自体の速度','権限設定']),
  elem('HYP-0004','初期診断への支払意思の仮説','顧客は教育の追加より診断への投資を選ぶ可能性がある。',['V3','V5','V6'],hypothesis_kind='purchase',prediction='予算責任者は診断の範囲と成果条件を受け入れ可能と評価する。',falsification_condition='予算責任者は診断より自力改善または追加教育を選ぶ。',verification_plan='許諾を得た実顧客によるコンセプト比較。',alternative_explanations=['予算不足','購買フロー不成立'])]
 d['alternatives']=[
  elem('ALT-0001','現状維持','既存教育・運用を継続し、新規の診断投資を行わない。',['V4','V5'],option_kind='status_quo',comparison_problem_id='PRB-0001',tradeoffs=['追加費用は抑えられる可能性','根本原因が残る可能性'],selection_status='candidate'),
  elem('ALT-0002','追加の操作教育','利用者の操作知識不足を主障害と仮定する施策。',['V4','V5'],option_kind='change',comparison_problem_id='PRB-0001',tradeoffs=['操作不足に有効かもしれない','業務責任や重複問題を解決しない可能性'],selection_status='candidate'),
  elem('ALT-0003','業務・定着診断','業務プロセス、役割、情報管理の課題を診断して改善案を作る。',['V4','V5'],option_kind='change',comparison_problem_id='PRB-0001',tradeoffs=['原因仮説を横断的に確認できる','現場の調査協力が必要'],selection_status='candidate')]
 d['capabilities']=[elem('CAP-0001','診断ヒアリングと業務分析能力','自社が提供可能かを判断する必要がある能力。',['V4','V6'],capability_owner='self',availability='unknown')]
 d['decisions']=[elem('DEC-0001','最初の提案入口の選択','案をまだ選択せず、顧客の課題と購買条件を確認して判断する。',['V5'],decision_status='open',chosen_alternative_id=None,decision_authority_actor_id='ACT-0005',criteria=['顧客課題への適合','営業負担','顧客が協力できる範囲','実行能力'],revisit_trigger='顧客の課題確認と社内能力確認が完了したとき')]
 d['interventions']=[elem('INT-0001','顧客の業務実態を確認する','外部連絡を自動実施せず、許諾を得たヒアリング案を作る。',['V6','V7'],target_actor_ids=['ACT-0001','ACT-0002'],execution_owner_id='ACT-0003',cost_status='unestimated',channel='対面またはオンライン（未定）')]
 d['evidence']=[elem('EVD-0001','架空の相談記述','ALM定着が不十分という架空ケースの入力。実顧客の観測ではない。',['V0','V3'],origin='user_explicit',claim_state='stated',source_refs=['SRC-0001'],evidence_kind='documented_record',source_fragment_id='SRC-0001',verification_status='unverified',limitations='架空ケース。実市場の証拠には使えない。')]
 d['outcomes']=[elem('OUT-0001','顧客による課題の確認状況','今後の検証で対象顧客が実課題を認識するか確認する。',['V7'],observation_status='planned',measure_name='課題認識の確認',value=None,unit='顧客',period='未設定',comparison_baseline='未調査',attribution_status='not_assessed')]
 d['risks']=[elem('RSK-0001','根拠のないROI訴求','根拠のない数値で提案すると顧客の信頼を損なう。',['V5','V7'],cause='実測データが無い',event='ROIを断定して提案',consequence='誤判断・信用低下',mitigation_candidate='算出条件を確認し、未確認の数値は提示しない',risk_acceptance_status='not_assessed')]
 d['decisions']=[elem('DEC-0001','開発候補の採否','静音価値の検証を受けて開発方針を判断する。',['V5'],decision_status='open',chosen_alternative_id=None,decision_authority_actor_id='ACT-0002',criteria=['顧客の選択理由','騒音と送風性能の比較','価格と提供可能性'],revisit_trigger='利用者の実試験データ取得後')]
 d['interventions']=[elem('INT-0001','試作コンセプトの比較を準備する','自動的に顧客へ送らず、承認後に実施する。',['V6'],target_actor_ids=['ACT-0001'],execution_owner_id='ACT-0002',cost_status='unestimated')]
 d['experiments']=[elem('EXP-0001','匿名化ヒアリングで原因仮説を区別する','実顧客の許諾を得るまでは開始しない。',['V7'],target_hypothesis_ids=['HYP-0001','HYP-0002','HYP-0003'],method='interview',primary_measure='主要原因として挙がる障害と、業務上の具体例',decision_rule='複数の独立証拠が得られた原因を優先し、矛盾は保留する',confounders=['役職による回答バイアス','成功顧客のみを対象にする選択バイアス'],status='planned',result_outcome_ids=[]),
  elem('EXP-0002','価値提案を比較して購買条件を確認する','架空の購買反応ではなく、許諾を得た顧客との検証を計画する。',['V6','V7'],target_hypothesis_ids=['HYP-0004'],method='prototype_test',primary_measure='評価された価値・導入条件・反対理由',decision_rule='受容条件の具体性と反対証拠を含めて検討する',confounders=['既存関係の有無','予算タイミング'],status='planned',result_outcome_ids=[])]
 d['relations']=[
  rel(1,'OBJ-0001','PRB-0001','addresses'),rel(2,'ACT-0001','PRB-0001','experiences'),rel(3,'ACT-0001','PRB-0002','experiences'),
  rel(4,'EVD-0001','HYP-0001','supports','相談記述は操作不足の直接証拠ではない。仮説検討のきっかけ。'),
  rel(5,'ALT-0001','PRB-0001','addresses'),rel(6,'ALT-0002','PRB-0001','addresses'),rel(7,'ALT-0003','PRB-0001','addresses'),
  rel(8,'ALT-0003','VAL-0001','offers'),rel(9,'EXP-0001','HYP-0001','tests'),rel(10,'EXP-0001','HYP-0002','tests'),
  rel(11,'EXP-0001','HYP-0003','tests'),rel(12,'EXP-0002','HYP-0004','tests'),rel(13,'INT-0001','ALT-0003','implements'),
  rel(14,'INT-0001','ACT-0001','targets'),rel(15,'RSK-0001','ALT-0003','risks'),
  rel(16,'ALT-0003','ALT-0001','compared_with'),rel(17,'ALT-0003','ALT-0002','compared_with'),
  rel(18,'INT-0001','OUT-0001','causally_influences','仮説として検証する。因果が確定したわけではない。',causal_status='hypothesized')]
 d['open_questions']=[
 {'id':'QST-0001','question':'顧客がALMを利用しない直接の障害は、操作・役割・二重登録のどれか。','priority':'critical','impact_refs':['PRB-0001','HYP-0001','HYP-0002','HYP-0003'],'owner_role':'顧客の現場担当者','verification_action':'許諾を得た業務ヒアリングと成果物フロー確認','status':'open'},
 {'id':'QST-0002','question':'診断サービスに予算と意思決定権限を持つ顧客担当者は誰か。','priority':'high','impact_refs':['HYP-0004','ALT-0003','DEC-0001'],'owner_role':'顧客の予算責任者','verification_action':'正式な顧客窓口を通じて確認する','status':'open'},
 {'id':'QST-0003','question':'自社が診断サービスを提供できる工数・契約範囲は何か。','priority':'high','impact_refs':['CAP-0001','DEC-0001'],'owner_role':'自社の事業責任者','verification_action':'社内能力と採算基準を確認する','status':'open'}]
 d['findings']=[{'id':'FND-0001','severity':'high','rule_id':'Q-PRB-01','evidence_refs':['PRB-0001','HYP-0002'],'message':'主要な原因は未確認。複数の説明を保持する必要がある。','minimum_repair':'顧客ヒアリングで仮説の区別を試みる。','requires_human':True}]
 d['change_log']=[{'id':'CHG-0001','event_type':'created','target_id':'DEC-0001','reason':'架空ケースの初稿作成','changed_by':'synthetic_generator','date':None}]
 return d

def consumer():
 d=base('consumer_product','架空の静音デスクファンの市場企画','product_planning','利用者の価値と代替品を比較し、需要の確かめ方を考える。',
    [source('SRC-0001','架空の製品企画メモ','静かに使える小型卓上ファンを検討している。価格、需要、購入意向は未調査とする。')])
 d['objectives']=[elem('OBJ-0001','検証可能な企画候補を作る','小型デスクファンの価値仮説と比較案を検討する。',['V0'],source_refs=['SRC-0001'],origin='user_explicit',claim_state='stated')]
 d['actors']=[elem('ACT-0001','在宅作業者','卓上で製品を使用する想定利用者。',['V1','V2'],actor_role='user',control_boundary='external',buying_role=['user']),elem('ACT-0002','製品企画責任者','企画の採否と試作を判断する自社の責任者候補。',['V1','V5'],actor_role='decision_authority_candidate',control_boundary='internal',buying_role=['none'])]
 d['problems']=[elem('PRB-0001','作業時の騒音','騒音が集中を妨げる可能性がある。',['V2'],current_state='利用者の実態は未調査',desired_state='集中を妨げずに送風する',customer_actor_id='ACT-0001',importance_unverified=True)]
 d['values']=[elem('VAL-0001','静かに使える価値','騒音への不満を減らすという価値仮説。',['V3'],beneficiary_actor_ids=['ACT-0001'],value_measure='主観的静音性と音圧レベル（方法未設定）',comparison_baseline='既存製品')]
 d['hypotheses']=[elem('HYP-0001','静音性の価値仮説','利用者にとって静音性が購入選択の重要要因となる可能性。',['V3'],hypothesis_kind='value',prediction='対象者が既存製品との比較で静音性を優先して評価する。',falsification_condition='静音性が優先選択要因でない回答/行動が多数見られる。',verification_plan='利用試験と選択理由の確認を計画。',alternative_explanations=['価格優先','送風性能優先'])]
 d['alternatives']=[elem('ALT-0001','既存製品を選ぶ','新しい製品を開発せず既存製品を選ぶ。',['V5'],option_kind='status_quo',comparison_problem_id='PRB-0001',selection_status='candidate'),
  elem('ALT-0002','静音志向の新製品','静音性を主な価値として新製品を設計する。',['V4','V5'],option_kind='change',comparison_problem_id='PRB-0001',selection_status='candidate')]
 d['decisions']=[elem('DEC-0001','開発候補の採否','静音価値の検証を受けて開発方針を判断する。',['V5'],decision_status='open',chosen_alternative_id=None,decision_authority_actor_id='ACT-0002',criteria=['顧客の選択理由','騒音と送風性能の比較','価格と提供可能性'],revisit_trigger='利用者の実試験データ取得後')]
 d['interventions']=[elem('INT-0001','試作コンセプトの比較を準備する','自動的に顧客へ送らず、承認後に実施する。',['V6'],target_actor_ids=['ACT-0001'],execution_owner_id='ACT-0002',cost_status='unestimated')]
 d['experiments']=[elem('EXP-0001','コンセプト比較','実参加者によるコンセプト選択を計画。',['V7'],target_hypothesis_ids=['HYP-0001'],method='prototype_test',primary_measure='実参加者が重視した選択理由',decision_rule='価格・静音性のトレードオフが説明できるかを確認する',confounders=['既存ブランド選好'],status='planned',result_outcome_ids=[])]
 d['relations']=[rel(1,'OBJ-0001','PRB-0001','addresses'),rel(2,'ACT-0001','PRB-0001','experiences'),rel(3,'ALT-0001','PRB-0001','addresses'),rel(4,'ALT-0002','PRB-0001','addresses'),rel(5,'ALT-0002','VAL-0001','offers'),rel(6,'EXP-0001','HYP-0001','tests'),rel(7,'INT-0001','ALT-0002','implements'),rel(8,'INT-0001','ACT-0001','targets')]
 d['open_questions']=[{'id':'QST-0001','question':'どの利用者・使用環境で静音性が価値になるか。','priority':'high','impact_refs':['HYP-0001'],'owner_role':'企画担当','verification_action':'実利用者の試作比較','status':'open'}]
 d['quality_summary']['checks']=[{'rule_id':'Q-GAT-01','status':'pass_with_provisional_assumption','detail':'架空ケースの比較・反証計画がレビュー可能。実市場未検証。'}]
 return d

def main():
 for folder,fn in [('b2b_alm',b2b),('consumer_product',consumer)]:
  out=ROOT/'examples'/folder/'10_vse_model.json'
  out.write_text(json.dumps(fn(),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  print(out)

if __name__=='__main__':main()

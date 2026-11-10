# GitHub等で公開する前のチェックリスト

- [ ] すべての例は架空、実顧客の会社名・個人名・機密情報を含まない。
- [ ] すべての出典URLは一次情報または信頼できる出版元を指し、全文複製でない。
- [ ] `10_vse_model.json`は候補モデルで、実証・顧客確認・正式採用と表示されていない。
- [ ] PythonスクリプトにAPIキーや外部送信処理がない。
- [ ] `python -m unittest discover -s tests -v`が通る。
- [ ] `python scripts/validate_vse.py examples/b2b_alm/10_vse_model.json --strict`が通る。
- [ ] 生成した投影ファイルのIDと名称が正本JSONと一致する。
- [ ] 生成ファイルのsha256は`16_generation_manifest.json`に記録されている。
- [ ] 過去4回の模擬レビューを実在専門家レビューとして表示していない。
- [ ] ライセンス、著者表記、参照元SELaboの扱いを公開前に確認する。
- [ ] READMEで未実施の検証を明記する。

※ ZIP作成自体はGitHubへの公開を意味しない。公開には追加のユーザー操作が必要。

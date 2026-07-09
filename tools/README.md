# tools/ — クラウドからカレンダー・メールを操作

PCを離れていても、この環境から **Googleカレンダー登録** と **Gmail送信** を実行するための最小ツール。
標準ライブラリのみ（pipインストール不要）。

## 中身
| ファイル | 役割 | 実行場所 |
|---------|------|---------|
| `google_auth.py` | 共通認証（環境変数から鍵を読む） | クラウド |
| `calendar_add.py` | カレンダーに予定を追加 | クラウド |
| `gmail_send.py` | メールを送信 | クラウド |
| `make_refresh_token.py` | リフレッシュトークンを発行 | **PC** |

## セットアップ（1回だけ）

### ① PC側：鍵を発行
PC側Claudeに頼むか、手元で実行：
```bash
python3 tools/make_refresh_token.py /Users/sagaratoera/秘書/認証/gcp-oauth.keys.json
```
ブラウザで同意すると、3つの値が表示される：
```
GOOGLE_CLIENT_ID     = ...
GOOGLE_CLIENT_SECRET = ...
GOOGLE_REFRESH_TOKEN = ...
```

### ② クラウド側：シークレットに登録
Claude Code (web) の**環境設定**で、上の3つを環境変数（シークレット）として登録する。
- 参考: https://code.claude.com/docs/en/claude-code-on-the-web
- ⚠️ **Gitには絶対にコミットしない**（`.gitignore` で `.env` 系は除外済み）。

## 使い方

カレンダー追加:
```bash
python3 tools/calendar_add.py \
  --summary "世紀東急へ警備営業" \
  --start 2026-07-10T14:00:00 --end 2026-07-10T15:00:00 \
  --location "本社" --description "提案資料PDF持参"
```

メール送信:
```bash
python3 tools/gmail_send.py \
  --to hayashi@example.com \
  --subject "出張旅費規程の確認" \
  --body "林さん\n\nお世話になっております。..." \
  --cc boss@example.com
```

## 注意
- **7日失効の罠**: OAuth同意画面が「テスト」状態だと、リフレッシュトークンが7日で失効する。長期運用するなら Google Cloud Console で同意画面を「本番公開」にしてから鍵を発行すること。
- **鍵はPC用と別管理を推奨**（片方が漏れても他方が無事）。
- **ネットワークポリシー**: この環境の外向き通信ポリシーが Google API を許可している必要がある（疎通確認済み: 2026-07-09）。
- スコープは `calendar.events` と `gmail.send` の最小限。予定の閲覧やメール読み取りは含まない。

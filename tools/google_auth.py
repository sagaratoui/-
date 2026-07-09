"""Google API 共通認証ヘルパー（クラウド環境・ヘッドレス用）。

秘密情報は一切ここに書かない。環境変数（シークレット）から読む:
  - GOOGLE_CLIENT_ID
  - GOOGLE_CLIENT_SECRET
  - GOOGLE_REFRESH_TOKEN

標準ライブラリのみ使用（pipインストール不要）。
"""
import json
import os
import urllib.parse
import urllib.request
import urllib.error

TOKEN_URL = "https://oauth2.googleapis.com/token"


def get_access_token():
    """リフレッシュトークンからアクセストークンを取得して返す。"""
    cid = os.environ.get("GOOGLE_CLIENT_ID")
    csecret = os.environ.get("GOOGLE_CLIENT_SECRET")
    rtoken = os.environ.get("GOOGLE_REFRESH_TOKEN")

    missing = [
        name for name, val in (
            ("GOOGLE_CLIENT_ID", cid),
            ("GOOGLE_CLIENT_SECRET", csecret),
            ("GOOGLE_REFRESH_TOKEN", rtoken),
        ) if not val
    ]
    if missing:
        raise SystemExit(
            "環境変数(シークレット)が未設定です: " + ", ".join(missing)
            + "\n→ 環境のシークレットに登録してください。"
        )

    data = urllib.parse.urlencode({
        "client_id": cid,
        "client_secret": csecret,
        "refresh_token": rtoken,
        "grant_type": "refresh_token",
    }).encode()

    req = urllib.request.Request(TOKEN_URL, data=data, method="POST")
    try:
        with urllib.request.urlopen(req) as r:
            payload = json.load(r)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        hint = ""
        if "invalid_grant" in detail:
            hint = ("\nヒント: リフレッシュトークンが失効している可能性。"
                    "OAuth同意画面が「テスト」状態だと7日で失効します。"
                    "「本番公開」にして再発行してください。")
        raise SystemExit(f"トークン取得エラー {e.code}: {detail}{hint}")
    return payload["access_token"]


def api_post(url, token, body):
    """認証付きでJSONをPOSTし、結果のdictを返す。"""
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        url, data=data, method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        raise SystemExit(f"APIエラー {e.code}: {detail}")

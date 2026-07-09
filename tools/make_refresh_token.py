#!/usr/bin/env python3
"""【PCで実行】カレンダー+Gmail送信用のリフレッシュトークンを発行する。

既存の OAuth クライアント(gcp-oauth.keys.json)を使い、ブラウザで一度だけ同意する。
出力された3つの値を、クラウド環境のシークレットに登録する。

必要: pip install google-auth-oauthlib （PC側には既に入っているはず）

実行:
  python3 make_refresh_token.py [gcp-oauth.keys.json のパス]
"""
import sys

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    raise SystemExit(
        "google-auth-oauthlib が必要です: pip install google-auth-oauthlib"
    )

SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/gmail.send",
]


def main():
    keys = sys.argv[1] if len(sys.argv) > 1 else "gcp-oauth.keys.json"
    flow = InstalledAppFlow.from_client_secrets_file(keys, SCOPES)
    # access_type=offline + prompt=consent でリフレッシュトークンを確実に取得
    creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")

    print("\n===== クラウド環境のシークレットに登録する3つの値 =====")
    print("GOOGLE_CLIENT_ID     =", creds.client_id)
    print("GOOGLE_CLIENT_SECRET =", creds.client_secret)
    print("GOOGLE_REFRESH_TOKEN =", creds.refresh_token)
    print("\n⚠️ これらは秘密。Gitにコミットしないこと。")


if __name__ == "__main__":
    main()

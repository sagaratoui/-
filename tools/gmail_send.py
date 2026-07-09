#!/usr/bin/env python3
"""Gmailでメールを送信する（クラウド環境から実行可）。

使用例:
  python3 tools/gmail_send.py \
    --to someone@example.com \
    --subject "出張旅費規程の確認" \
    --body "林さん\n\nお世話になっております。..." \
    --cc boss@example.com
"""
import argparse
import base64
from email.message import EmailMessage

from google_auth import get_access_token, api_post


def main():
    p = argparse.ArgumentParser(description="Gmailでメール送信")
    p.add_argument("--to", required=True, help="宛先(カンマ区切りで複数可)")
    p.add_argument("--subject", required=True, help="件名")
    p.add_argument("--body", required=True, help="本文(改行は \\n)")
    p.add_argument("--cc", default=None, help="CC(任意)")
    p.add_argument("--from", dest="sender", default=None,
                   help="送信元(省略時は認証アカウント)")
    args = p.parse_args()

    msg = EmailMessage()
    msg["To"] = args.to
    if args.cc:
        msg["Cc"] = args.cc
    if args.sender:
        msg["From"] = args.sender
    msg["Subject"] = args.subject
    msg.set_content(args.body.replace("\\n", "\n"))

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    token = get_access_token()
    res = api_post(
        "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
        token, {"raw": raw},
    )
    print("✅ 送信しました  id:", res.get("id"))


if __name__ == "__main__":
    main()

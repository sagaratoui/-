#!/usr/bin/env python3
"""Googleカレンダーに予定を追加する（クラウド環境から実行可）。

使用例:
  python3 tools/calendar_add.py \
    --summary "世紀東急へ警備営業" \
    --start 2026-07-10T14:00:00 --end 2026-07-10T15:00:00 \
    --location "本社" --description "提案資料PDF持参"
"""
import argparse

from google_auth import get_access_token, api_post


def main():
    p = argparse.ArgumentParser(description="Googleカレンダーに予定を追加")
    p.add_argument("--summary", required=True, help="予定タイトル")
    p.add_argument("--start", required=True,
                   help="開始 ISO8601 例: 2026-07-10T14:00:00")
    p.add_argument("--end", required=True,
                   help="終了 ISO8601 例: 2026-07-10T15:00:00")
    p.add_argument("--tz", default="Asia/Tokyo", help="タイムゾーン(既定 Asia/Tokyo)")
    p.add_argument("--calendar", default="primary", help="カレンダーID(既定 primary)")
    p.add_argument("--description", default="", help="説明")
    p.add_argument("--location", default="", help="場所")
    args = p.parse_args()

    body = {
        "summary": args.summary,
        "start": {"dateTime": args.start, "timeZone": args.tz},
        "end": {"dateTime": args.end, "timeZone": args.tz},
    }
    if args.description:
        body["description"] = args.description
    if args.location:
        body["location"] = args.location

    token = get_access_token()
    url = f"https://www.googleapis.com/calendar/v3/calendars/{args.calendar}/events"
    res = api_post(url, token, body)
    print("✅ 予定を作成しました:", res.get("htmlLink") or res.get("id"))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""自宅→集合場所の道路距離を Google Maps Distance Matrix API で計算し、
通勤費(距離手当)の月額バンドに割り付ける。

必要な環境変数(シークレット):
  - GOOGLE_MAPS_API_KEY   ← カレンダー/Gmailの鍵とは別物。課金有効化＋Distance Matrix API有効化が必要。

入力(個人情報を含むためGitに置かない。--input で外部ファイルを指定):
  JSON配列。例:
  [
    {"no": 1, "name": "相良 修二", "address": "福岡県糟屋郡志免町王子1-26-4"},
    ...
  ]

使用例:
  python3 tools/distance.py \
    --office "福岡県福岡市博多区月隈2-23" \
    --input /path/to/people.local.json
"""
import argparse
import json
import os
import urllib.parse
import urllib.request
import urllib.error

# 片道km → (月額, ラベル)  ※国税庁 マイカー・自転車通勤者の非課税限度額
BANDS = [
    (2,   0,      "〜2km未満(対象外)"),
    (10,  4200,   "2〜10km"),
    (15,  7100,   "10〜15km"),
    (25,  12900,  "15〜25km"),
    (35,  18700,  "25〜35km"),
    (45,  24400,  "35〜45km"),
    (55,  28000,  "45〜55km"),
    (10**9, 31600, "55km〜"),
]


def band_for(km):
    for upper, yen, label in BANDS:
        if km < upper:
            return yen, label
    return 31600, "55km〜"


def distance_matrix(origins, destination, key):
    """origins(list) -> destination の道路距離(m)を返す。Distance Matrix API。"""
    params = urllib.parse.urlencode({
        "origins": "|".join(origins),
        "destinations": destination,
        "mode": "driving",
        "language": "ja",
        "region": "jp",
        "key": key,
    })
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?" + params
    try:
        with urllib.request.urlopen(url) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"APIエラー {e.code}: {e.read().decode(errors='replace')}")
    if data.get("status") != "OK":
        raise SystemExit(f"APIステータス異常: {data.get('status')} / {data.get('error_message','')}")
    results = []
    for row in data["rows"]:
        el = row["elements"][0]
        if el.get("status") != "OK":
            results.append(None)
        else:
            results.append(el["distance"]["value"])  # meters
    return results


def main():
    p = argparse.ArgumentParser(description="通勤距離→月額バンド割付(Google Maps)")
    p.add_argument("--office", required=True, help="集合場所の住所")
    p.add_argument("--input", required=True, help="人員JSONファイル(Git管理外)")
    args = p.parse_args()

    key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not key:
        raise SystemExit(
            "環境変数 GOOGLE_MAPS_API_KEY が未設定です。\n"
            "→ Google Cloud で Maps APIキー(課金有効・Distance Matrix API有効)を作り、"
            "環境シークレットに登録してください。"
        )

    with open(args.input, encoding="utf-8") as f:
        people = json.load(f)

    origins = [pp["address"] for pp in people]
    meters = distance_matrix(origins, args.office, key)

    total = 0
    print(f"集合場所: {args.office}\n")
    print(f"{'No':>2}  {'氏名':<22} {'片道':>7}  {'距離帯':<14} {'月額':>8}")
    print("-" * 62)
    for pp, m in zip(people, meters):
        if m is None:
            print(f"{pp['no']:>2}  {pp['name']:<22} {'算出不可(住所要確認)'}")
            continue
        km = m / 1000
        yen, label = band_for(km)
        total += yen
        print(f"{pp['no']:>2}  {pp['name']:<22} {km:>6.1f}km  {label:<14} ¥{yen:>7,}")
    print("-" * 62)
    print(f"{'月額合計':<34} ¥{total:>7,}   / 年 ¥{total*12:,}")


if __name__ == "__main__":
    main()

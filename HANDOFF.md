# 🧳 引き継ぎ書（HANDOFF）— PCから離れても続けるために

> このファイルは「新しいセッションを開いたClaude」と「PCから離れた自分」が、
> **これ1枚を読めば文脈を引き継げる**ための起点。最終更新 2026-07-09。
> ⚠️ 社外秘（氏名・住所・財務・取引先・ID）を含む。private前提。

---

## 0. まず新セッションはこの順で読む
1. この `HANDOFF.md`（全体像・どこに何があるか）
2. `open.md`（現在の未対応TODO＝Notion「✅未対応TODO一覧」のミラー）
3. 必要に応じて Notion を検索（下の構造マップ参照）

---

## 1. これは何のシステムか
**晴栄建設の「AI秘書システム」**。経営・採用・現場・秘書業務をClaudeが横断管理する。
本体はユーザーのPC `/Users/sagaratoera/秘書`（Claude Code ターミナル版）にあり、
**Notion「晴栄建設 HQ」が全社の一元管理ベース（= クラウドの真実の源）**。

## 2. 「ローカル」は2つある（混同注意）
| | ① PCのローカル秘書システム | ② クラウド環境（Web/このリポジトリ） |
|---|---|---|
| 場所 | PC `/Users/sagaratoera/秘書` | クラウドの使い捨てコンテナ / `sagaratoui/-` |
| 中身 | `.company/`・スクリプト群・GAS・音声 | `open.md`・`HANDOFF.md` 等のテキスト |
| Notion同期 | ローカル `todos/open.md` ⇄ Notion | このリポジトリ ⇄ Notion（手動git） |
| スクリプト実行 | ✅ できる | ❌ できない（PC認証が必要） |

## 3. PCを離れてできること / できないこと
**✅ できる（Notion＋Web版Claudeだけで完結）**
- TODO・意思決定ログの確認／追記／整理（Notionはスマホからも読める）
- 資料の読み込み・要約・文章作成（メール下書き、原稿、提案文など）
- 判断の壁打ち・段取り検討
- Notion「📱 現場・手待ちタスク（スマホでOK）」に抽出済みの現場タスク

**❌ できない（PCに戻ってから）**
- 見積書/日報/評価シートの生成（`見積書/` `日報/` 等のPythonスクリプト）
- Googleカレンダー登録・フォーム作成・スプレッドシート更新（`automation/ ./run`）
- Gmail自動送信、GAS(clasp)関連
- → これらは「PCでやることリスト」として `open.md` に残す運用にする

## 4. Notion 構造マップ（引き継ぎの本棚）
- 🏢 **晴栄建設 HQ**（親） … https://app.notion.com/p/344cc219fe6281f781f7d7bf9d4db402
  - ✅ **未対応TODO一覧（本体・常時更新）** … https://app.notion.com/p/392cc219fe6281059939f63b8c7a6b09
  - 📱 **現場・手待ちタスク（スマホでOK）** … https://app.notion.com/p/397cc219fe6281f49149fc2f586bf3d4
  - 📅 定期業務まとめ（週次・月次） … https://app.notion.com/p/353cc219fe62815cb74af67129a7b29c
  - 📚 運用ドキュメント … https://app.notion.com/p/392cc219fe628160b96ed687ce11782f
  - 🗂️ ローカル秘書システム構成ガイド … https://app.notion.com/p/392cc219fe6281aab773fb502f7a94f7
  - 🗄️ 秘書室・TODO（親） … https://app.notion.com/p/344cc219fe6281e7b399e992b7610ae2
  - 👥 採用・人事 … https://app.notion.com/p/344cc219fe62813eb6fde9768c030d2c
- 4部署構成：経営戦略 / 採用・人事 / 現場管理(PM) / 秘書室・TODO

## 5. 直近の締切（2026-07-09 時点・詳細は open.md）
| 期限 | 内容 |
|------|------|
| 7/10 | 世紀東急へ警備営業（提案資料PDF持参）／税理士アポ（PL・消費税・課税確認3件） |
| 7/13(月)17:00 | King of Time キックオフ 班長会議 |
| 7/22締切 | 斗偉さん 2級土木施工管理技士 申込（試験10/25） |
| 7/27週 | 須恵 上下水打ち合わせ日程確定 |
| 12月アンカー | 須恵造成の売却入金→西銀3,200万返済（9月売出し必達が生命線） |

## 6. 同期のルール（重要）
- **真実の源は Notion**。このリポジトリの `open.md` はそのミラー。
- 双方向の自動同期ではない。反映は手動git：
  - このリポジトリを更新 → PC側で `git pull origin claude/integration-status-check-2cf6ed`
  - PC側で編集 → PCから `git push`
- 食い違ったら **Notionを正**とする。

## 7. PCに戻ったらやること
- [ ] この `open.md`・`HANDOFF.md` を PC側 `.company/` と `todos/open.md` に反映
- [ ] **PC側Claudeに明記させる**：「TODOの真実の源はNotion。ローカルは控え。食い違ったらNotionを正」を `.company/` に書き、Claudeの記憶にも入れる（※Notion構成ガイドには記載済みだがPC側メモリは別物のため念押し）

---
*作成：Claude（Web） / 2026-07-09。*

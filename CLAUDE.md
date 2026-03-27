# Lumina - 読書管理アプリ

## プロジェクト概要
単一HTMLファイル（index.html）で動作する読書管理PWA。
Google Books API / OpenBD / NDL APIで本を検索・登録・管理できる。

## 公開状況
- **GitHub**: pushで自動デプロイ
- **Vercel**: 本番公開済み
- **Google Play Console**: 本人確認完了済み（2026-03-27時点）

## 次のステップ（Play Store公開）
1. PWABuilderでAPKを生成（https://www.pwabuilder.com）
2. assetlinks.jsonをVercelに配置（TWAドメイン認証）
3. Play StoreにAPKをアップロード
4. 審査提出

## 技術構成
- `index.html` - アプリ本体（全機能）
- `manifest.json` - PWAマニフェスト（name: "Lumina", theme_color: "#3A4A30"）
- `sw.js` - Service Worker
- `icons/icon-192.png` / `icons/icon-512.png` - アプリアイコン

## デザイン
- カラーテーマ: オリーブグリーン (#3A4A30) / クリーム (#EDE8DF)
- ダークモード対応（html.dark クラスで切り替え）
- 本棚グリッド表示、月別グラフ（Chart.js）

## 主要機能
- 本の検索・登録（バーコードスキャン対応）
- ステータス管理: Next / Reading / Done
- 11ジャンル分類（日本語ラベル）
- お気に入り著者、メモ機能
- フィルター（ステータス・ジャンル・価格・登録月）
- バックアップ/リストア、パスコードロック、ダークモード

## LocalStorage キー
- `myshelf-v2` - 書籍データ
- `lumina-fav-authors` - お気に入り著者
- `lumina-passcode` / `lumina-passcode-enabled` - パスコード設定

## 開発環境
- ローカルサーバー: `python3 -m http.server 8080 --directory /Users/zett/bookshelf`
- launch.json設定済み（ポート8080）
- GitHubへのpush → Vercel自動デプロイ

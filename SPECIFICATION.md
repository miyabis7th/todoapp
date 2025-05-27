# Todo Application 開発仕様書

## 1. プロジェクト概要

### 1.1 アプリケーション名
**Todo Application** - Instagram風UIを持つモダンなタスク管理アプリケーション

### 1.2 概要説明
Flask（Python）とGoogle Cloud Servicesを使用して構築された、直感的で美しいUIを持つタスク管理アプリケーション。ユーザーはタスクの作成、編集、削除、完了状況の管理、画像の添付が可能。

### 1.3 主要機能
- ✅ タスクの作成・読み取り・更新・削除（CRUD操作）
- ✅ タスク完了状況の管理
- ✅ 画像アップロード機能
- ✅ Instagram風のモダンUI
- ✅ Google Cloud Firestore連携によるデータ永続化
- ✅ Google Cloud Run上での運用
- ✅ GitHub Actions CI/CD自動デプロイ

---

## 2. 技術スタック

### 2.1 バックエンド
- **言語**: Python 3.9
- **フレームワーク**: Flask 2.2.3
- **WSGIサーバー**: Gunicorn 20.1.0
- **テンプレートエンジン**: Jinja2

### 2.2 データベース
- **メインDB**: Google Cloud Firestore
- **認証**: Google Cloud Service Account

### 2.3 フロントエンド
- **CSS Framework**: Bootstrap 5
- **Icons**: Font Awesome
- **レスポンシブデザイン**: モバイルファースト

### 2.4 インフラストラクチャ
- **ホスティング**: Google Cloud Run
- **コンテナ**: Docker
- **イメージレジストリ**: Google Artifact Registry
- **CI/CD**: GitHub Actions
- **認証**: Google Cloud Service Account

### 2.5 開発・運用
- **バージョン管理**: Git (GitHub)
- **依存関係管理**: requirements.txt
- **環境管理**: Docker コンテナ

---

## 3. アプリケーション設計

### 3.1 アーキテクチャ概要
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   ユーザー      │────│  Cloud Run      │────│   Firestore     │
│   (Browser)     │    │  (Flask App)    │    │   (Database)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                │
                        ┌─────────────────┐
                        │ Artifact Registry│
                        │ (Docker Images) │
                        └─────────────────┘
```

### 3.2 ディレクトリ構造
```
todoapp/
├── Dockerfile                 # コンテナ定義
├── main.py                   # アプリケーションエントリポイント
├── requirements.txt          # Python依存関係
├── README.md                 # プロジェクト説明
├── .github/
│   └── workflows/
│       └── ci-cd.yaml       # CI/CDパイプライン定義
└── app/
    ├── __init__.py          # アプリケーションファクトリ
    ├── models.py            # データモデル定義
    ├── routes.py            # ルート定義・ビジネスロジック
    ├── static/
    │   └── uploads/         # アップロード画像保存
    └── templates/           # HTMLテンプレート
        ├── base.html        # ベーステンプレート
        ├── index.html       # タスク一覧画面
        ├── create.html      # タスク作成画面
        ├── view.html        # タスク詳細画面
        └── edit.html        # タスク編集画面
```

---

## 4. データモデル設計

### 4.1 Todoモデル
```python
class Todo:
    def __init__(self, title, description='', completed=False, 
                 image_url=None, id=None, created_at=None):
        self.id = id or str(uuid.uuid4())           # ユニークID
        self.title = title                          # タスクタイトル (必須)
        self.description = description              # タスク説明 (任意)
        self.completed = completed                  # 完了状況 (boolean)
        self.image_url = image_url                  # 添付画像URL (任意)
        self.created_at = created_at or datetime.now()  # 作成日時
```

### 4.2 Firestoreコレクション構造
```
todos/
├── {document_id}/
│   ├── id: string          # ドキュメントID
│   ├── title: string       # タスクタイトル
│   ├── description: string # タスク説明
│   ├── completed: boolean  # 完了状況
│   ├── image_url: string   # 画像URL (任意)
│   └── created_at: timestamp # 作成日時
```

---

## 5. API設計（ルート定義）

### 5.1 エンドポイント一覧

| メソッド | エンドポイント | 説明 | 機能 |
|---------|---------------|------|------|
| GET | `/` | タスク一覧表示 | 全タスクを作成日時降順で表示 |
| GET | `/todo/create` | タスク作成フォーム | 新規タスク作成画面 |
| POST | `/todo/create` | タスク作成処理 | 新規タスクをDBに保存 |
| GET | `/todo/<id>` | タスク詳細表示 | 指定IDのタスク詳細 |
| GET | `/todo/<id>/edit` | タスク編集フォーム | タスク編集画面 |
| POST | `/todo/<id>/edit` | タスク更新処理 | タスク情報を更新 |
| POST | `/todo/<id>/delete` | タスク削除処理 | 指定タスクを削除 |
| POST | `/todo/<id>/toggle` | 完了状況切替 | Ajax経由で完了状況を切替 |

### 5.2 ルート詳細仕様

#### 5.2.1 タスク一覧 (`GET /`)
- **機能**: 全タスクを作成日時降順で表示
- **レスポンス**: `index.html` テンプレート
- **データ**: `todos` リスト（Todoオブジェクトの配列）

#### 5.2.2 タスク作成 (`GET/POST /todo/create`)
- **GET**: 作成フォーム表示
- **POST**: 
  - 入力データ: `title`, `description`, `image` (ファイル)
  - バリデーション: タイトル必須チェック
  - 画像処理: ファイルアップロード・URL生成
  - DB保存: Firestoreに新規ドキュメント作成

#### 5.2.3 タスク詳細 (`GET /todo/<id>`)
- **機能**: 指定IDのタスク詳細表示
- **エラーハンドリング**: 存在しないIDの場合はindex画面にリダイレクト

#### 5.2.4 タスク編集 (`GET/POST /todo/<id>/edit`)
- **GET**: 編集フォーム（既存データ表示）
- **POST**: 
  - 更新データ: `title`, `description`, `completed`, `image`
  - 画像処理: 新規アップロード時のみ更新
  - DB更新: Firestoreドキュメント更新

#### 5.2.5 タスク削除 (`POST /todo/<id>/delete`)
- **機能**: 指定タスクをFirestoreから削除
- **リダイレクト**: 削除後はindex画面へ

#### 5.2.6 完了状況切替 (`POST /todo/<id>/toggle`)
- **機能**: Ajax経由でタスクの完了状況を切替
- **レスポンス**: JSON形式 `{"completed": boolean}`

---

## 6. UI/UX設計

### 6.1 デザインコンセプト
- **Instagram風カードレイアウト**
- **モバイルファースト・レスポンシブデザイン**
- **直感的な操作性**
- **モダンで清潔感のあるUI**

### 6.2 画面構成

#### 6.2.1 タスク一覧画面 (`index.html`)
- **レイアウト**: カードグリッド（3列）
- **要素**: 
  - ヘッダー（タイトル + New Taskボタン）
  - タスクカード（画像、タイトル、説明、完了状況、操作ボタン）
  - 完了済みタスクの視覚的区別

#### 6.2.2 タスク作成画面 (`create.html`)
- **フォーム要素**:
  - タイトル入力（必須）
  - 説明入力（任意・テキストエリア）
  - 画像アップロード（任意）
  - 作成ボタン・キャンセルボタン

#### 6.2.3 タスク詳細画面 (`view.html`)
- **表示要素**:
  - 画像（存在する場合）
  - タイトル・説明
  - 作成日時・完了状況
  - 編集・削除ボタン

#### 6.2.4 タスク編集画面 (`edit.html`)
- **フォーム要素**:
  - 既存データの事前入力
  - 完了状況チェックボックス
  - 画像の差し替え機能
  - 更新・キャンセルボタン

### 6.3 共通コンポーネント (`base.html`)
- **Bootstrap 5** ベースのレスポンシブレイアウト
- **Font Awesome** アイコン
- **フラッシュメッセージ** 表示領域
- **ナビゲーション** ヘッダー

---

## 7. セキュリティ仕様

### 7.1 認証・認可
- **Google Cloud Service Account** による認証
- **Cloud Run** 環境での自動認証
- **Firestore** アクセス権限管理

### 7.2 入力検証
- **ファイルアップロード**: 画像形式制限 (png, jpg, jpeg, gif)
- **ファイル名**: `secure_filename()` による安全化
- **必須項目**: タイトルフィールドの検証

### 7.3 データ保護
- **UUID**: ランダムなタスクID生成
- **HTTPS**: Cloud Run自動SSL/TLS
- **環境変数**: 機密情報の外部管理

---

## 8. インフラ・デプロイメント仕様

### 8.1 CI/CDパイプライン
```yaml
トリガー: mainブランチへのpush
↓
1. ソースコードチェックアウト
2. Google Cloud認証
3. Docker認証設定
4. Dockerイメージビルド
5. Artifact Registryへpush
6. Cloud Runへデプロイ
7. 公開URL出力
```

### 8.2 必要なGCPサービス
- **Cloud Run**: アプリケーションホスティング
- **Artifact Registry**: Dockerイメージ保存
- **Firestore**: データベース
- **IAM**: サービスアカウント・権限管理

### 8.3 必要な権限
- **Artifact Registry 管理者** (roles/artifactregistry.admin)
- **Cloud Run 管理者** (roles/run.admin)
- **Firestore User** (roles/datastore.user)

### 8.4 環境設定
- **GitHub Secrets**:
  - `GCP_PROJECT_ID`: GCPプロジェクトID
  - `GCP_SERVICE_NAME`: Cloud Runサービス名
  - `GCP_ARTIFACT_REGISTRY_REPO_NAME`: リポジトリ名
  - `GCP_SERVICE_ACCOUNT_KEY`: サービスアカウントキー（JSON）

---

## 9. 運用・保守

### 9.1 監視・ログ
- **Cloud Run ログ**: アプリケーションログ監視
- **Firestore監査ログ**: データベースアクセス監視
- **GitHub Actions**: CI/CD実行履歴

### 9.2 スケーリング
- **Cloud Run**: 自動スケーリング（リクエストベース）
- **Firestore**: 自動スケーリング

### 9.3 バックアップ
- **Firestore**: 自動バックアップ機能
- **ソースコード**: GitHub リポジトリ

---

## 10. 開発手順

### 10.1 初期セットアップ
1. GCPプロジェクト作成
2. 必要なAPIの有効化（Cloud Run, Firestore, Artifact Registry）
3. サービスアカウント作成・権限付与
4. Firestoreデータベース作成
5. Artifact Registryリポジトリ作成
6. GitHub Secrets設定

### 10.2 ローカル開発
```bash
# 仮想環境作成・有効化
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 依存関係インストール
pip install -r requirements.txt

# アプリケーション起動
python main.py
```

### 10.3 デプロイ
```bash
# mainブランチにpush
git add .
git commit -m "feature: new functionality"
git push origin main

# GitHub Actionsが自動実行
# → Cloud Runに自動デプロイ
```

---

## 11. トラブルシューティング

### 11.1 よくある問題
1. **Service Unavailable**: Flaskルート定義の構文エラー
2. **Internal Server Error**: Firestore認証エラー
3. **Repository not found**: Artifact Registry未作成
4. **Permission Denied**: サービスアカウント権限不足

### 11.2 デバッグ手順
1. Cloud Run ログ確認
2. GitHub Actions 実行ログ確認
3. サービスアカウント権限確認
4. Firestore接続状況確認

---

## 12. 今後の拡張予定

### 12.1 機能拡張
- [ ] ユーザー認証機能
- [ ] タスクカテゴリ機能
- [ ] 期限設定・通知機能
- [ ] タスク検索・フィルタ機能
- [ ] チーム共有機能

### 12.2 技術的改善
- [ ] テストコード追加
- [ ] パフォーマンス最適化
- [ ] セキュリティ強化
- [ ]監視・アラート機能

---

## 13. 参考資料

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Google Cloud Firestore Documentation](https://cloud.google.com/firestore/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)

---

**最終更新**: 2025年5月27日  
**作成者**: Development Team  
**バージョン**: 1.0

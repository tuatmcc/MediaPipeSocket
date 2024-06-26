# MediaPipe Socket

This is a simple python script that allows you to send data from MediaPipe to a UDP socket.

ウェブカメラを起動し、メディアパイプポーズで全身のポーズ検出、取得された体の 33 個のランドマーク(三次元座標+visibility)をローパスフィルターを通して自身の UDP ソケットに送信します。

デフォルトではローカルホストのポート 8080 に送信されます。

## 環境構築

複数方法があります。

- [`pip`でグローバルにパッケージをインストールする方法](#pipでグローバルにパッケージをインストールする方法): 簡単ですが非推奨。
- [`venv`と`pip`で仮想環境にパッケージをインストールする方法](#venvとpipで仮想環境にパッケージをインストールする方法): 仮想環境を使うことで、他のプロジェクトと PyPI パッケージの衝突を防ぐことができます。Python の標準です。推奨
- [`rye`で仮想環境にパッケージをインストールする方法](#ryeで仮想環境にパッケージをインストールする方法): これで作成されました。上記よりプロジェクト管理および Python 環境管理に優れます。オススメです.
- `poetry`で仮想環境にパッケージをインストールする方法: 未検証です。Python依存なので大変そう
- その他仮想環境を使う方法: 自分でやってください。

**注意**: 以下の`python`コマンドは、`python3`です。自分の環境に応じて`py`や`python3`に置き換えてください。

2, 3 の方法は動作確認済み。`pip`のバージョンが古いと動かないかもしれません。

### `pip`でグローバルにパッケージをインストールする方法

`pip install -r requirements.lock`で`requirements.lock`に記載されているパッケージをインストールします。

まったくオススメしません。

### `venv`と`pip`で仮想環境にパッケージをインストールする方法

```bash
python -m venv .venv
pip install -r requirements.lock # 依存関係をインストール
source .venv/bin/activate # 仮想環境に入る
```

### `rye`で仮想環境にパッケージをインストールする方法

[rye](https://rye-up.com/guide/installation/)をインストールします。Linux(WSL)の場合は以下。Windows の場合公式から `.exe` ファイルをダウンロードしてください。(`cargo`でビルドでも可)

- WSL Ubuntu

```bash
curl -sSf https://rye-up.com/get | bash
```

- Windows
```pwsh
scoop install rye
```

or

```
cargo install --git https://github.com/astral-sh/rye rye
```

- ArchLinux

```
yay -S rye
```

- Mac or Any Other Linux
```
brew install rye
```

~~公式のインストールガイドでは、この後`echo 'source "$HOME/.rye/env"' >> ~/.bashrc`を実行するように書かれていますが、これを実行すると、既存の Python の環境と衝突する可能性があります。~~ WSL で検証したところ、必要そうでした。

```bash
rye sync # 依存関係をインストール
rye shell # 仮想環境に入る
```

## 使い方

### 指定のIPに固定してある場合(本番用)

```bash
rye run all
```

or

```bash
python mediapipe_socket
```

### ローカルホストで動かす場合(開発用)

```
rye run local
```

or

```
python mediapipe_socket --ip_address "127.0.0.1"
```

`-h`オプションで利用可能なコマンドライン引数を確認できます。

## デバックモードと通常モードの切り替え

- `D`キーを押すことでデバッグモードに切り替えることができます。
- デバックモードでは、予め用意した画像を読み込んでカメラ入力の代わりに利用することができます。
- 複数の画像を読み込んでいる場合は`数字`キー(`0`~`9`)を押すことで画像の切り替えができます。
- `filenames`に書かれている順番で画像に`0`から`9`の番号が割り振られます。この番号と`数字`キーの数字が対応しています。
- デフォルトでは`0`キーに対応する画像が最初に表示されるようになっています。変更する場合は`filenames`の順番を書き換えてください。
- `R`キーを押すことでデバックモードを終了してカメラ入力に戻すことができます。

## デバッグ画像の読込

- デバッグ画像を追加で読み込みたい場合は、画像を`debugImages`フォルダの直下に追加して、`debug.py`内の`filenames`に追加した画像のファイル名を追加してください。
```
#debug.py

filenames: List[str] = [
    "T-pose.png",
    "X-pose.png",
    #ここに追加(拡張子も書いてください。)
]
```

## 開発環境

- `pylance(pyright)`: 言語サーバー・型チェッカー
- `black`: フォーマッター
- `isort`: importのソート
- `flake8`: リンター
- `tox`: 自動化

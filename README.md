# MediaPipe Socket

This is a simple python script that allows you to send data from MediaPipe to a UDP socket.

ウェブカメラを起動し、メディアパイプポーズで全身のポーズ検出、取得された体のランドマーク(三次元座標+visibility)を自身の UDP ソケットに送信します。

デフォルトではローカルホストのポート 5000 に送信されます。

## 環境構築

複数方法があります。

- [`pip`でグローバルにパッケージをインストールする方法](#`pip`でグローバルにパッケージをインストールする方法): 簡単ですが非推奨。
- [`venv`と`pip`で仮想環境にパッケージをインストールする方法](#`pip`で仮想環境にパッケージをインストールする方法): 仮想環境を使うことで、他のプロジェクトと PyPI パッケージの衝突を防ぐことができます。Python の標準です。推奨
- [`rye`で仮想環境にパッケージをインストールする方法](#`rye`で仮想環境にパッケージをインストールする方法): これで作成されました。上記よりプロジェクト管理および Python 環境管理に優れます。オススメです.
- `poetry`で仮想環境にパッケージをインストールする方法: 未検証です。
- その他仮想環境を使う方法: 自分でやってください。

**注意**: 以下の`python`コマンドは、`python3`です。`python`が`python2`の場合は、`python3`に置き換えてください。

以下に一部方法の説明を示します。`rye`以外は動作確認していません。

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

[rye](https://rye-up.com/guide/installation/)をインストールします。Linux(WSL)の場合は以下。

```bash
curl -sSf https://rye-up.com/get | bash
```

~~公式のインストールガイドでは、この後`echo 'source "$HOME/.rye/env"' >> ~/.bashrc`を実行するように書かれていますが、これを実行すると、既存の Python の環境と衝突する可能性があります。~~ WSL で検証したところ、必要そうでした。

```bash
rye sync # 依存関係をインストール
rye shell # 仮想環境に入る
```

## 使い方

`mediapipe_socket/__main__.py`に実行部分があります。

```bash
rye run main
```

or

```bash
python mediapipe_socket
```

`--debug`オプションをつけると、キャプチャした様子をウィンドウに表示します。`-h`オプションでその他のオプションを確認できます。
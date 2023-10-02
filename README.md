# MediaPipe Socket

This is a simple python script that allows you to send data from MediaPipe to a UDP socket.

ウェブカメラを起動し、メディアパイプポーズで全身のポーズ検出、取得された体のランドマーク(三次元座標+visibility)を自身の UDP ソケットに送信します。

デフォルトではローカルホストのポート 5000 に送信されます。

## 環境構築

複数方法があります。

- [`pip`でグローバルにパッケージをインストールする方法](#`pip`でグローバルにパッケージをインストールする方法): 一番簡単ではあります。
- [`pip`で仮想環境にパッケージをインストールする方法](#`pip`で仮想環境にパッケージをインストールする方法): 仮想環境を使うことで、他のプロジェクトとの衝突を防ぐことができます。
- [`rye`で仮想環境にパッケージをインストールする方法](#`rye`で仮想環境にパッケージをインストールする方法): より整備された仮想環境を使うことができます。この方法で作成されたため、この方法を推奨します。
- `poetry`で仮想環境にパッケージをインストールする方法: `pyproject.toml`があるのでたぶん使えます。
- その他仮想環境を使う方法: 自分でやってください。

**注意**: 以下の`python`コマンドは、`python3`です。`python`が`python2`の場合は、`python3`に置き換えてください。

以下に一部方法の説明を示します。`rye`以外は動作確認していません。

### `pip`でグローバルにパッケージをインストールする方法

`requirements.lock`に記載されているパッケージをインストールします。

### `pip`で仮想環境にパッケージをインストールする方法

```bash
python -m pip install virtualenv
python -m venv venv
pip install -r requirements.lock
```

### `rye`で仮想環境にパッケージをインストールする方法

[rye](https://rye-up.com/guide/installation/)をインストールします。Linux(WSL)の場合は以下。

```bash
curl -sSf https://rye-up.com/get | bash
```

公式のインストールガイドでは、この後`echo 'source "$HOME/.rye/env"' >> ~/.bashrc`を実行するように書かれていますが、これを実行すると、既存の Python の環境と衝突する可能性があります。

```bash
rye sync # 依存関係をインストール
rye shell # 仮想環境に入る
```

## 使い方

`src/main.py`を実行します。

```bash
python src/main.py
```

or

```bash
rye run main
```

`--debug`オプションをつけると、キャプチャした様子をウィンドウに表示します。`--help`オプションでその他のオプションを確認できます。

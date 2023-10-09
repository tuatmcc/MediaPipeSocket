# MediaPipe Socket

This is a simple python script that allows you to send data from MediaPipe to a UDP socket.

ウェブカメラを起動し、メディアパイプポーズで全身のポーズ検出、取得された体の 33 個のランドマーク(三次元座標+visibility)を自身の UDP ソケットに送信します。

デフォルトではローカルホストのポート 5000 に送信されます。

## 環境構築

複数方法があります。

1. [`pip`でグローバルにパッケージをインストールする方法](#`pip`でグローバルにパッケージをインストールする方法): 一番簡単ですが、非推奨。
2. [`pip`で仮想環境にパッケージをインストールする方法](#`pip`で仮想環境にパッケージをインストールする方法): 仮想環境を使うことで、他のプロジェクトとの衝突を防ぐことができます。推奨
3. [`rye`で仮想環境にパッケージをインストールする方法](#`rye`で仮想環境にパッケージをインストールする方法): 上に同じだが、加えて Python 自体のバージョンも管理できる。プロジェクト自体もこれで作成した。個人的に結構推奨。
4. `poetry`で仮想環境にパッケージをインストールする方法: 使えるかも。やりたければ自己責任で。
5. その他仮想環境を使う方法: 同じく自己責任で。

**注意**: 以下の`python`コマンドは、`python3`です。自分の環境に応じて`py`や`python3`に置き換えてください。

2, 3 の方法は動作確認済み。`pip`のバージョンが古いと動かないかもしれません。

### `pip`でグローバルにパッケージをインストールする方法

`requirements.lock`に記載されているパッケージをインストールします。

```bash
pip install -r requirements.lock
```

### `pip`で仮想環境にパッケージをインストールする方法

```bash
python -m pip install virtualenv
python -m venv venv
pip install -r requirements.lock
```

### `rye`で仮想環境にパッケージをインストールする方法

[rye](https://rye-up.com/guide/installation/)をインストールします。Linux(WSL)の場合は以下。Windows の場合公式から `.exe` ファイルをダウンロードしてください。(`cargo`でビルドでも可)

```bash
curl -sSf https://rye-up.com/get | bash
```

~~公式のインストールガイドでは、この後`echo 'source "$HOME/.rye/env"' >> ~/.bashrc`を実行するように書かれていますが、これを実行すると、既存の Python の環境と衝突する可能性があります。~~ WSL で検証してもらったところ、これは必要だった模様。

```bash
rye sync # 依存関係をインストール
rye shell # 仮想環境に入る
```

## 使い方

`src/main.py`を実行します。

```bash
python src/main.py
```

または

```bash
rye run main
```

`--debug`オプションをつけると、キャプチャした様子をウィンドウに表示します。`-h`オプションでその他のオプションを確認できます。

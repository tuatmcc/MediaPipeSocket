# MediaPipe Socket

This is a simple python script that allows you to send data from MediaPipe to a UDP socket.

## 環境構築

**Python の仮想環境に`rye`以外使ったことないので分かりませんが、たぶん`rye`以外でもできます。**

[rye](https://rye-up.com/guide/installation/)をインストールします。Linux(WSL)の場合は以下。

```bash
curl -sSf https://rye-up.com/get | bash
```

公式のインストールガイドでは、この後`echo 'source "$HOME/.rye/env"' >> ~/.bashrc`を実行するように書かれていますが、これを実行すると、既存の Python の環境と衝突する可能性があります。

## Usage

1. リポジトリをクローンして、`cd`で移動します。
2. `rye sync`を実行して仮想環境を作成します。
3. `rye shell`を実行して仮想環境に入ります。
4. `rye run all`(`rye run python src/main.py`)を実行します。
5. カメラとウィンドウが起動し、MediaPipe のデータが localhost の UDP ポート 5000 に送信されます。

- `rye run all --help`で、引数の説明を見ることができます。カメラのサイズやポートの指定などができます。

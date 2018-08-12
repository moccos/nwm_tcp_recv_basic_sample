# nwm_tcp_recv_sample
「Network Maniacs TCP受信基本編」 のサンプルコードリポジトリです。

書籍の詳細: http://networkmaniacs.net/circle/nwm/tcp_recv_basic.html

This is a sample code repository for my book written in Japanese.

## Python3によるサンプルコード

chat_pythonディレクトリ内にあります。

- TCPクライアント

`python3 ./client.py`

- TCPサーバー

`python3 ./server.py`

- TCPサーバー (select版)

`python3 ./server_sel.py`

## Elirirによるサンプルコード

chat_elixirディレクトリ内にあります。

- TCPサーバー

`elixir ./ex_tcp_server.exs`

## Python3によるトイスクリプト

snippet_pythonディレクトリ内にあります。

リターンキーを押すたびに指定サイズのゴミデータを受信または送信するスクリプトです。
数値を入力するとsend()またはrecv()に渡すサイズを変更できます。
送信バッファ、受信バッファのサイズを引数で指定できますので、そのあたりの実験も可能です。


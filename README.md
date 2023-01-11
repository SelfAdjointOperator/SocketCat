# SocketCat

A few simple socket tools. Currently written for `AF_UNIX` and `AF_INET`

## `socket-send.py`

Call `socket-send.py` and type away to connect to a socket and send data from stdin

## `socket-cat.py`

Call `socket-cat.py` to connect to a socket and recv data from it to stdout

Inspired by `cat(1)`

## `socket-write.py`

Call `socket-write.py` to connect to a socket and send and recv data with it. sends stdin to the socket and recvs from the socket to stdout

Inspired by `write(1)`

## `echo-server.py`

Binds to an address and send()s back what it recv()s

Inspired by `echo(1)`

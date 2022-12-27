# UnixSend

## `unix-send.py`

Call `unix-send.py /path/to/socket` and type away to connect to the Unix socket at `/path/to/socket` and send data from stdin

## `unix-cat.py`

Call `unix-cat.py /path/to/socket` to connect to the Unix socket at `/path/to/socket` and recv data from it to stdout

Inspired by `cat(1)`

## `unix-write.py`

Call `unix-write.py /path/to/socket` to connect to the Unix socket at `/path/to/socket` and send and recv data with it. sends stdin to the socket and recvs from the socket to stdout

Inspired by `write(1)`

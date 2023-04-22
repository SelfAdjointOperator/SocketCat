# SocketCat

A few simple tools for connecting to sockets and `send`ing and `recv`ing with them. Currently written for `AF_UNIX` and `AF_INET`

`socket-cat {cat,echo,send,write} {bind,connect} {unix,inet} <socket-address>`

See `socket-cat --help` for full `argparse` help

`$ socket-cat {...} bind {...} <socket-address>` binds to the specified address and runs a socketserver

`$ socket-cat {...} connect {...} <socket-address>` connects to the specified address as a client

## Programs

### `socket-cat send`

Reads from `stdin` and writes to the socket

### `socket-cat cat`

Reads from the socket and writes to `stdout`

Inspired by `cat(1)`

### `socket-cat write`

Reads from `stdin` and writes to the socket

Reads from the socket and writes to `stdout`

This is a nice program for talking to a socket, combining both `send` and `cat`'s abilities

Inspired by `write(1)`

### `socket-cat echo`

Reads from the socket and writes back to the socket

Inspired by `echo(1)`

## Examples

### Talk to HTTPD

Send a simple HTTP/0.9 GET request to Apache running on localhost:80 and get the response

```
$ echo -ne "GET /\r\n\r\n" | ./src/socket-cat.py write connect inet 127.0.0.1 80
```

```
read(): 0 from stdin, calling shutdown(SHUT_WR)
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
...
</html>
recv(): 0 from socket; remote end called shutdown(SHUT_WR)
```

### Echo server

Run an echo server as a systemd unit serving at localhost:9001

```ini
[Service]
Type=forking
ExecStart=/home/jb2170/Repositories/Python/SocketCat/src/socket-cat.py echo bind --fork inet 127.0.0.1 9001
```

And talk to it via

```
$ echo "Hello, World!" | ./src/socket-cat.py write connect inet 127.0.0.1 9001
```

```read(): 0 from stdin, calling shutdown(SHUT_WR)
Hello, World!
recv(): 0 from socket; remote end called shutdown(SHUT_WR)
```

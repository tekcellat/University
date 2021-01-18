# Курсовой проект по ОС, на тему: "Модуль ядра rootkit."
Компилим, не выёживаемся, сдаём :^)
## Linux 
Качаем нужную версию, на всякий х32 оставлю, но работать не должно (вроде).
| Kernel |         x86         |        x86-64        |
|:-------------:|:-------------------:|:--------------------:|
|     4.4.0     | Ubuntu 16.04 i386 (647M) [[torrent]](http://old-releases.ubuntu.com/releases/16.04.0/ubuntu-16.04-server-i386.iso.torrent) [[iso]](http://old-releases.ubuntu.com/releases/16.04.0/ubuntu-16.04-server-i386.iso) |  Ubuntu 16.04 amd64 (655M) [[torrent]](http://old-releases.ubuntu.com/releases/16.04.0/ubuntu-16.04-server-amd64.iso.torrent) [[iso]](http://old-releases.ubuntu.com/releases/16.04.0/ubuntu-16.04-server-amd64.iso) |

### Далее на всякий:
```sh
sudo apt-get update
sudo apt install linux-headers-$(uname -r)
```
### Building

```sh
make
```

## Use

Load rootkit:

```sh
make load
```
Unload rootkit:

```sh
make unload
```
**Usage**
После `make load` вводим в терминале, а далее сюда же вписываем команды.
```sh
nc -4 -u localhost 8071
```
8071 задан как порт по умолчанию, при сильном желании, его можно сменить, на строчке 28 `UDP_PORT`, в файле `include.h`.
**Смена приритета по PID**
Проверить PID можно например `top`
```sh
escalate-PID
deescalate-PID
```
**Скрытие модулей**
```sh
hidemod
showmod
```
**Скрытие файлов определённого типа (должны начинаться на rootkit_ или .rootkit_, но во 2м варианте бывают проблемы!)**
```sh
hidefile
showfile
```

Остальное вроде всё нативно. Также есть функции, которые не вошли в РПЗ (по итогу не показал): 
- Скрытие портов (*usage* `hideport-12345` | `showport-12345`)
- Скрытие пакетов (можно чекнуть WireShark'ом)
```sh
hidepacket-udp4-192.168.2.141
hidepacket-udp6-0123:4567:89ab:cdef:0123:4567:89ab:cdef
hidepacket-tcp6-::1
--------------------
showpacket-udp6-0123:4567:89ab:cdef:0123:4567:89ab:cdef
showpacket-tcp6-::1
```
- Скрытие сокетов 
```sh
hidesocket-udp4-12345
hidesocket-udp6-12346
hidesocket-tcp4-12347
hidesocket-tcp6-12348
---------------------
showsocket-udp4-12345
showsocket-udp6-12346
showsocket-tcp4-12347
showsocket-tcp6-12348

```

# Проект для запуска T-Rex сервера внутри GNS3

Здесь собирается Docker-образ сервера, который можно настроить через переменные окружения при запуске в GNS3.

Примечание: если GNS3 тоже работает внутри Docker-контейнера, то этот проект нужно собирать внутри контейнера с GNS3.

# Сборка контейнера

Смотри Makefile.

```bash
make image
```

# Переменные окружения

Все параметры опциональны.

```bash
# Путь к файлу конфигурации который будет сгенерирован (по дефолту: /etc/trex_cfg.yaml):
TREX_CFG_FILE="{PATH}"

# Автоматический запуск bash консоли после запуска сервера (по дефолту: N):
TREX_CFG_SHELL="N|Y"

# Режим работы сервера (по дефолту: STL)
TREX_CFG_MODE="STL|ASTF|EMU"

# Опция для поддержки NAT, значения параметра см. https://trex-tgn.cisco.com/trex/doc/trex_manual.html#_nat_support
TREX_CFG_LEARN_MODE=""

# Интерфейс для подключения к серверу (по дефолту: eth0):
TREX_CFG_CTL_IFACE="{IFACE}"

# IP адрес сервера:
TREX_CFG_CTL_IFACE_IP="{IPV4_ADDR}/{LEN}"
# Default Gateway для управляющего трафика:
TREX_CFG_CTL_IFACE_GW="{IPV4_ADDR}"

# zmq_pub_port, см. https://trex-tgn.cisco.com/trex/doc/trex_manual.html#_platform_yaml_cfg_argument
TREX_CFG_CTL_ZQM="{NUM}"
# zmq_rpc_port, см. https://trex-tgn.cisco.com/trex/doc/trex_manual.html#_platform_yaml_cfg_argument
TREX_CFG_CTL_ZQM_STL="{NUM}"
# Порт EMU, который прослушивает сервер в режиме EMU
TREX_CFG_CTL_EMU="{NUM}"

# Параметры интерфейсов генерирующих трафик (пользователи).

# Дефолтный TREX_CFG_SRC_IFACE: eth1
TREX_CFG_SRC_IFACE="{IFACE} {IFACE} ..."
TREX_CFG_SRC_IFACE_VLAN="{VLAN} {VLAN} ..."
TREX_CFG_SRC_IFACE_MAC="{MAC} {MAC} ..."
TREX_CFG_SRC_IFACE_IP="{IPV4_ADDR} {IPV4_ADDR} ..."
TREX_CFG_SRC_IFACE_GW="{IPV4_ADDR} {IPV4_ADDR} ..."
TREX_CFG_SRC_IFACE_DST_MAC="{MAC} {MAC} ..."

# Параметры интерфейсов принимающих трафик (сервисы).

# Дефолтный TREX_CFG_DST_IFACE: eth2
TREX_CFG_DST_IFACE="{IFACE} {IFACE} ..."
TREX_CFG_DST_IFACE_VLAN="{VLAN} {VLAN} ..."
TREX_CFG_DST_IFACE_MAC="{MAC} {MAC} ..."
TREX_CFG_DST_IFACE_IP="{IPV4_ADDR} {IPV4_ADDR} ..."
TREX_CFG_DST_IFACE_GW="{IPV4_ADDR} {IPV4_ADDR} ..."
TREX_CFG_DST_IFACE_DST_MAC="{MAC} {MAC} ..."
```

В конфигурации должно быть одинаковое количество dst и src портов.

# Подключение к серверу

## trex-console

Описание актуально для версии T-Rex 3.05.
После сборки образа в корне этого проекта появится каталог `trex-bin`, там будут лежать бинарники.

Простая команда запуска консоли для подключения к серверу (STL и ASTF режимы):

```bash
# CTL_IP  := IP адрес (без длины) заданный в TREX_CFG_CTL_IFACE_IP

 ./trex-bin/trex-console -s $CTL_IP
```

если сервер в EMU режиме (https://trex-tgn.cisco.com/trex/doc/trex_emu.html):

```bash
# CTL_IP  := IP адрес (без длины) заданный в TREX_CFG_CTL_IFACE_IP

 ./trex-bin/trex-console -s $CTL_IP --emu
```

Если заданы один или несколько параметров CTL портов:

```bash
# CTL_IP        := IP адрес (без длины) заданный в TREX_CFG_CTL_IFACE_IP
# CTL_ZQM       := порт заданный в TREX_CFG_CTL_ZQM
# CTL_ZQM_STL   := порт заданный в TREX_CFG_CTL_ZQM_STL
# CTL_EMU       := порт заданный в TREX_CFG_CTL_EMU

 ./trex-bin/trex-console -s $CTL_IP --emu -p $CTL_ZQM_STL --async_port $CTL_ZQM --emu-server-port $CTL_EMU
```

# Ссылки
https://trex-tgn.cisco.com/trex/doc/
https://trex-tgn.cisco.com/trex/doc/trex_vm_manual.html

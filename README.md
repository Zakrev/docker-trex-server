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

```
Путь к файлу конфигурации который будет сгенерирован (по дефолту: /etc/trex_cfg.yaml):
TREX_CFG_FILE="{PATH}"

Автоматический запуск bash консоли после запуска сервера (по дефолту: N):
TREX_CFG_SHELL="N|Y"

Режим работы сервера (по дефолту: STL)
TREX_CFG_MODE="STL|ASTF|EMU"

Опция для поддержки NAT, см. https://trex-tgn.cisco.com/trex/doc/trex_manual.html#_nat_support
TREX_CFG_LEARN_MODE=""

Интерфейс для подключения к серверу (по дефолту: eth0):
TREX_CFG_CTL_IFACE="{IFACE}"

IP адрес сервера:
TREX_CFG_CTL_IFACE_IP="{IPV4_ADDR}/{LEN}"

Параметры интерфейсов генерирующих трафик (пользователи).

Дефолтный TREX_CFG_SRC_IFACE: eth1
TREX_CFG_SRC_IFACE="{IFACE} {IFACE} ..."
TREX_CFG_SRC_IFACE_VLAN="{VLAN} {VLAN} ..."
TREX_CFG_SRC_IFACE_MAC="{MAC} {MAC} ..."
TREX_CFG_SRC_IFACE_IP="{IPV4_ADDR} {IPV4_ADDR} ..."
TREX_CFG_SRC_IFACE_GW="{IPV4_ADDR} {IPV4_ADDR} ..."
TREX_CFG_SRC_IFACE_DST_MAC="{MAC} {MAC} ..."

Параметры интерфейсов принимающих трафик (сервисы).

Дефолтный TREX_CFG_DST_IFACE: eth2
TREX_CFG_DST_IFACE="{IFACE} {IFACE} ..."
TREX_CFG_DST_IFACE_VLAN="{VLAN} {VLAN} ..."
TREX_CFG_DST_IFACE_MAC="{MAC} {MAC} ..."
TREX_CFG_DST_IFACE_IP="{IPV4_ADDR} {IPV4_ADDR} ..."
TREX_CFG_DST_IFACE_GW="{IPV4_ADDR} {IPV4_ADDR} ..."
TREX_CFG_DST_IFACE_DST_MAC="{MAC} {MAC} ..."
```

В конфигурации должно быть одинаковое количество dst и src портов.

# Ссылки
https://trex-tgn.cisco.com/trex/doc/
https://trex-tgn.cisco.com/trex/doc/trex_vm_manual.html

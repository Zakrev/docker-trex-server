# Скрипт start_container

Docker compose не гарантирует что network будут подключены в правильном порядке, т.е. при запуске контейнера может перепутаться порядок интерфейсов хоста и ethN интерфейсов в контейнере. Скрипт вручную создает network и в правильном порядке подключает к запущенному контейнеру.

## Запуск

Нужно составить файл с конфигурацией (bash-переменные), например `some_trex_config`:

```bash
HOST_TREX_IMAGE="local/trex-server"
HOST_CLIENTS_IFACE="enp2s0.10"
HOST_SERVERS_IFACE="enp2s0.11"

TREX_CFG_MODE="ASTF"
TREX_CFG_SRC_IFACE_IP="10.0.0.2"
TREX_CFG_SRC_IFACE_GW="10.0.0.1"
TREX_CFG_DST_IFACE_IP="20.0.0.2"
TREX_CFG_DST_IFACE_GW="20.0.0.1"

# TREX_CFG_CTL_ZQM="4500"
# TREX_CFG_CTL_ZQM_STL="4501"
# TREX_CFG_CTL_EMU="4510"
```

запустить скрипт:

```bash
./start_container.sh some_trex_config
```

Скрипт создаст контейнер и будет ожидать его завершения.

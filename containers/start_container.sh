#!/bin/bash

source $1

if [ -z "${HOST_TREX_IMAGE}" ] ; then echo "Failed at ${LINENO}" ; exit 1 ; fi
if [ -z "${TREX_CFG_MODE}" ] ; then echo "Failed at ${LINENO}" ; exit 1 ; fi
if [ -z "${HOST_CLIENTS_IFACE}" ] || [ -z "${HOST_SERVERS_IFACE}" ] ; then echo "Failed at ${LINENO}" ; exit 1 ; fi

if [ -z "${TREX_CFG_CTL_ZQM}" ] ; then TREX_CFG_CTL_ZQM="4500" ; fi
if [ -z "${TREX_CFG_CTL_ZQM_STL}" ] ; then TREX_CFG_CTL_ZQM_STL="4501" ; fi

if [ -n "${TREX_CFG_CTL_EMU}" ] ; then TREX_CFG_CTL_EMU="-p ${TREX_CFG_CTL_EMU}:4510" ; fi

ETH1_NETWORK="trex_server_${HOST_CLIENTS_IFACE}_eth1"
ETH2_NETWORK="trex_server_${HOST_SERVERS_IFACE}_eth2"
CONTAINER="trex_server_${HOST_CLIENTS_IFACE}_${HOST_SERVERS_IFACE}"

cleanup()
{
    echo "Cleanup..."
    docker container stop ${CONTAINER} 2>>/dev/null
    docker container rm ${CONTAINER} 2>>/dev/null
    docker network rm ${ETH1_NETWORK} 2>>/dev/null
    docker network rm ${ETH2_NETWORK} 2>>/dev/null
}

fail()
{
    echo "Failed at line $1"
    cleanup
    exit 1
}

start_container()
{
    echo "Start container: ${CONTAINER}"

    docker run --rm -d \
        --name "${CONTAINER}" \
        --cap-add ALL \
 		--privileged \
        --env TREX_CFG_MODE=${TREX_CFG_MODE} \
        --env TREX_CFG_SRC_IFACE_IP=${TREX_CFG_SRC_IFACE_IP} \
        --env TREX_CFG_SRC_IFACE_GW=${TREX_CFG_SRC_IFACE_GW} \
        --env TREX_CFG_DST_IFACE_IP=${TREX_CFG_DST_IFACE_IP} \
        --env TREX_CFG_DST_IFACE_GW=${TREX_CFG_DST_IFACE_GW} \
        -p ${TREX_CFG_CTL_ZQM}:4500 \
        -p ${TREX_CFG_CTL_ZQM_STL}:4501 \
        ${TREX_CFG_CTL_EMU} \
            ${HOST_TREX_IMAGE} || fail ${LINENO}
}

create_networks()
{
    echo "Create network: ${HOST_CLIENTS_IFACE}"

    docker network create -d macvlan \
        -o parent=${HOST_CLIENTS_IFACE} \
        ${ETH1_NETWORK} || fail ${LINENO}

    docker network connect ${ETH1_NETWORK} ${CONTAINER} || fail ${LINENO}

    echo "Create network: ${HOST_SERVERS_IFACE}"

    docker network create -d macvlan \
        -o parent=${HOST_SERVERS_IFACE} \
        ${ETH2_NETWORK} || fail ${LINENO}

    docker network connect ${ETH2_NETWORK} ${CONTAINER} || fail ${LINENO}
}

cleanup
start_container || fail ${LINENO}
create_networks || fail ${LINENO}

echo "Waiting for container: ${CONTAINER}"
docker container wait ${CONTAINER}
cleanup

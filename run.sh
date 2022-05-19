#!/usr/bin/with-contenv bashio

python ./iec62056_to_mqtt.py $(bashio::config 'device_name') $(bashio::config 'serial') $(bashio::services 'mqtt' 'host') $(bashio::services 'mqtt' 'username') $(bashio::services 'mqtt' 'password')

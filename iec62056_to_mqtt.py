#! /usr/bin/env python3

import argparse
import logging
import time

import paho.mqtt.client as mqtt
from iec62056_21.client import Iec6205621Client

logging.basicConfig(format="%(asctime)s:" + logging.BASIC_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

parser = argparse.ArgumentParser(
    description="Publish DSMR P1 telegrams acquired over IEC62056-21 to MQTT"
)
parser.add_argument("device_name", help="MQTT topic prefix")
parser.add_argument("serial", help="Serial device file")
parser.add_argument("mqtt_host", help="MQTT broker address")
args = parser.parse_args()


def on_connect(client, userdata, flags, rc):
    logger.info("Connected to mqtt with result code %s", rc)


client = mqtt.Client()
client.on_connect = on_connect
client.connect(args.mqtt_host)
client.loop_start()

serial = Iec6205621Client.with_serial_transport(port=args.serial)
serial.connect()
logger.info("Connected to iec62056 serial")

while True:
    # Before requesting another standard readout, the transport must be set back
    # to the initial baudrate to send the init sequence.
    # Our physically-available optocoupler, unlike P1 ports, does not continuously
    # send out telegrams.  It instead blinks at 1000blinks/kWh unless a telegram is
    # explicitly requested.
    serial.transport.switch_baudrate(300)

    try:
        r = serial.standard_readout()
    except Exception as e:
        logger.exception("Reading failed, waiting 30s")
        time.sleep(30)
        continue

    for l in r.data:
        t = f"{args.device_name}/iec62056_data_line/{l.address}"
        logger.debug("Publish %s to %s", l.value, t)
        client.publish(t, payload=l.value, qos=1, retain=False)

    # Re-request a new telegram every 60 seconds, to not flood the meter but still
    # get data points relatively often.
    logger.info("Waiting 60 seconds")
    time.sleep(60)

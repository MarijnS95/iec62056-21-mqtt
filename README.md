# IEC 62056-21

Publish DSMR P1 telegrams acquired over IEC62056-21 to MQTT.

`-21` is the "Direct local data exchange" standard, defining how to communicate with meters directly. This is required for "smart" meters that do not feature a physical `RJ12` P1 port but an optocoupler directly on the outside. By default these meters blink 1000 times per kWh, and need to be sent special command sequences from the IEC62056-21 standard to reply with a P1 telegram once (instead of continuously as is common across physical P1 ports).

## Usage

### Directly on HASS

(This is temporary, until the script is converted to a proper integration to supersede manual MQTT switch configuration below).

Clone this repository inside your `/addons` folder, and [install the _local_ addon from the HassIO store](https://my.home-assistant.io/redirect/supervisor_addon/?addon=local_iec62056-21-mqtt).

Set a device name in the configuration tab (used in published data lines as [explained below](###Output)) before starting the addon.

### On an external machine (with access to MQTT)

Install the required dependencies through `pip install -r requirements.txt`, then start the script using:

```console
$ ./iec62056_to_mqtt.py ZCF120ABd 192.168.1.1
```

To run it in the background:

```console
$ nohup ./iec62056_to_mqtt.py ZCF120ABd 192.168.1.1 &
```

### Output

Data lines will be published to `<device_name>/iec62056_data_line/<address>` where `<device_name>` is the first argument passed on the command line and `<address>` is an [OBIS object identifier](https://github.com/lvzon/dsmr-p1-parser/blob/master/doc/IEC-62056-21-notes.md#obis-object-identifiers).

Note that on some meters, such as the `ZCF120ABd`, the `A-B:` prefix is not provided by the meter, only the `C.D.E()` fields are set.

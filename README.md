# devolo-cli
Small cli for devolo powerlan adapters

# Features

- reboot powerlan adapter
- output asset data (config and runtime info about the device, from ntp config to device temperatur and lost segments)

# Supported devices

- Devolo Magic 2 (tested)

# Examples

## Reboot device

```
% devolo-cli reboot 192.168.1.20
<Response [200]>
```

## Get asset data

```
% devolo-cli data 192.168.1.20
AUTHORIZED=Y
AUTHREQUIRED=N
CLOCK.GENERAL.TIME=Sun Dec 18 17:04:41 2022
CLOCK.GENERAL.TIME_ZONE_NAME=Europe/Vienna
COEX.GENERAL.ALIEN_NETWORK_TIME_MAX=50
COEX.GENERAL.ALIEN_NETWORK_TIME_MIN=20
COEX.GENERAL.ALIEN_NETWORK_TIME_PERC=50
COEX.GENERAL.ENABLE_MODE=NO
CONNECTIVITYFB.GENERAL.DEVICE_STATE=0
CONNECTIVITYFB.GENERAL.REDUCE_LEDS=NO
...
```

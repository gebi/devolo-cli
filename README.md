# devolo-cli
Small cli for devolo powerlan adapters

# Usage

I wrote this tool because my Devolo Magic 2 Lan adapters constantly "lock up" in a way no data is transmitted anymore or only with *huge* latencies (like >1min ttl) making the connection unusable, but starting to work again without any issues after just rebooting one of the adapters.

This seems like a SW problem on devolos side which is so far still unfixed...

I have this script running in the background:

`while true; do ping -q 192.168.0.1 -c 3 -W 5 &>/dev/null || (echo -n "### Reboot - "; date; devolo-cli reboot 192.168.0.17; sleep 30); sleep 3 || break; done`

And in more readable form:

```sh
while true; do
  ping -q 192.168.0.1 -c 3 -W 5 &>/dev/null || \
  (
    echo -n "### Reboot - "; date
    devolo-cli reboot 192.168.0.17
    sleep 30
  )
  sleep 3 || break
done
```

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

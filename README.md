RC-RESTserver
=============

RC-RESTserver is a small REST Server written in python. It is designed for Control RF Remote-controlled devices (power sockets / lamp / ..) using several protocols (Chacon / Otio / Blyss / X10)

## Dependencies

Submodules require wiringPi : https://projects.drogon.net/raspberry-pi/wiringpi/

**Building WiringPi**

```bash
sudo apt-get install git-core
git clone git://git.drogon.net/wiringPi
cd wiringPi/wiringPi
./build
```

## Installation 

```bash
git clone --recursive https://github.com/pyrou/RC-RESTserver.git
chmod ugo+x $(pwd)/RC-RESTserver/rcserver.py
ln -s /etc/init.d/rcserver $(pwd)/RC-RESTserver/rcserver.py
/etc/init.d/rcserver start
```

## API

Once the server is running you can perform HTTP requests to control your devices.

### X10 devices

```
GET /x10/{device}/{unit}/{status}.json
```

| Param name | Description | Example |
| --- | :--- | --- |
| `device` | Called also "House code" on some devices, the de device must be a letter between `A` and `P` (case insensitive) | `C` |
| `unit` | This is the "Unit number" and must be a number between `1` and `16` | `3` |
| `status` | `on` or `off` | `on` |

**Example**

To turn on the power socket configured as house code C, unit number 3 ; perform a GET request on the following endpoint :

```
GET /x10/C/3/on.json 
```


### RC Switches devices

This endpoint will use the [rcswitch-pi library](https://github.com/r10r/rcswitch-pi) to control devices with a SC5262 / SC5272, HX2262 / HX2272, PT2262 / PT2272, EV1527, RT1527, FP1527 or HS1527 chipset. Also supports Intertechno outlets.

```
GET /switch/{device}/{unit}/{status}.json
```

| Param name | Description | Example |
| --- | :--- | --- |
| `device` | 5-Bits length mask* of the switch group. |  `10010` |
| `unit` | This is the "Unit number" and must be a number between `1` and `5` | `2` |
| `status` | `on` or `off` | `on` |

**Determine your bit mask and unit number**

Refer to DIP switches 1 to 5 where "1" = on and "0" = off, if all DIP switches are on, `{device}` should be `11111`. Then refer to DIP switches 6 to 10 (A..E) if switche D is on, `{unit}` is `4`.

**Example**

To turn off the power outlet socket configured as group 01001, unit B ; perform a GET request on the following endpoint :

```
GET /switch/01001/2/off.json 
```


```
GET /x10/C/3/on.json 
```


#### Tri-states commands

This endpoint will also use the [rcswitch-pi library](https://github.com/r10r/rcswitch-pi) by sending "tri-states" raw commands.

```
GET /tristate/{command}.json
```

| Param name | Description | Example |
| --- | :--- | --- |
| `command` | Command identifier defined by F, 0 or 1. |  `F0FF011F0011` |

**Example**

```
GET /tristate/F0FF011F0011.json 
```

### Blyss devices

```
GET /blyss/{key}/{channel}/{status}.json
```

| Param name | Description | Example |
| --- | :--- | --- |
| `key` | This is your RF key in hex format. | `0FAE24` |
| `channel` | This is the channel number to control. It must be a number between `1` and `5` | `1` |
| `status` | `on` or `off` | `on` |

**Determine your RF Key**

Determining your RF Key require additionnal components such as a 433Mhz RF Receiver. See complete instruction and code at [skyduino blog (in french)](https://skyduino.wordpress.com/2012/07/19/hack-partie-2-reverse-engineering-des-interrupteurs-domotique-blyss/)

**Example**

To turn on the power socket on channel 1; perform a GET request on the following endpoint :

```
GET /blyss/0FAE24/1/on.json 
```

### UniFi Emoji Fixer

The config file written to UniFi APs by the UniFi Controller is encoded as MUTF-8. This works fine when your 
configuration file is entirely ASCII, but breaks completely when you want to use emojis in your SSID. This script 
fixes the configuration file's encoding.

## Manually Setting an SSID

One way is to disable the network name validation in the webapp in your browser's JavaScript console:

    > delete angular.element('input[name="wirelessNetworkName"]').scope().wirelessNetworkFormCtrl.patterns.name;

You can also directly edit it in the database:

    $ mongo --port 27117
    > use ace;
    > db.wlanconf.update({name: "eggplant"}, {$set: {name: "🍆"}});

## Usage

All script arguments are passed directly to `ssh`:

    $ python3 fix_unifi_ssid.py unifi-ap

If you updated the configuration wirelessly, your SSID will break and you probably will not be able to reconnect to your 
wireless network. If you can remotely SSH into another computer on the same network (and have a recent enough version of 
OpenSSH), you can use it as a jump host to remotely fix the config file:

    $ python3 fix_unifi_ssid.py -J jump-host unifi-ap

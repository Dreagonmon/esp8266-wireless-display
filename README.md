# esp8266-wireless-display

ESP32 wireless display.
based on microython 1.14
![preview](.pc/preview.jpg)

# Install and Useage
Make sure ESP8266 is in the same network.

Add a file named ```config.py```:
```py
# config
wifi_ssid = 'YourWifiName'
wifi_password = 'YourWifiPassword'
```

Use [mpypack](https://github.com/Dreagonmon/mpypack) to upload:
```
mpypack -p PORT sync
```

Use librarys in ```.pc/lib``` folder to write your applications.

The preview image shows the example ```.pc/TruckTelemetry```, a Euro Truck Simulator 2 external display screen.

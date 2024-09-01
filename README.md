# Local Sensor Storage

A program for locally storing sensor data to your local hard drive. New smart home sensors often requires paid for clouds to store data over time (SaaS). This repository stores the data locally on you computer or home server. Just edit the config files and run the program. It is very useful to have on your own home server system and costs you nothing. Currently only camera feeds can be stored, but in near future, other sensors will be added to the system, such as bluetooth, wifi, phones and ZWave LTE devices and sensors.

# How to Run

For running the application in docker:
1. Edit configs.
2. Start docker container `docker-compose up`.
3. Result will be stored in volume `./video`.

For running the application without docker:
1. Install Python3.X. Tested on Python 3.9.
2. Install python packages `pip install -r ./requirements.txt`
3. Edit configs.
4. Run `python ./main.py`
5. Results will be stored in `./video`.

# Key features

* Logging
* Auto detect sensors
* Control storage formats

# Camera Config

In camera config fill in configs for camera recordings.

```python
{
    "subnet":"192.168.1", # subnet to search for cameras
    "ignore-ips": ["192.168.0.1","192.168.0.255"], # ignore these ips
    "RECORD_MAX_TIME":14, # [days] Maximum age of stored videos
    "RECORD_MAX_SIZE":20, # [GB] Total maximum size of stored videos
    "RECORDING_TIME":30, # [Minutes] Amount of minutes in each video
    "STORAGE_FOLDER":"./video", # Storage folder
    "SHOW_STREAM":false, # Show stream while storing, good for debugging
    "VIDEO_WIDTH":720, # Storage video width, to control file size
    "VIDEO_HEIGHT":480, # Storage video height, to control file size
    "FPS":20 # [FPS] Frames per seconds in stored videos
}
```

# Camera Secret Config

In camera secret config, set authorization settings. See example below. The provided authorizations will be used on all cameras until a stable connection can be established.

```python
[
    {"user":"admin",
    "password":"admin",
    "path":"stream1",
    "port":554},
    {"user":"admin",
    "password":"admin",
    "path":"stream2",
    "port":554}, ...
]
```

# License
The project uses MIT License, read more [here](./License).

@Grebtsew
It was announced that SarmaLink service will be discontinued on December 15, 2024. Potentially it may be moved to a new platform, but in order to ensure the continuity of sensor data, and to assist integration of SarmaLink devices into alternative monitoring systems, here is information on how to access the readings over LAN. Do not connect the devices to the public internet.

The data can be retrieved using simple HTTP requests. For the OpenWRT versions of the devices (temperature only) the readings are provided in text format at the following link

http://your.trermom.ip.addr/sarmalink_pull.txt

For humidity probes the data along with diagnostic information can be accessed in JSON file format.

http://your.hygrom.ip.addr/reading.json

The files contain unique device identifiers and readings that can be retrieved and parsed at regular time intervals.

New updates on SarmaLink migration will be posted here.

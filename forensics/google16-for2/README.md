# Google CTF 2016 - for2 Solution

The clue consists of a pcap only. The pcap contains USB packet captures. We identify the type of USB device by using the vendor ID and the product ID which are announced in one of the types of USB packets.

```
root@kali:~/google/for/for2# tshark -r usb.pcap -T fields -e usb.bus_id -e usb.device_address -e usb.idVendor -e usb.idProduct "usb.idVendor > 0" 2>/dev/null
1   3   1133    0x0000c05a
```

We lookup this number online to find it is a Logitech M90/M100  mouse. Ok so mouse movement packets. We also note the second field here which is the USB device_address field.

We know these kinds of packets contain basically x,y and mouse button data in a field called "usb.capdata". Using tshark we can extract it:

```
root@kali:~/google/for/for2# tshark -r capture.pcapng -T fields -e usb.capdata usb.capdata and usb.device_address==3 2> /dev/null | head -5
00:01:fe:00
00:01:ff:00
00:02:00:00
00:03:00:00
00:01:00:00
```

The coordinates are signed integer relative offsets from some initial X,Y position. So values > 127 are negative. 

The first byte indicates whether the left mouse button is down or not.

We write quick python code to extract the coordinates and draw us a picture of every pixel where the mouse button is down.

```
#!/usr/bin/python

from PIL import Image, ImageDraw
from subprocess import check_output

print "[*] Extracting data from pcap"
with open('/dev/null') as DN:
    md = [x.strip() for x in check_output(['tshark','-r','capture.pcapng','-Tfields','-e','usb.capdata','usb.capdata','and','usb.device_address==3'],stderr=DN).splitlines()]

x = 1000    # origin coords
y = 300

img = Image.new("RGB",(1200,800),"white")
dr = ImageDraw.Draw(img)

print "[*] Drawing you a picture!"
for line in md:
    coords = [j if j<128 else (j-256) for j in [int(k,16) for k in line.split(':')]]
    x += coords[1]
    y += coords[2]
    if coords[0] != 0:
        dr.rectangle(((x - 2, y - 2), (x + 2, y + 2)), fill="black")

img.show()
```

A fun problem and a quick solve!


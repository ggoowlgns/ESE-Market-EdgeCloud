import xml.etree.ElementTree as ET
import urllib.request
from bitmath import *


def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
    while size > power:
        size /= power
        n += 1
    return size, power_labels[n]+'bytes'


webPage_xml = urllib.request.urlopen("http://61.253.199.32:81/stat.xml")
webPage_xml = webPage_xml.read().decode("utf-8")

# print(webPage_xml)

root = ET.fromstring(webPage_xml)

# print(root.tag, root.attrib)

bandwidth_per_sec = int(root.findtext("bw_in"))
BW_bits = format_bytes(bandwidth_per_sec)
print(BW_bits)




# R E F
# 1. urllib : https://bigfood.tistory.com/161
# 2. xml parsing : https://118k.tistory.com/215

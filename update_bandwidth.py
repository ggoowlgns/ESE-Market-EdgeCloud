import xml.etree.ElementTree as ET
import urllib.request
from bitmath import *

class UpdateBandwidth:
    def __init__(self):
        self.in_bw = 0
        self.stream_meta = {}


    def format_bytes(self, size):
        # 2**10 = 1024
        power = 2**10
        n = 0
        power_labels = {0 : '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
        while size > power:
            size /= power
            n += 1
        return size, power_labels[n]+'bytes'

    def update_page(self):
        webPage_xml = urllib.request.urlopen("http://61.253.199.32:81/stat.xml")
        webPage_xml = webPage_xml.read().decode("utf-8")

        # print(webPage_xml)

        root = ET.fromstring(webPage_xml)

        # print(root.tag, root.attrib)

        bandwidth_per_sec = int(root.findtext("bw_in"))
        # stream_live = root.find("server")
        stream_list = root.find("server").find("application").find("live").findall("stream")
        stream_name_resolution = {}
        for stream in stream_list:
            stream_name_resolution[stream.findtext("name")] = [stream.find("meta").find("video").findtext("width"),stream.find("meta").find("video").findtext("height")]
        BW_bits = self.format_bytes(bandwidth_per_sec)

        self.in_bw = BW_bits
        self.stream_meta = stream_name_resolution
        # print(stream_name_resolution)
        # print(BW_bits)

    def get_data(self):

        return self.in_bw, self.stream_meta


# R E F
# 1. urllib : https://bigfood.tistory.com/161
# 2. xml parsing : https://118k.tistory.com/215

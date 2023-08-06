import json
import socket
from getmac import get_mac_address
from wget import download as wget_download
from hackpy.settings import *


# Load file from URL
def wget(url, output = None, bar = None):
    return wget_download(url, bar = bar, out = output)

# Get info by ip address
# WARNING! Usage limits:
# This endpoint is limited to 150 requests per minute from an IP address. If you go over this limit your IP address will be blackholed.
# You can unban here: http://ip-api.com/docs/unban
def whois(ip = '', out_tempfile = module_location + r'\tempdata\whois.json'):
    wget_download('http://ip-api.com/json/' + ip, bar = None, out = out_tempfile)
    with open(out_tempfile, "r", encoding = "utf8", errors = 'ignore') as tempfile:
        whois_data = json.load(tempfile)
    try:
        os.remove(out_tempfile)
    except:
        pass
    if whois_data.get('status') == 'success':
        return whois_data
    else:
        raise ConnectionError('Status: ' + ip_data.get('status') + ', Message: ' + ip_data.get('message'))

# Get geodata by ip
def geoplugin(ip = '', out_tempfile = module_location + r'\tempdata\geoplugin.json'):
    wget_download('http://www.geoplugin.net/json.gp?ip=' + ip, bar = None, out = out_tempfile)
    with open(out_tempfile, "r", encoding = "utf8", errors = 'ignore') as tempfile:
        geoplugin_data = json.load(tempfile)
    try:
        os.remove(out_tempfile)
    except:
        pass
    if geoplugin_data.get('geoplugin_status') == 200:
        return geoplugin_data
    else:
        raise ConnectionError('Could not connect to server')

# Get LATITUDE, LONGITUDE, RANGE with bssid
def bssid_locate(bssid, out_tempfile = module_location + r'\tempdata\bssid_locate.json'):
    wget_download('http://api.mylnikov.org/geolocation/wifi?bssid=' + bssid, bar = None, out = out_tempfile)
    with open(out_tempfile, "r", encoding = "utf8", errors = 'ignore') as tempfile:
        bssid_data = json.load(tempfile)
    try:
        os.remove(out_tempfile)
    except:
        pass

    if bssid_data['result'] == 200:
        return bssid_data['data']

# Get router BSSID
def router():
    try:
        SMART_ROUTER_IP = ('.'.join(socket.gethostbyname(socket.gethostname()).split('.')[:-1]) + '.1')
        BSSID = get_mac_address(ip = SMART_ROUTER_IP)
    except:
        return None
    else:
        return BSSID

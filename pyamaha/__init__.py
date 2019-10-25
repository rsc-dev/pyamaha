#!/usr/bin/env python

__author__      = 'Radoslaw Matusiak'
__copyright__   = 'Copyright (c) 2017 Radoslaw Matusiak'
__license__     = 'MIT'
__version__     = '0.3'

import json
import logging
import requests

BAND = ['common', 'am', 'fm', 'dab']
CD_PLAYBACK = ['play', 'stop', 'pause', 'previous', 'next', 'fast_reverse_start', 
               'fast_reverse_end', 'fast_forward_start', 'fast_forward_end', 'track_select ']
DIR = ['next', 'previous']
PLAYBACK = ['play', 'stop', 'pause', 'play_pause', 'previous', 'next', 'fast_reverse_start', 
            'fast_reverse_end', 'fast_forward_start', 'fast_forward_end']
PRESET_BAND = ['common', 'separate']
ZONES = ['main', 'zone2', 'zone3', 'zone4']
SERVICE_INFO_TYPE = ['account_list', 'licensing', 'activation_code']
SLEEP = [0, 30, 60, 90, 120]
TUNING = ['up', 'down', 'cancel', 'auto_up', 'auto_down', 'tp_up', 'tp_down', 'direct']
TYPE = ['select', 'play', 'return']
POWER = ['on', 'standby', 'toggle']
LIST_ID = ['main', 'auto_complete', 'search_artist', 'search_track']
LANG = ['en', 'ja', 'fr', 'de', 'es', 'ru', 'it', 'zh']
WIFI = ['none', 'wep', 'wpa2-psk(aes)', 'mixed_mode']
WIFI_DIRECT = ['none', 'wpa2-psk(aes)']
STANDBY = ['off', 'on', 'auto']

RESPONSE_CODE = {
    0: 'Successful request',
    1: 'Initializing',
    2: 'Internal Error',
    3: 'Invalid Request (A method did not exist, a method wasn\'t appropriate etc.)',
    4: 'Invalid Parameter (Out of range, invalid characters etc.)',
    5: 'Guarded (Unable to setup in current status etc.)',
    6: 'Time Out',
    99: 'Firmware Updating',
    100: 'Access Error',
    101: 'Other Errors',
    102: 'Wrong User Name',
    103: 'Wrong Password',
    104: 'Account Expired',
    105: 'Account Disconnected/Gone Off/Shut Down',
    106: 'Account Number Reached to the Limit',
    107: 'Server Maintenance',
    108: 'Invalid Account',
    109: 'License Error',
    110: 'Read Only Mode',
    111: 'Max Stations',
    112: 'Access Denied'
}


class Device():
    """
    Yamaha device abstraction class.
    """
    
    def __init__(self, ip):
        """Ctor.
        
        Arguments:
            ip -- Yamaha device IP.
        """
        self.ip = ip
    # end-of-method __init__
    
    def request(self, *args):
        """Request YamahaExtendedControl API URI.
        
        Arguments:
            args -- URI link for GET or tupple (URI, data) for POST.
        """
        
        # If it is only a URI, send GET...
        if isinstance(args[0], str):
            return self.get(args[0])
        else:
            # ...otherwise unpack tuple and send POST
            return self.post(*(args[0]))
    # end-of-method request
    
    def get(self, uri):
        """Request given URI. Returns response object.
        
        Arguments:
            uri -- URI to request
        """
        r = requests.get(uri.format(host=self.ip))
        return r
    # end-of-method request    
    
    def post(self, uri, data):
        """Send POST request. Returns response object.
        
        Arguments:
            uri -- URI to send POST
            data -- POST data
        """
        r = requests.post(uri.format(host=self.ip), data=json.dumps(data))
        return r
    # end-of-method post    
    
    pass
# end-of-class Device    


class Dist():
    """APIs in regard to Link distribution related setting and getting information."""
    
    URI = {
        'GET_DISTRIBUTION_INFO': 'http://{host}/YamahaExtendedControl/v1/dist/getDistributionInfo',
        'SET_SERVER_INFO': 'http://{host}/YamahaExtendedControl/v1/dist/setServerInfo',
        'SET_CLIENT_INFO': 'http://{host}/YamahaExtendedControl/v1/dist/setClientInfo',
        'START_DISTRIBUTION': 'http://{host}/YamahaExtendedControl/v1/dist/startDistribution?num={num}',
        'STOP_DISTRIBUTION': 'http://{host}/YamahaExtendedControl/v1/dist/stopDistribution',
        'SET_GROUP_NAME': 'http://{host}/YamahaExtendedControl/v1/dist/setGroupName',
    }
    
    @staticmethod
    def get_distribution_info():
        """For retrieving a Device information related to Link distribution.
        """
        return Dist.URI['GET_DISTRIBUTION_INFO']
    # end-of-method get_distribution_info
    
    @staticmethod
    def set_server_info(group_id, zone=None, type=None, client_list=None):
        """For setting a Link distribution server (Link master).
        
        Arguments:
            group_id -- Specify Group ID in 32-digit hex.
                        Specify "" (empty text) here to cancel a Device being the Link
                        distribution server. Group ID will be initialized ("000...")
                        after the cancel operation.
            zone -- Specifies which target Zone ID to be the Link distribution
                    server. If nothing is specified, current setting is kept. Zone
                    ID to be the Link distribution server is confirmable using
                    system/getFeatures server_zone_list.
                    Values: "main" / "zone2" / "zone3" / "zone4"
            type -- Specifies a type of adding or removing clients. Not necessary
                    to specify when canceling the Link master status.
                    Values: "add" / "remove"
            client_list -- Specifies IP addresses of adding/removing clients. Specifiable
                           up to 9 clients
        """
        data = {}
        
        data['group_id'] = group_id
        
        if zone is not None:
            data['zone'] = zone
            
        if type is not None:
            data['type'] = type
            
        if client_list is not None:
            data['client_list'] = client_list
            
        return Dist.URI['SET_SERVER_INFO'], data
    # end-of-method set_server_info
    
    @staticmethod
    def set_client_info(group_id, zone=None, server_ip_address=None):
        """For setting Link distributed clients. If a Device is already setup as Link distribution server, this
           client setup is denied by that Device: use this API after canceling a Device's Link distribution
           server setup using setServerInfo, then confirming that the target Device's role is changed to other
           values than "server" using getDistributionInfo.
           
        Arguments:
            group_id -- Specifies Group ID in 32-digit hex.
                        Specify "" (empty text) here to cancel a Device being a Link
                        distributed client. Group ID will be initialized ("000...") after
                        the cancel operation.
            zone -- Specifies which target Zone ID to be a Link distributed
                    client. Not necessary to specify when cancelling a client status.
                    Values: "main" / "zone2" / "zone3" / "zone4"
            server_ip_address -- Specifies the IP Address of the Link distribution server.
        """
        data = {}
        
        data['group_id'] = group_id
        
        if zone is not None:
            data['zone'] = zone
        
        if server_ip_address is not None:
            data['server_ip_address'] = server_ip_address
            
        return Dist.URI['SET_CLIENT_INFO'], data
    # end-of-method set_client_info
    
    @staticmethod
    def start_distribution(num):
        """For initiating Link distribution. 
        This is valid to a Device that is setup as Link distribution server.
        
        Arguments:
            num -- Specifies Link distribution number on current MusicCast Network.
        """
        return Dist.URI['START_DISTRIBUTION'].format(host='{host}', num=num)
    # end-of-method start_distribution
    
    @staticmethod
    def stop_distribution():
        """For quitting Link distribution. 
        This is valid to a Device that is setup as Link distribution server.
        """
        return Dist.URI['STOP_DISTRIBUTION']
    # end-of-method stop_distribution
    
    @staticmethod
    def set_group_name(name):
        """For setting up Group Name. 
        Note that Group Name is reserved in volatile memory.
        
        Arguments:
            name -- Specifies Group Name. Use UTF-8 within 128 bytes. Default name
                    would be used if it's not setup or "" (empty text) is specified.
        """
        data = {}
        
        data['name'] = name
        
        return Dist.URI['SET_GROUP_NAME'], data
    # end-of-method set_group_name
    
    pass
# end-of-class Dist


class System():
    """System commands."""
    
    URI = {
        'GET_DEVICE_INFO': 'http://{host}/YamahaExtendedControl/v1/system/getDeviceInfo',
        'GET_FEATURES': 'http://{host}/YamahaExtendedControl/v1/system/getFeatures',
        'GET_NETWORK_STATUS': 'http://{host}/YamahaExtendedControl/v1/system/getNetworkStatus',
        'GET_FUNC_STATUS': 'http://{host}/YamahaExtendedControl/v1/system/getFuncStatus',
        'SET_AUTOPOWER_STANDBY': 'http://{host}/YamahaExtendedControl/v1/system/setAutoPowerStandby?enable={enable}',
        'GET_LOCATION_INFO': 'http://{host}/YamahaExtendedControl/v1/system/getLocationInfo',
        'SEND_IR_CODE': 'http://{host}/YamahaExtendedControl/v1/system/sendIrCode?code={code}',
        'SET_WIRED_LAN': 'http://{host}/YamahaExtendedControl/v1/system/setWiredLan',
        'SET_WIRELESS_LAN': 'http://{host}/YamahaExtendedControl/v1/system/setWirelessLan',
        'SET_WIRELESS_DIRECT': 'http://{host}/YamahaExtendedControl/v1/system/setWirelessDirect',
        'SET_IP_SETTINGS': 'http://{host}/YamahaExtendedControl/v1/system/setIpSettings',
        'SET_NETWORK_NAME': 'http://{host}/YamahaExtendedControl/v1/system/setNetworkName',
        'SET_AIRPLAY_PIN': 'http://{host}/YamahaExtendedControl/v1/system/setAirPlayPin',
        'GET_MAC_ADDRESS_FILTER': 'http://{host}/YamahaExtendedControl/v1/system/getMacAddressFilter',
        'SET_MAC_ADDRESS_FILTER': 'http://{host}/YamahaExtendedControl/v1/system/setMacAddressFilter',
        'GET_NETWORK_STANDBY': 'http://{host}/YamahaExtendedControl/v1/system/getNetworkStandby',
        'SET_NETWORK_STANDBY': 'http://{host}/YamahaExtendedControl/v1/system/setNetworkStandby?standby={standby}',
        'GET_BLUETOOTH_INFO': 'http://{host}/YamahaExtendedControl/v1/system/getBluetoothInfo',
        'SET_BLUETOOTH_STANDBY': 'http://{host}/YamahaExtendedControl/v1/system/setBluetoothStandby?enable={enable}',
        'SET_BLUETOOTH_TX_SETTING': 'http://{host}/YamahaExtendedControl/v1/system/setBluetoothTxSetting?enable={enable}',
        'GET_BLUETOOTH_DEVICE_LIST': 'http://{host}/YamahaExtendedControl/v1/system/getBluetoothDeviceList',
        'UPDATE_BLUETOOTH_DEVICE_LIST': 'http://{host}/YamahaExtendedControl/v1/system/updateBluetoothDeviceList',
        'CONNECT_BLUETOOTH_DEVICE': 'http://{host}/YamahaExtendedControl/v1/system/connectBluetoothDevice?address={address}',
        'DISCONNECT_BLUETOOTH_DEVICE': 'http://{host}/YamahaExtendedControl/v1/system/disconnectBluetoothDevice',
        'SET_SPEAKER_A': 'http://{host}/YamahaExtendedControl/v1/system/setSpeakerA?enable={enable}',
        'SET_SPEAKER_B': 'http://{host}/YamahaExtendedControl/v1/system/setSpeakerB?enable={enable}',
        'SET_DIMMER': 'http://{host}/YamahaExtendedControl/v1/system/setDimmer?value={value}',
        'SET_ZONE_B_VOLUME_SYNC': 'http://{host}/YamahaExtendedControl/v1/system/setZoneBVolumeSync?enable={enable}',
        'SET_HDMI_OUT_1': 'http://{host}/YamahaExtendedControl/v1/system/setHdmiOut1?enable={enable}',
        'SET_HDMI_OUT_2': 'http://{host}/YamahaExtendedControl/v1/system/setHdmiOut2?enable={enable}',
        'GET_NAME_TEXT': 'http://{host}/YamahaExtendedControl/v1/system/getNameText?id={id}',
        'SET_NAME_TEXT': 'http://{host}/YamahaExtendedControl/v1/system/setNameText'
    }

    @staticmethod
    def get_device_info():
        """For retrieving basic information of a Device.
        """
        return System.URI['GET_DEVICE_INFO']
    # end-of-method get_device_info

    @staticmethod
    def get_features():
        """For retrieving feature information equipped with a Device.
        """
        return System.URI['GET_FEATURES']
    # end-of-method get_features

    @staticmethod
    def get_network_status():
        """For retrieving network related setup/information.
        """
        return System.URI['GET_NETWORK_STATUS']
    # end-of-method get_network_status

    @staticmethod
    def get_func_status():
        """For retrieving setup/information of overall system function. 
        Parameters are readable only when corresponding functions are available in "func_list" of /system/getFeatures.
        """
        return System.URI['GET_FUNC_STATUS']
    # end-of-method get_func_status

    @staticmethod
    def set_autopower_standby(enable=True):
        """For setting Auto Power Standby status. 
        Actual operations/reactions of enabling Auto Power Standby depend on each Device.
        
        Arguments:
        enable -- Specifies Auto Power Standby status.
        """
        return System.URI['SET_AUTOPOWER_STANDBY'].format(host='{host}', enable=_bool_to_str(enable))
    # end-of-method set_autopower_standby

    @staticmethod
    def get_location_info():
        """For retrieving Location information.
        """
        return System.URI['GET_LOCATION_INFO']
    # end-of-method get_location_info

    @staticmethod
    def send_ir_code(code):
        """For sending specific remote IR code. 
        A Device is operated same as remote IR code reception. But continuous IR code cannot be used in this command. 
        Refer to each Device's IR code list for details..
        
        Arguments:
        code -- Specifies IR code in 8-digit hex.
        """
        return System.URI['SEND_IR_CODE'].format(host='{host}', code=code)
    # end-of-method send_ir_code

    @staticmethod
    def set_wired_lan(dhcp=None, ip_address=None, subnet_mask=None, default_gateway=None, dns_server_1=None, dns_server_2=None):
        """For setting Wired Network. Network connection is switched to wired by using this API. If no
        parameter is specified, current parameter is used. If set parameter is incomplete, it is possible not
        to provide network avalability.
        
        Arguments:
        dhcp -- Specifies DHCP setting.
        ip_address -- Specifies IP Address.
        subnet_mask -- Specifies Subnet Mask.
        default_gateway -- Specifies Default Gateway.
        dns_server_1 -- Specifies DNS Server 1.
        dns_server_2 -- Specifies DNS Server 2.
        """
        data = {}
        
        if dhcp is not None:
            data['dhcp'] = dhcp
            
        if ip_address is not None:
            data['ip_address'] = ip_address
           
        if subnet_mask is not None:
            data['subnet_mask'] = subnet_mask
            
        if default_gateway is not None:
            data['default_gateway'] = default_gateway
            
        if dns_server_1 is not None:
            data['dns_server_1'] = dns_server_1
        
        if dns_server_2 is not None:
            data['dns_server_2'] = dns_server_2
        
        return System.URI['SET_WIRED_LAN'].format(host='{host}'), data
    # end-of-method set_wired_lan
    
    @staticmethod
    def set_wireless_lan(ssid=None, type=None, key=None, dhcp=None, ip_address=None, 
                         subnet_mask=None, default_gateway=None, dns_server_1=None, dns_server_2=None):
        """For setting Wireless Network (Wi-Fi). Network connection is switched to wireless (Wi-Fi) by using
        this API. If no parameter is specified, current parameter is used. If set parameter is incomplete, it
        is possible not to provide network avalability.
        """
        data = {}
        
        if ssid is not None:
            data['ssid'] = ssid
            
        if type is not None:
            assert type in WIFI, 'Invalid TYPE value!'
            data['type'] = type
           
        if key is not None:
            data['key'] = key
            
        if dhcp is not None:
            data['dhcp'] = dhcp
            
        if ip_address is not None:
            data['ip_address'] = ip_address
        
        if subnet_mask is not None:
            data['subnet_mask'] = subnet_mask
            
        if default_gateway is not None:
            data['default_gateway'] = default_gateway
            
        if dns_server_1 is not None:
            data['dns_server_1'] = dns_server_1

        if dns_server_2 is not None:
            data['dns_server_2'] = dns_server_2    
        
        return System.URI['SET_WIRELESS_LAN'].format(host='{host}'), data
    # end-of-method set_wireless_lan
    
    @staticmethod
    def set_wireless_direct(type=None, key=None):
        """For setting Wireless Network (Wireless Direct). Network connection is switched to wireless
        (Wireless Direct) by using this API. If no parameter is specified, current parameter is used. If set
        parameter is incomplete, it is possible not to provide network avalability.
        """
        data = {}
        
        if type is not None:
            assert type in WIFI_DIRECT, 'Invalid TYPE value!'
            data['type'] = type
            
        if key is not None:
            data['key'] = key
            
        return System.URI['SET_WIRELESS_DIRECT'].format(host='{host}'), data
    # end-of-method set_wireless_direct
    
    @staticmethod
    def set_ip_settings(dhcp, ip_address, subnet_mask, default_gateway, dns_server_1, dns_server_2):
        """For setting IP. This API only set IP as maintain same network connection status (Wired/Wireless
        Lan/Wireless Direct/Extend). If no parameter is specified, current parameter is used. If set
        parameter is incomplete, it is possible not to provide network avalability.
        """
        data = {}
        
        if dhcp is not None:
            data['dhcp'] = dhcp
            
        if ip_address is not None:
            data['ip_address'] = ip_address
           
        if subnet_mask is not None:
            data['subnet_mask'] = subnet_mask
            
        if default_gateway is not None:
            data['default_gateway'] = default_gateway
            
        if dns_server_1 is not None:
            data['dns_server_1'] = dns_server_1
        
        if dns_server_2 is not None:
            data['dns_server_2'] = dns_server_2
        
        return System.URI['SET_WIRED_LAN'].format(host='{host}'), data
    # end-of-method set_ip_settings
    
    @staticmethod
    def set_network_name(name):
        """For setting Network Name (Friendly Name)"""
        return System.URI['SET_NETWORK_NAME'].format(host='{host}'), {'name': name}
    # end-of-method set_network_name
    
    @staticmethod
    def set_airplay_pin(pin):
        """For setting AirPlay PIN. This is valid only when "airplay" exists in "func_list" found in
        /system/getFuncStatus.
        """
        return System.URI['SET_AIRPLAY_PIN'].format(host='{host}'), {'pin': pin}
    # end-of-method set_airplay_pin
    
    @staticmethod
    def get_mac_address_filter():
        """For retrieving setup of MAC Address Filter"""
        return System.URI['GET_MAC_ADDRESS_FILTER']
    # end-of-method get_mac_address_filter
    
    @staticmethod
    def set_mac_address_filter(filter, *macs):
        """For setting MAC Address Filter"""
        data = {}
        data['filter'] = filter
        
        for i, address in enumerate(macs):
            data['address_{}'.format(i+1)]
            
            if i >= 9:
                break
        
        return System.URI['SET_MAC_ADDRESS_FILTER'].format(host='{host}'), data
    # end-of-method set_mac_address_filter
    
    @staticmethod
    def get_network_standby():
        """For retrieving setup of Network Standby"""
        return System.URI['GET_NETWORK_STANDBY']
    # end-of-method get_network_standby
    
    @staticmethod
    def set_network_standby(standby):
        """For setting Network Standby"""
        assert standby in STANDBY, 'Invalid STANDBY value!'
        return System.URI['SET_NETWORK_STANDBY'].format(host='{host}', standby=standby)
    # end-of-method set_network_standby
    
    @staticmethod
    def get_bluetooth_info():
        """For retrieving setup/information of Bluetooth. Parameters are readable only when corresponding
        functions are available in "func_list" of /system/getFuncStatus. "bluetooth_device" parameter is
        contained in "bluetooth_tx_setting".
        """
        return System.URI['GET_BLUETOOTH_INFO']
    # end-of-method get_bluetooth_info
    
    @staticmethod
    def set_bluetooth_standby(enable=True):
        """For setting Bluetooth Standby"""
        return System.URI['SET_BLUETOOTH_STANDBY'].format(host='{host}', enable=_bool_to_str(enable))
    # end-of-method set_bluetooth_standby
    
    @staticmethod
    def set_bluetooth_tx_setting(enable=True):
        """For setting Bluetooth transmission"""
        return System.URI['SET_BLUETOOTH_TX_SETTING'].format(host='{host}', enable=_bool_to_str(enable))
    # end-of-method set_bluetooth_tx_setting

    @staticmethod
    def get_bluetooth_device_list():
        """For retrieving Bluetooth (Sink) device list. This API is available only when "bluetooth_tx_setting"
        is true under /system/getFuncStatus.
        This device list information is in the cach. If update device list information, excute
        /system/updateBluetoothDeviceList.
        """
        return System.URI['GET_BLUETOOTH_DEVICE_LIST']
    # end-of-method get_bluetooth_device_list
    
    @staticmethod
    def update_bluetooth_device_list():
        """For updating Bluetooth (Sink) device list. This API is available only when "bluetooth_tx_setting"
        is true under /system/getFuncStatus.
        Retrieve update status and list information after finish updating via
        /system/getBluetoothDeviceList.
        """
        return System.URI['UPDATE_BLUETOOTH_DEVICE_LIST']
    # end-of-method update_bluetooth_device_list
    
    @staticmethod
    def connect_bluetooth_device(address):
        """For connecting Bluetooth (Sink) device. This API is available only when "bluetooth_tx_setting" is
        true under /system/getFuncStatus.
        It is possible to take time to return this API response issued after connection status is fixed.
        """
        return System.URI['CONNECT_BLUETOOTH_DEVICE'].format(host='{host}', address=address)
    # end-of-method connect_bluetooth_device
    
    @staticmethod
    def disconnect_bluetooth_device():
        """For disconnecting Bluetooth (Sink) device. This API is available only when "bluetooth_tx_setting"
        is true under /system/getFuncStatus.
        This API response is issued immediately after disconnect request is accepted.
        """
        return System.URI['DISCONNECT_BLUETOOTH_DEVICE']
    # end-of-method disconnect_bluetooth_device
    
    @staticmethod
    def set_speaker_a(enable=True):
        """For setting Speaker A status"""
        return System.URI['SET_SPEAKER_A'].format(host='{host}', enable=_bool_to_str(enable))
    # end-of-method set_speaker_a
    
    @staticmethod
    def set_speaker_b(enable=True):
        """For setting Speaker A status"""
        return System.URI['SET_SPEAKER_B'].format(host='{host}', enable=_bool_to_str(enable))
    # end-of-method set_speaker_b
    
    @staticmethod
    def set_dimmer(value):
        """For setting FL/LED Dimmer.
        
        Arguments:
        value -- Setting Dimmer. Specifies -1 in case of auto setting.
                 Specifies 0 or more than 0 in case of manual setting.
                 Auto setting is available only when -1 is exists in vale range under
                 /system/getFeatures.
                 Value Range: calculated by minimum/maximum/step values gotten
                 via /system/getFeatures
        """
        return System.URI['SET_DIMMER'].format(host='{host}', value=value)
    # end-of-method set_dimmer
    
    @staticmethod
    def set_zone_b_volume_sync(enable):
        """For setting Zone B volume sync."""
        return System.URI['SET_ZONE_B_VOLUME_SYNC'].format(host='{host}', enable=_bool_to_str(enable))
    # end-of-method set_zone_b_volume_sync
    
    @staticmethod
    def set_hdmi_out_1(enable):
        """set_hdmi_out_1."""
        return System.URI['SET_HDMI_OUT_1'].format(host='{host}', enable=_bool_to_str(enable))
    # end-of-method set_hdmi_out_1
    
    @staticmethod
    def set_hdmi_out_2(enable):
        """set_hdmi_out_1."""
        return System.URI['SET_HDMI_OUT_2'].format(host='{host}', enable=_bool_to_str(enable))
    # end-of-method set_hdmi_out_2
    
    @staticmethod
    def get_name_text(id):
        """For retrieving text information of Zone, Input, Sound program. If they can be renamed, can
        retrieve text information renamed.
        
        Arguments:
        id -- Specifies ID. If no ID is specified, retrieve all information of
              Zone, Input, Sound program. Refer to "All ID List" for details (documentation).
        """
        return System.URI['GET_NAME_TEXT'].format(host='{host}', id=id)
    # end-of-method get_name_text
    
    @staticmethod
    def set_name_text(id, text):
        """For setting text information related to each ID of Zone, Input.
        
        Arguments:
        id -- Specifies ID. Input ID can be specified only when
              " rename_enable " is true under /system/getFeatures.
              Sound Program ID can not be specified.
              Note:
              If "main" is specified, Network Name is overwritten with same
              text information to be acceptable both MusicCast CONTROLLER
              (Yamaha) and Spotify App. If Network Name is changed, "main"
              text information is not changed.
        text -- Specifies text information (UTF-8 within 64 bytes).
                If "" (empty text) is specified, specifies default text information.  
        """
        data = {'id': id, 'text': text}
        return System.URI['SET_NAME_TEXT'], data
    # end-of-method set_name_text
        
    pass
# end-of-class System


class Zone():
    """Zone commands."""

    URI = {
        'GET_STATUS': 'http://{host}/YamahaExtendedControl/v1/{zone}/getStatus',
        'GET_SOUND_PROGRAM_LIST': 'http://{host}/YamahaExtendedControl/v1/{zone}/getSoundProgramList',
        'SET_POWER': 'http://{host}/YamahaExtendedControl/v1/{zone}/setPower?power={power}',
        'SET_SLEEP': 'http://{host}/YamahaExtendedControl/v1/{zone}/setSleep?sleep={sleep}',
        'SET_VOLUME': 'http://{host}/YamahaExtendedControl/v1/{zone}/setVolume?volume={volume}&step={step}',
        'SET_MUTE': 'http://{host}/YamahaExtendedControl/v1/{zone}/setMute?enable={enable}',
        'SET_INPUT': 'http://{host}/YamahaExtendedControl/v1/{zone}/setInput?input={input}&mode={mode}',
        'SET_SOUND_PROGRAM': 'http://{host}/YamahaExtendedControl/v1/{zone}/setSoundProgram?program={program}',
        'PREPARE_INPUT_CHANGE': 'http://{host}/YamahaExtendedControl/v1/{zone}/prepareInputChange?input={input}',
        'SET_3D_SURROUND': 'http://{host}/YamahaExtendedControl/v1/{zone}/set3dSurround?enable={enable}',
        'SET_DIRECT': 'http://{host}/YamahaExtendedControl/v1/{zone}/setDirect?enable={enable}',
        'SET_PURE_DIRECT': 'http://{host}/YamahaExtendedControl/v1/{zone}/setPureDirect?enable={enable}',
        'SET_ENHANCER': 'http://{host}/YamahaExtendedControl/v1/{zone}/setEnhancer?enable={enable}',
        'SET_TONE_CONTROL': 'http://{host}/YamahaExtendedControl/v1/{zone}/setToneControl?mode={mode}&bass={bass}&treble={treble}',
        'SET_EQUALIZER': 'http://{host}/YamahaExtendedControl/v1/{zone}/setEqualizer?mode={mode}&low={low}&mid={mid}&high={high}',
        'SET_BALANCE': 'http://{host}/YamahaExtendedControl/v1/{zone}/setBalance?value={value}',
        'SET_DIALOGUE_LEVEL': 'http://{host}/YamahaExtendedControl/v1/{zone}/setDialogueLevel?value={value}',
        'SET_DIALOGUE_LIFT': 'http://{host}/YamahaExtendedControl/v1/{zone}/setDialogueLift?value={value}',
        'SET_CLEAR_VOICE': 'http://{host}/YamahaExtendedControl/v1/{zone}/setClearVoice?enable={enable}',
        'SET_SUBWOOFER_VOLUME': 'http://{host}/YamahaExtendedControl/v1/{zone}/setSubwooferVolume?volume={volume}',
        'SET_BASS_EXTENSION': 'http://{host}/YamahaExtendedControl/v1/{zone}/setBassExtension?enable={enable}',
        'GET_SIGNAL_INFO': 'http://{host}/YamahaExtendedControl/v1/main/getSignalInfo',
        'SET_LINK_CONTROL': 'http://{host}/YamahaExtendedControl/v1/{zone}/setLinkControl?control={control}',
        'SET_LINK_AUDIO_DELAY': 'http://{host}/YamahaExtendedControl/v1/{zone}/setLinkAudioDelay?delay={delay}'
    }
    
    @staticmethod
    def get_status(zone):
        """For retrieving basic information of each Zone like power, volume, input and so on.
        
        Arguments:
            zone -- Specifies target Zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4'
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        return Zone.URI['GET_STATUS'].format(host='{host}', zone=zone)
    # end-of-method get_status
    
    @staticmethod
    def get_sound_program_list(zone):
        """For retrieving a list of Sound Program available in each Zone. It is possible for the list contents to
           be dynamically changed.

        Arguments:
            zone -- Specifies target Zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4'
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        return Zone.URI['GET_SOUND_PROGRAM_LIST'].format(host='{host}', zone=zone)
    # end-of-method get_sound_program_list        
    
    @staticmethod
    def set_power(zone, power):
        """For setting power status of each Zone.
        
        Arguments:
            zone -- Specifies target Zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4'
            power -- Specifies power status.
                     Values: 'on', 'standby', 'toggle'
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        assert power in POWER, 'Invalid POWER value!'
        return Zone.URI['SET_POWER'].format(host='{host}', zone=zone, power=power)
    # end-of-method set_power
    
    @staticmethod
    def set_sleep(zone, sleep):
        """For setting Sleep Timer for each Zone.
        With Zone B enabled Devices, target Zone is described as Master Power, but Main Zone is used to
        set it up via YXC.
           
        Arguments:   
            zone -- Specifies target Zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4'
            sleep -- Specifies Sleep Time (unit in minutes)
                     Values: 0, 30, 60, 90, 120
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        assert sleep in SLEEP, 'Invalid SLEEP value!'
        return Zone.URI['SET_SLEEP'].format(host='{host}', zone=zone, sleep=sleep)
    # end-of-method set_sleep

    @staticmethod
    def set_volume(zone, volume, step):
        """For setting volume in each Zone. Values of specifying range and steps are different. There are
        some Devices that cannot allow this value to be go up to Device's maximum volume.
        
        Arguments:
            zone -- Specifies target Zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4'    
            volume -- Specifies volume value
                      Value Range: calculated by minimum/maximum/step values gotten via /system/getFeatures.
                      (Available on and after API Version 1.17) 'up', 'down'
            step -- Specifies volume step value if the volume is 'up' or 'down'. If
                    nothing specified, minimum step value is used implicitly.
                    (Available on and after API Version 1.17)
                    Values: Value range calculated by minimum/maximum/step values gotten via /system/getFeatures.
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        return Zone.URI['SET_VOLUME'].format(host='{host}', zone=zone, volume=volume, step=step)
    # end-of-method set_volume
    
    @staticmethod
    def set_mute(zone, enable=True):
        """For setting mute status in each Zone.
        
        Arguments:
            zone -- Specifies target Zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4' 
            enable -- Specifying mute status. Default: True.
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        return Zone.URI['SET_MUTE'].format(host='{host}', zone=zone, enable=_bool_to_str(enable))
    # end-of-method set_mute
    
    @staticmethod
    def set_input(zone, input, mode):
        """For selecting each Zone input.
        
        Arguments:
            zone -- Specifies target Zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4'
            input -- Specifies Input ID.
                     Values: Input IDs gotten via /system/getFeatures
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        return Zone.URI['SET_INPUT'].format(host='{host}', zone=zone, input=input, mode=mode)
    # end-of-method set_input
    
    @staticmethod
    def set_sound_program(zone, program):
        """For selecting Sound Programs.
        
        Arguments:
            zone -- Specifies target Zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4'      
            program -- Specifies Sound Program ID.
                       Values: Sound Program IDs gotten via /system/getFeatures
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        return Zone.URI['SET_SOUND_PROGRAM'].format(host='{host}', zone=zone, program=program)
    # end-of-method set_sound_program
    
    @staticmethod
    def prepare_input_change(zone, input):
        """Let a Device do necessary process before changing input in a specific zone. This is valid only
        when 'prepare_input_change' exists in 'func_list' found in /system/getFuncStatus.
        MusicCast CONTROLLER executes this API when an input icon is selected in a Room, right
        before sending various APIs (of retrieving list information etc.) regarding selecting input.
        
        Arguments:
            zone -- Specifies target Zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4'  
            input -- Specifies Input ID.
                     Values: Input IDs gotten via /system/getFeatures
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        return Zone.URI['PREPARE_INPUT_CHANGE'].format(host='{host}', zone=zone, input=input)
    # end-of-method prepare_input_change
    
    @staticmethod
    def set_3d_surround(zone, enable):
        """For setting 3D Surround status.
        
        Arguments:
            zone -- Specifies target Zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4'  
            enable -- Specifies 3D Surround status.
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        return Zone.URI['SET_3D_SURROUND'].format(host='{host}', zone=zone, enable=_bool_to_str(enable))
    # end-of-method set_3d_surround
    
    @staticmethod
    def set_direct(zone, enable):
        """For setting Direct status.
        
        Arguments:
            zone -- Specifies target Zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4'  
            enable -- Specifies Direct status.
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        return Zone.URI['SET_DIRECT'].format(host='{host}', zone=zone, enable=_bool_to_str(enable))
    # end-of-method set_direct
    
    @staticmethod
    def set_pure_direct(zone, enable):
        """For setting Pure Direct status.
        
        Arguments:
            zone -- Specifies target Zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4'  
            enable -- Specifies Pure Direct status.
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        return Zone.URI['SET_PURE_DIRECT'].format(host='{host}', zone=zone, enable=_bool_to_str(enable))
    # end-of-method set_pure_direct
    
    @staticmethod
    def set_enhancer(zone, enable):
        """For setting Enhancer status.
        
        Arguments:
            zone -- Specifies target Zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4'  
            enable -- Specifies Enhancer status.
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        return Zone.URI['SET_ENHANCER'].format(host='{host}', zone=zone, enable=_bool_to_str(enable))
    # end-of-method set_enhancer
    
    @staticmethod
    def set_tone_control(zone, mode, bass, treble):
        """For setting Tone Control in each Zone. Values of specifying range and steps are different.
        
        Arguments:
            zone -- Specifies target Zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4'
            mode -- Specifies Mode setting. If no parameter is specified, current Mode
                    setting is not changed.
                    Regardless of the Mode setting, bass/treble setting can be changed,
                    but valid only when Mode setting is "manual".
            bass -- Specifies Bass value
                    Values: Value range calculated by minimum/maximum/step values
                    gotten via /system/getFeatures
            treble -- Specifies Treble value
                      Values: Value range calculated by minimum/maximum/step values
                      gotten via /system/getFeatures
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        return Zone.URI['SET_TONE_CONTROL'].format(host='{host}', zone=zone, mode=mode, bass=bass, treble=treble)
    # end-of-method set_tone_control
    
    @staticmethod
    def set_equalizer(zone, mode, low, mid, high):
        """For setting Equalizer in each Zone. Values of specifying range and steps are different.
        
        Arguments:
            zone -- Specifies target Zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4'
            mode -- Specifies Mode setting. If no parameter is specified, current Mode
                    setting is not changed.
                    Regardless of the Mode setting, low/mid/high setting can be
                    changed, but valid only when Mode setting is "manual".
                    Values: Values gotten via /system/getFeatures
            low -- Specifies Low value
                   Values: Value range calculated by minimum/maximum/step values
                   gotten via /system/getFeatures
            mid -- Specifies Mid value
                   Values: Value range calculated by minimum/maximum/step values
                   gotten via /system/getFeatures
            high -- Specifies High value
                    Values: Value range calculated by minimum/maximum/step values
                    gotten via /system/getFeatures
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        return Zone.URI['SET_EQUALIZER'].format(host='{host}', zone=zone, mode=mode, low=low, mid=mid, high=high)
    # end-of-method set_equalizer
    
    @staticmethod
    def set_balance(zone, value):
        """For setting L/R Balance in each Zone's speaker. Values of specifying range and steps are different.
        
        Arguments:
            zone -- Specifies target Zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4'
            value -- Specifies L/R Balance value. Negative values are for left side,
                     positive values are for right side balance.
                     Values: Value range calculated by minimum/maximum/step values
                     gotten via /system/getFeatures
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        return Zone.URI['SET_BALANCE'].format(host='{host}', zone=zone, value=value)
    # end-of-method set_balance
    
    @staticmethod
    def set_dialogue_level(zone, value):
        """For setting Dialogue Level in each Zone. Values of specifying range and steps are different.
        
        Arguments:
            zone -- Specifies target Zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4'
            value -- Specifies Dialogue Level value
                     Values: Value range calculated by minimum/maximum/step values
                     gotten via /system/getFeatures
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        return Zone.URI['SET_DIALOGUE_LEVEL'].format(host='{host}', zone=zone, value=value)        
    # end-of-method set_dialogue_level
    
    @staticmethod
    def set_dialogue_lift(zone, value):
        """For setting Dialogue Lift in each Zone. Values of specifying range and steps are different.
        
        Arguments:
            zone -- Specifies target Zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4'
            value -- Specifies Dialogue Lift value
                     Values: Value range calculated by minimum/maximum/step values
                     gotten via /system/getFeatures
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        return Zone.URI['SET_DIALOGUE_LIFT'].format(host='{host}', zone=zone, value=value)
    # end-of-method set_dialogue_lift
    
    @staticmethod
    def set_clear_voice(zone, value):
        """For setting Clear Voice in each Zone.
        
        Arguments:
            zone -- Specifies target Zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4'
            value -- Specifies Clear Voice setting
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        return Zone.URI['SET_CLEAR_VOICE'].format(host='{host}', zone=zone, value=value)
    # end-of-method set_clear_voice
        
    @staticmethod
    def set_subwoofer_volume(zone, volume):
        """For setting Subwoofer Volume in each Zone.
        
        Arguments:
            zone -- Specifies target Zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4'
            volume -- Specifies volume value
                      Values: Value range calculated by minimum/maximum/step values
                      gotten via /system/getFeatures
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        return Zone.URI['SET_SUBWOOFER_VOLUME'].format(host='{host}', zone=zone, volume=volume)
    # end-of-method set_clear_voice        
    
    @staticmethod
    def set_bass_extension(zone, enable):
        """For setting Bass Extension in each Zone.
        
        Arguments:
            zone -- Specifies target Zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4'
            enable -- Specifies Bass Extension setting
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        return Zone.URI['SET_BASS_EXTENSION'].format(host='{host}', zone=zone, enable=_bool_to_str(enable))
    # end-of-method set_bass_extension
    
    @staticmethod
    def get_signal_info(zone):
        """For retrieving current playback signal information in each Zone.
        
        Arguments:
            zone -- Specifies target Zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4'
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        return Zone.URI['SET_BASS_EXTENSION'].format(host='{host}', zone=zone)  
    # end-of-method get_signal_info
    
    @staticmethod
    def set_link_control(zone, control):
        """For setting Link Control in each Zone.
        
        Arguments:
            zone -- Specifies target Zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4'
            control -- Specifies Link Control setting
                       Values: Values gotten via /system/getFeatures
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        return Zone.URI['SET_LINK_CONTROL'].format(host='{host}', zone=zone, control=control)
    # end-of-method set_link_control
    
    @staticmethod
    def set_link_audio_delay(zone, delay):
        """For setting Link Audio Delay in each Zone. This setting is invalid when Link Control setting is
           "Stability Boost".
           
        Arguments:
            zone -- Specifies target Zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4'
            delay -- Specifies Link Audio Delay setting
                     Values: Values gotten via /system/getFeatures
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        return Zone.URI['SET_LINK_AUDIO_DELAY'].format(host='{host}', zone=zone, delay=delay)
    # end-of-method set_link_audio_delay
    
    pass
# end-of-class Zone    
    

class Tuner():
    """APIs in regard to Tuner setting and getting information.
    Target inputs: AM / FM / DAB"""
    
    URI = {
        'GET_PRESET_INFO': 'http://{host}/YamahaExtendedControl/v1/tuner/getPresetInfo?band={band}',
        'GET_PLAY_INFO': 'http://{host}/YamahaExtendedControl/v1/tuner/getPlayInfo',
        'SET_FREQ': 'http://{host}/YamahaExtendedControl/v1/tuner/setFreq?band={band}&tuning={tuning}&num={num}',
        'RECALL_PRESET': 'http://{host}/YamahaExtendedControl/v1/tuner/recallPreset?zone={zone}&band={band}&num={num}',
        'SWITCH_PRESET': 'http://{host}/YamahaExtendedControl/v1/tuner/switchPreset?dir={dir}',
        'STORE_PRESET': 'http://{host}/YamahaExtendedControl/v1/tuner/storePreset?num={num}',
        'SET_DAB_SERVICE': 'http://{host}/YamahaExtendedControl/v1/tuner/setDabService?dir={dir}',
    }
    
    @staticmethod
    def get_preset_info(band):
        """For retrieving Tuner preset information.
        
        Arguments:
            band -- Specifying a band. Values depend on Preset Type gotten via /system/getFeatures.
                    Values: 'common' (common), 'am', 'fm', 'dab' (separate)
        """
        assert band in BAND, 'Invalid BAND value!'
        return Tuner.URI['GET_PRESET_INFO'].format(host='{host}', band=band)
    # end-of-method get_preset_info
    
    @staticmethod
    def get_play_info():
        """For retrieving playback information of Tuner."""
        return Tuner.URI['GET_PLAY_INFO']
    # end-of-method get_play_info
    
    @staticmethod
    def set_freq(band, tuning, num):
        """For setting Tuner frequency.
        
        Arguments:
            band -- Specifies Band. Values : 'am', 'fm'
            tunning -- Specifies a tuning method. Use 'tp_up' and 'tp_down' only when Band is RDS.
                       Values: 'up', 'down', 'cancel', 'auto_up', 'auto_down',
                       'tp_up', 'tp_down', 'direct'
            num -- Specifies frequency (unit in kHz). Valid only when tuning is 'direct'
        """
        assert band in BAND, 'Invalid BAND value!'
        assert tuning in TUNING, 'Invalid TUNING value!'
        return Tuner.URI['SET_FREQ'].format(host='{host}', band=band, tuning=tuning, num=num)
    # end-of-method set_freq
    
    @staticmethod
    def recall_preset(zone, band, num):
        """For recalling a Tuner preset.
        
        Arguments:
            zone -- Specifies station recalling zone. This causes input change in specified zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4'
            band -- Specifies Band type. Depending on Preset Type gotten via
                    /system/getFeatures, specifying value is different
                    Values: 'common' (band common), 'separate' (each band preset)
            num -- Specifies Preset number.
                   Value: one in the range gotten via /system/getFeatures
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        assert band in PRESET_BAND, 'Invalid BAND value!'
        return Tuner.URI['RECALL_PRESET'].format(host='{host}', zone=zone, band=band, num=num)
    # end-of-method recall_preset
    
    @staticmethod
    def switch_preset(dir):
        """For selecting Tuner preset.
        Call this API after change the target zone's input to Tuner. It is possible to change Band in case of
        preset type is 'common'. In case of preset type is 'separate', need to change the target Band
        before calling this API.
        This API is available on and after API Version 1.17.
        
        Arguments:
            dir -- Specifies change direction of preset.
                   Values: 'next', 'previous'
        """
        assert dir in DIR, 'Invalid DIR value!'
        return Tuner.URI['SWITCH_PRESET'].format(host='{host}', dir=dir)
    # end-of-method switch_preset
    
    @staticmethod
    def store_preset(num):
        """For registering current station to a preset.
        
        Arguments:
            num -- Specifying a preset number.
                   Value: one in the range gotten via /system/getFeatures  
        """
        return Tuner.URI['STORE_PRESET'].format(host='{host}', num=num)
    # end-of-method store_preset
    
    @staticmethod
    def set_dab_service(dir):
        """For selecting DAB Service. Available only when DAB is valid to use.
        
        Arguments:
            dir -- Specifies change direction of services.
                   Values: 'next', 'previous'
        """
        assert dir in DIR, 'Invalid DIR value!'
        return Tuner.URI['SET_DAB_SERVICE'].format(host='{host}', dir=dir)
    # end-of-method set_dab_service
    
    pass
# end-of-class Tuner    


class  NetUSB():
    """APIs in regard to Network/USB related setting and getting information
    Target Inputs: USB / Network related ones (Server / Net Radio / Pandora / Spotify / AirPlay etc.)"""
    
    URI = {
        'GET_PRESET_INFO': 'http://{host}/YamahaExtendedControl/v1/netusb/getPresetInfo',
        'GET_PLAY_INFO': 'http://{host}/YamahaExtendedControl/v1/netusb/getPlayInfo',
        'SET_PLAYBACK': 'http://{host}/YamahaExtendedControl/v1/netusb/setPlayback?playback={playback}',
        'TOGGLE_REPEAT': 'http://{host}/YamahaExtendedControl/v1/netusb/toggleRepeat',
        'TOGGLE_SHUFFLE': 'http://{host}/YamahaExtendedControl/v1/netusb/toggleShuffle',
        'GET_LIST_INFO': 'http://{host}/YamahaExtendedControl/v1/netusb/getListInfo?input={input}&index={index}&size={size}&lang={lang}&list_id={list_id}',
        'SET_LIST_CONTROL': 'http://{host}/YamahaExtendedControl/v1/netusb/setListControl?list_id={list_id}&type={type}&index={index}&zone={zone}',
        'SET_SEARCH_STRING': 'http://{host}/YamahaExtendedControl/v1/netusb/setSearchString',
        'RECALL_PRESET': 'http://{host}/YamahaExtendedControl/v1/netusb/recallPreset?zone={zone}&num={num}',
        'STORE_PRESET': 'http://{host}/YamahaExtendedControl/v1/netusb/storePreset?num={num}',
        'GET_ACCOUNT_STATUS': 'http://{host}/YamahaExtendedControl/v1/netusb/getAccountStatus',
        'SWITCH_ACCOUNT': 'http://{host}/YamahaExtendedControl/v1/netusb/switchAccount?input={input}&index={index}&timeout={timeout}',
        'GET_SERVICE_INFO': 'http://{host}/YamahaExtendedControl/v1/netusb/getServiceInfo?input={input}&type={type}&timeout={timeout}',
    }
    
    @staticmethod
    def get_preset_info():
        """For retrieving preset information. Presets are common use among Net/USB related input sources.
        """
        return NetUSB.URI['GET_PRESET_INFO']
    # end-of-method get_preset_info
    
    @staticmethod
    def get_play_info():
        """For retrieving playback information."""
        return NetUSB.URI['GET_PLAY_INFO']
    # end-of-method get_play_info
    
    @staticmethod
    def set_playback(playback):
        """For controlling playback status.
        
        Arguments:
            playback -- Specifies playback status.
                        Values: 'play', 'stop', 'pause', 'play_pause', 'previous', 'next',
                        'fast_reverse_start', 'fast_reverse_end', 'fast_forward_start',
                        'fast_forward_end'
        """
        assert playback in PLAYBACK, 'Invalid PLAYBACK value!'
        return NetUSB.URI['SET_PLAYBACK'].format(host='{host}', playback=playback)
    # end-of-method set_playback    
    
    @staticmethod
    def toggle_repeat():
        """For toggling repeat setting. No direct / discrete setting commands available."""
        return NetUSB.URI['TOGGLE_REPEAT']
    # end-of-method toggle_repeat    
    
    @staticmethod
    def toggle_shuffle():
        """For toggling shuffle setting. No direct / discrete setting commands available."""
        return NetUSB.URI['TOGGLE_SHUFFLE']
    # end-of-method toggle_shuffle    
    
    @staticmethod
    def get_list_info(input, index, size, lang, list_id):
        """For retrieving list information. Basically this info is available to all relevant inputs, not limited to
        or independent from current input.

        Arguments:
                input -- Specifies target Input ID. Controls for setListControl are to work
                         with the input specified here.
                         Values: Input IDs for Net/USB related sources
                index -- Specifies the reference index (offset from the beginning of the list).
                         Note that this index must be in multiple of 8. If nothing was
                         specified, the reference index previously specified would be used.
                         Values: 0, 8, 16, 24, ..., 64984, 64992
                size -- Specifies max list size retrieved at a time.
                        Value Range: 1 - 8
                lang -- Specifies list language. But menu names or text info are not
                        always necessarily pulled in a language specified here. If nothing
                        specified, English ("en") is used implicitly
                        Values: 'en' (English), 'ja' (Japanese), 'fr' (French), 'de'
                        (German), 'es' (Spanish), 'ru' (Russian), 'it' (Italy), 'zh' (Chinese)
                list_id -- Specifies list ID. If nothing specified, 'main' is chosen implicitly
                           Values: 'main' (common for all Net/USB sources)
                                   'auto_complete' (Pandora)
                                   'search_artist' (Pandora)
                                   'search_track' (Pandora)
        """
        assert lang in LANG, 'Invalid LANG value!'
        return NetUSB.URI['GET_LIST_INFO'].format(host='{host}', input=input, index=index, size=size, lang=lang, list_id=list_id)
    # end-of-method get_list_info    
    
    @staticmethod
    def set_list_control(list_id, type, index, zone):
        """For control a list. Controllable list info is not limited to or independent from current input.
        
        Arguments:
            list_id -- Specifies list ID. If nothing specified, 'main' is chosen implicitly
                       Values: 'main' (common for all Net/USB sources)
                               'auto_complete' (Pandora)
                               'search_artist' (Pandora)
                               'search_track' (Pandora)
            type -- Specifies list transition type. 'select' is to enter and get into one deeper layer than the current 
                    layer where the element specified by the index belongs to. 'play' is to start playback current index
                    element, 'return' is to go back one upper layer than current. 'select' and 'play' needs to specify 
                    an index at the same time. In case to 'select' an element with its attribute being 'Capable of Search', 
                    specify search text using setSearchString in advance. (Or it is possible to specify search text and 
                    move layers at the same time by specifying an index in setSearchString).
                    Values: 'select', 'play', 'return'
        """
        assert type in TYPE, 'Invalid TYPE value!'
        assert zone in ZONES, 'Invalid ZONE value!'
        return NetUSB.URI['SET_LIST_CONTROL'].format(host='{host}', list_id=list_id, type=type, index=index, zone=zone)
    # end-of-method set_list_control        
    
    @staticmethod
    def set_search_string():
        raise NotImplementedError()
    # end-of-method set_search_string

    @staticmethod
    def recall_preset(zone, num):
        """For recalling a content preset.
        
        Arguments:
            zone -- Specifies station recalling zone. This causes input change in specified zone.
                    Values: 'main', 'zone2', 'zone3', 'zone4'
            num -- Specifies Preset number.
                   Value: one in the range gotten via /system/getFeatures
        """
        assert zone in ZONES, 'Invalid ZONE value!'
        return NetUSB.URI['RECALL_PRESET'].format(host='{host}', zone=zone, num=num)
    # end-of-method recall_preset
    
    @staticmethod
    def store_preset(num):
        """For registering current content to a preset. Presets are common use among Net/USB related
        input sources.
        
        Arguments:
            num -- Specifying a preset number.
                   Value: one in the range gotten via /system/getFeatures
        """
        return NetUSB.URI['STORE_PRESET'].format(host='{host}', num=num)
    # end-of-method store_preset
    
    @staticmethod
    def get_account_status():
        """For retrieving account information registered on Device."""
        return NetUSB.URI['GET_ACCOUNT_STATUS']
    # end-of-method get_account_status
    
    @staticmethod
    def switch_account(input, index, timeout):
        """For switching account for service corresponding multi account.
        
        Arguments:
            input -- Specifies target Input ID.
                     Value: 'pandora'
            index -- Specifies switch account index.
                     Value : 0 - 7 (Pandora)
            timeout -- Specifies timeout duration(ms) for this API process. If specifies 0,
                       treat as maximum value.
                       Value: 0 - 60000
        """
        return NetUSB.URI['SWITCH_ACCOUNT'].format(host='{host}', input=input, index=index, timeout=timeout)
    # end-of-method switch_account
    
    @staticmethod
    def get_service_info(input, type, timeout):
        """For retrieving information of various Streaming Service. The combination of Input/Type is available
        as follows;
        
        Account List (account_list) : retrieving list of account registed on Device
        Licensing (licensing) : checking license
        Activation Code (activation_code) : retrieving Activation Code
        * Disable to check Rhapsody license by refering the value of this APIs response_code. a
          Device issues events of netusb - account_updated by condition, retrieve the info excute
          /netusb/getAccountStatus. (Sometimes Deivice not issue events)
        * Before retrieve Activation Code, retrieve Account List and check not to reach Max about
          the num of registration.
        Note: Rhapsody service name will be changed to Napster.

        Arguments:
            input -- Specifies target Input ID.
                     Value: 'pandora', 'rhapsody', 'napster'
        """
        return NetUSB.URI['GET_SERVICE_INFO'].format(host='{host}', input=input, type=type, timeout=timeout)
    # end-of-method switch_account
    
    pass
# end-of-class Network_USB
    

class CD():
    """APIs in regard to CD setting and getting information."""

    URI = {
        'GET_PLAY_INFO': 'http://{host}/YamahaExtendedControl/v1/cd/getPlayInfo',
        'SET_PLAYBACK': 'http://{host}/YamahaExtendedControl/v1/cd/setPlayback?playback={playback}&num={num}',
        'TOGGLE_TRAY': 'http://{host}/YamahaExtendedControl/v1/cd/toggleTray',
        'TOGGLE_REPEAT': 'http://{host}/YamahaExtendedControl/v1/cd/toggleRepeat',
        'TOGGLE_SHUFFLE': 'http://{host}/YamahaExtendedControl/v1/cd/toggleShuffle',
    }

    def get_play_info():
        """For retrieving playback information of CD."""
        return CD.URI['GET_PLAY_INFO']
    # end-of-method get_play_info

    def set_playback(playback):
        """For controlling playback status.
        
        Arguments:
        playback -- Specifies playback status
                    Values: 'play', 'stop', 'pause', 'previous', 'next',
                            'fast_reverse_start', 'fast_reverse_end', 'fast_forward_start',
                            'fast_forward_end', 'track_select'
                            
        num -- Specifies target track number to playback. 
               This parameter is valid only when playback "track_select" is specified.
               Values: 1-512
        """
        assert playback in PLAYBACK, 'Invalid PLAYBACK value!'
        return CD.URI['SET_PLAYBACK'].format(host='{host}', playback=playback)
    # end-of-method set_playback
    
    def toggle_tray():
        """For toggling CD tray Open/Close setting."""
        return CD.URI['TOGGLE_TRAY']
    # end-of-method toggle_tray
        
    def toggle_repeat():
        """For toggling repeat setting. No direct / discrete setting commands available."""
        return CD.URI['TOGGLE_REPEAT']
    # end-of-method toggle_repeat
    
    def toggle_shuffle():
        """For toggling shuffle setting. No direct / discrete setting commands available."""
        return CD.URI['TOGGLE_SHUFFLE']
    # end-of-method toggle_shuffle
    
    pass
# end-of-class CD


class Debug():
    """Undocumented Debug commands.
    """

    URI = {
        'GET_DIAG_INFO': 'http://{host}/YamahaExtendedControl/v1/debug/getDiagInfo',
        'GET_STATUS': 'http://{host}/YamahaExtendedControl/v1/debug/getStatus'
    }
    
    @staticmethod
    def get_diag_info():
        """None.
        """
        return Debug.URI['GET_DIAG_INFO']
    # end-of-method get_diag_info
    
    @staticmethod
    def get_status():
        """None.
        """
        return Debug.URI['GET_STATUS']
    # end-of-method get_status
    
    pass
# end-of-class Debug

def _bool_to_str(value):
    return str(value).lower()

if __name__ == '__main__':
    pass
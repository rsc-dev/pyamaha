# PYAMAHA

## About
Pyamaha is Python implementation of [Yamaha Extended Control API Specification](https://github.com/rsc-dev/pyamaha/blob/master/doc/YXC_API_Spec_Basic.pdf).
Please see Status for list of implemented functions.
Undocumented functions will be added in future.

## Instalation
```sh
pip install pyamaha
```
or
```sh
python setup.py install
```

## Usage
### API
```python
from pyamaha import Device, System

dev = Device('192.168.1.1')
res = dev.request(System.get_device_info())

print res.json() # JSON response
```

### CLI
```sh
> python -m pyamaha
yxc>device 192.168.1.106
yxc>system
yxc\system>getDeviceInfo
{u'api_version': 1.17,
 u'destination': u'BG',
 u'device_id': u'XXX',
 u'model_name': u'CD-NT670D',
 u'netmodule_checksum': u'XXX',
 u'netmodule_version': u'1130    ',
 u'operation_mode': u'normal',
 u'response_code': 0,
 u'system_id': u'XXX',
 u'system_version': 1.7,
 u'update_error_code': u'FFFFFFFF'}
yxc\system>
```

## Status
<table>
<th>Function</th>
<th>API</th>
<th>CLI</th>
<th>Info</th>
<tr><td colspan="4">SYSTEM</td></tr>
<tr>
<td>/YamahaExtendedControl/v1/system/getDeviceInfo</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/system/getFeatures</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/system/getNetworkStatus</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/system/getNetworkStatus</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/system/setAutoPowerStandby</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/system/getLocationInfo</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/system/sendIrCode
</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr><td colspan="4">ZONE</td></tr>
<tr>
<td>/YamahaExtendedControl/v1/{zone}/getStatus</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/{zone}/getSoundProgramList</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/{zone}/setPower</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/{zone}/setSleep</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/{zone}/setVolume</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/{zone}/setMute</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/{zone}/setInput</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/{zone}/setSoundProgram</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>http://{host}/YamahaExtendedControl/v1/{zone}/prepareInputChange</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr><td colspan="4">TUNER</td></tr>
<tr>
<td>/YamahaExtendedControl/v1/tuner/getPresetInfo</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/tuner/getPlayInfo</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/tuner/setFreq</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/tuner/recallPreset</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/tuner/switchPreset</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/tuner/storePreset</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/tuner/setDabService</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr><td colspan="4">NETWORK/USB</td></tr>
<tr>
<td>/YamahaExtendedControl/v1/netusb/getPresetInfo</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/netusb/getPlayInfo</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/netusb/setPlayback</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/netusb/toggleRepeat</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/netusb/toggleShuffle</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/netusb/getListInfo</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/netusb/setListControl</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/netusb/setSearchString</td>
<td>-</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/netusb/recallPreset</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/netusb/storePreset</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/netusb/getAccountStatus</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/netusb/switchAccount</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/netusb/getServiceInfo</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr><td colspan="4">CD</td></tr>
<tr>
<td>/YamahaExtendedControl/v1/cd/getPlayInfo</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/cd/setPlayback</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/cd/toggleTray</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/cd/toggleRepeat</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
<tr>
<td>/YamahaExtendedControl/v1/cd/toggleShuffle</td>
<td>x</td>
<td>-</td>
<td>Documented</td>
</tr>
</table>

## License
Code is released under [MIT license](https://github.com/rsc-dev/pyamaha/blob/master/LICENSE) © [Radoslaw '[rsc]' Matusiak](https://rm2084.blogspot.com/).
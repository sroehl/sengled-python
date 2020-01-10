import requests
from SengledElement import sengled_base_url, zigbee_url, device_url


class devices:
    devices = None
    client = None

    def add_device(self, device, room_id):
        if self.get_device(device['deviceUuid']) == None:
            device['roomId'] = room_id
            self.devices.append(device)
            return True
        return False

    def clear_device_list(self):
        self.devices = []

    def get_names(self):
        device_names = []
        for device in self.devices:
            device_names.append(device['deviceName'])
        return device_names

    def get_device_id(self, device_name):
        for device in self.devices:
            if 'deviceName' in device and device['deviceName'] == device_name and 'deviceUuid' in device:
                return device['deviceUuid']
        return None

    def get_device(self, device_id):
        for device in self.devices:
            if device['deviceUuid'] == device_id:
                return device

    def update_value(self, device_id, name, value):
        for device in self.devices:
            if device['deviceUuid'] == device_id:
                device[name] = value


    def toggle_device(self, device_id=None, device_name=None):
        if device_id is None:
            device_id = self.get_device_id(device_name)
        device = self.get_device(device_id)
        toggle_value = 0
        if device['onoff'] == 0:
            toggle_value = 1
        self.set_device_state(toggle_value, device_id=device_id)

    def set_device_state(self, state, device_id=None, device_name=None):
        if device_id is None:
            device_id = self.get_device_id(device_name)

        self.client.login()
        toggle_json = {'deviceUuid': device_id,
                       'onoff': state}
        resp = requests.post(sengled_base_url + zigbee_url + device_url + '/deviceSetOnOff.json',
                             headers=self.client.headers, json=toggle_json, verify=False)
        if resp.status_code == 200:
            self.update_value(device_id, 'onoff', state)
            return True
        else:
            print('Could not toggle device')
            return False

    def __init__(self, client):
        self.devices = []
        self.client = client

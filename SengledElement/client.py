import requests
from SengledElement.devices import devices
from SengledElement.rooms import rooms
from SengledElement import sengled_base_url, zigbee_url, customer_url, room_url


class client:

    headers = {'Content-type': 'application/json'}

    username = None
    password = None
    jsessionid = None
    logged_in = False

    rooms = None
    devices = None

    def login(self):
        if self.logged_in:
            return
        login_data = {'os_type': 'android', 'pwd': self.password, 'user': self.username, 'uuid': 'xxxxxx'}
        resp = requests.post(sengled_base_url + zigbee_url + customer_url + 'login.json',
                             headers=self.headers, verify=False, json=login_data)
        if resp.status_code == 200:
            resp_json = resp.json()
            if 'msg' in resp_json and resp_json['msg'] == 'success':
                self.headers['Cookie'] = 'JSESSIONID={}'.format(resp_json['jsessionid'])
                self.jsessionid = resp_json['jsessionid']
                self.logged_in = True
            else:
                key = None
                if 'msg' in resp_json:
                    key = 'msg'
                elif 'info' in resp_json:
                    key = 'info'
                if key is not None:
                    print('Login unsuccessful: {}'.format(resp_json[key]))
                else:
                    print('Could not login successfully')
        else:
            print('Could not login successfully')

    def update(self):
        self.login()
        resp = requests.post(sengled_base_url + zigbee_url + room_url + 'getUserRoomsDetail.json',
                             headers=self.headers, verify=False, json={})
        if resp.status_code == 200:
            resp_json = resp.json()
            if 'roomList' in resp_json:
                self.parse_room_list(resp_json['roomList'])
        else:
            print('Could not get rooms: {}'.format(resp.status_code))

    def parse_room_list(self, room_list):
        self.rooms.clear_rooms()
        for room in room_list:
            if 'deviceList' in room:
                for device in room['deviceList']:
                    self.devices.add_device(device, room['roomId'])
            del room['deviceList']
            self.rooms.add_room(room)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.devices = devices(self)
        self.rooms = rooms()
        self.update()

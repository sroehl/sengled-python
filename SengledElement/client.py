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
                msg_text = resp_json[key]
                if msg_text == '用户名不存在':
                    msg_text = 'Username does not exist'
                elif msg_text == '用户名或密码错误':
                    msg_text = 'Incorrect password'

                if key is not None:
                    print('Login unsuccessful: {}'.format(msg_text))
                else:
                    print('Could not login successfully')
        else:
            print('Could not login successfully')

    def update(self):
        self.login()
        if not self.logged_in:
            raise RuntimeError('Cannot update because user is not logged in')
        resp = requests.post(sengled_base_url + zigbee_url + room_url + 'getUserRoomsDetail.json',
                             headers=self.headers, verify=False, json={})
        if resp.status_code == 200:
            resp_json = resp.json()
            self.rooms.clear_rooms()
            if 'roomList' in resp_json:
                self.parse_room_list(resp_json['roomList'])
            if 'deviceNoRoomList' in resp_json:
                self.parse_no_room_list(resp_json['deviceNoRoomList'])
        else:
            print('Could not get rooms: {}'.format(resp.status_code))

    def parse_no_room_list(self, list):
        device_added = False
        for device in list:
            if self.devices.add_device(device, 'noRoom'):
                device_added = True
        if device_added:
            self.rooms.add_room('noRoom')

    def parse_room_list(self, room_list):
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

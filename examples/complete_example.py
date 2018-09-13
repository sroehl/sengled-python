from SengledElement import client
import sys

home = None


def list_devices():
    for name in home.devices.get_names():
        print(name)


def set_state(name=None, state=None):
    if name is None:
        name = input("Which bulb?")
    if state is None:
        state = input("What state?")
    home.devices.set_device_state(state, device_name=name)


def main_input():
    max_option = 3
    while True:
        print("1)\tList Bublbs")
        print("2)\tSet State")
        print("3)\tExit)")
        select = input("Select option: ")
        select = int(select)
        if 0 < select <= max_option:
            if select == 1:
                list_devices()
            elif select == 2:
                set_state()
            elif select == 3:
                return


if __name__ == '__main__':
    home = client.client(sys.argv[1], sys.argv[2])

    main_input()


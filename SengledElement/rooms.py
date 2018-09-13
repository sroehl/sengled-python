

class rooms:
    rooms = None

    def clear_rooms(self):
        self.rooms = []

    def add_room(self, room):
        self.rooms.append(room)

    def __init__(self):
        self.rooms = []

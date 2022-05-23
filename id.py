import uuid

class Id:
    def __init__(self):
        self.public_uuid = uuid.uuid4()
        self.private_uuid = uuid.uuid4()
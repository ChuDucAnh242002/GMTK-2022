import engine.database as db

class effect():
    def __init__(self):
        self.COLLIDE_TABLE = [
            ['pass', 'none', '3', 'none'],
            ['none', 'pass', 'none', 'none'],
            ['float', 'none', 'blow', 'pass'],
            ['sink', '7', 'heavy', 'none']
        ]
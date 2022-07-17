import engine.database as db

class effect():
    def __init__(self):
        self.COLLIDE_TABLE = [
            ['sink', 'die', 'blow', 'none']
            ['pass', 'none', '3', 'none'],
            ['none', 'pass', 'none', 'none'],
            ['float', 'none', 'die', 'pass'],
            ['sink', '7', 'slow', 'none']
        ]
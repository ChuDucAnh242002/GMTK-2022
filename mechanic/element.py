from engine.object import object


class element(object):
    def __init__(self, ID, pos, status = "idle", tag = ['object']): 
        super().__init__(self, ID, pos, status, tag)

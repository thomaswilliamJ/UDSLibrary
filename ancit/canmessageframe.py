
class messageframe(object):
    idr = 0
    isext = False
    data = []
    len = 0
    def __init__(self,ids,isext = False,data = [],length = 8):
        
        messageframe.idr = ids
        messageframe.isext = isext
        messageframe.data = data
        messageframe.len = length

class Score:

    def __init__(self, val, dir):
        self.value = val
        self.dir = dir

class LocalAlignment:

    def __init__(self, string, iStart, iEnd):
        self.string = string
        self.iStart = iStart
        self.iEnd = iEnd

class AlignmentData:

    def __init__(self, localAlignment, score):
        self.localAlignment = localAlignment
        self.score = score

    def string(self,i):
        return self.localAlignment[i].string

    def size(self):
        return len(self.string(0))
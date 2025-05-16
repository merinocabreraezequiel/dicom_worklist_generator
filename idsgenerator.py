import random
import string

class idsgenerator: #PATIENT ID CLASS

    def __init__(self):
        pass
    def gen_id(self, _len=8):
        chrs = string.ascii_uppercase + string.digits
        return ''.join(random.choices(chrs, k=_len))

    def multiple_gen_id(self, _total, _len=8):
        ids = set()
        while len(ids) < _total:
            ids.add(self.gen_id(_len))
        return list(ids)
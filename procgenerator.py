import random

class procgenerator: #PROCEDURE GENERATOR CLASS
    procedure_len = 8 #LENGTH OF PROCEDURE

    def __init__(self):
        pass

    def set_procedure_len(self, _procedure_len):
        if _procedure_len < 0:
            raise ValueError("Procedure length cannot be negative")
        else:
            self.procedure_len = _procedure_len
    
    def gen_procedure(self):
        min = 10**(self.procedure_len - 1)
        max = (10**self.procedure_len) - 1
        return random.randint(min, max)
    
    def multiple_gen_procedure(self, _total, _len=8):
        if _len != self.procedure_len and _len > 0: self.procedure_len = _len
        procs = set()
        while len(procs) < _total:
            procs.add(self.gen_procedure())
        return list(procs)
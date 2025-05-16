from datetime import datetime, timedelta
import random

class scheduling:
    sch_time = ''
    sch_date = ''
    procedure = ''
    aetitle = 'ORTHANC'

    margin_days = 30
    min_duration = 30 
    max_duration = 240
    procedure_len = 8

    def __init__(self):
        pass

    #GENERATORS
    def gen_sch_date(self):
        gen_date = datetime.today() + timedelta(days=random.randint((-1*self.margin_days), self.margin_days))
        return gen_date.strftime("%Y%m%d")
    
    def gen_sch_time(self):
        gen_time = datetime.today() + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
        return gen_time.strftime("%H%M%S")
    
    def gen_procedure(self):
        min = 10**(self.procedure_len - 1)
        max = (10**self.procedure_len) - 1
        return random.randint(min, max)
    
    def regen_schedule(self):
        self.sch_date = self.gen_sch_date()
        self.sch_time = self.gen_sch_time()
        self.procedure = self.gen_procedure()
        self.aetitle = "ORTHANC"
    
    #SETTERS
    def set_sch_date(self, _sch_date):
        try:
            datetime.strptime(_sch_date, "%Y%m%d")
            self.sch_date = _sch_date
        except ValueError:
            raise ValueError("Incorrect date format, should be YYYYMMDD")
    
    def set_sch_time(self, _sch_time):
        try:
            datetime.strptime(_sch_time, "%H%M%S")
            self.sch_time = _sch_time
        except ValueError:
            raise ValueError("Incorrect time format, should be HHMMSS")
    
    def set_margin_days(self, _margin_days):
        if _margin_days < 0:
            raise ValueError("Margin days cannot be negative")
        else:
            self.margin_days = _margin_days
    
    def set_procedure(self, _procedure):
        if _procedure < 10**(self.procedure_len - 1) or _procedure > (10**self.procedure_len) - 1:
            raise ValueError(f"Procedure should be {self.procedure_len} digits long")
        else:
            self.procedure = _procedure
    
    def set_procedure_len(self, _procedure_len):
        if _procedure_len < 0:
            raise ValueError("Procedure length cannot be negative")
        else:
            self.procedure_len = _procedure_len
    
    def set_aetitle(self, _aetitle):
        if _aetitle == "":
            raise ValueError("AETitle cannot be empty")
        else:
            self.aetitle = _aetitle
    
    #GETTERS
    def get_sch_date(self):
        if self.sch_date == "":
            self.sch_date = self.gen_sch_date()
        return self.sch_date
    
    def get_sch_time(self):
        if self.sch_time == "":
            self.sch_time = self.gen_sch_time()
        return self.sch_time
    
    def get_procedure(self):
        if self.procedure == "":
            self.procedure = self.gen_procedure()
        return self.procedure
    
    def get_aetitle(self):
        return self.aetitle
    
    def get_schedule(self):
        return self.sch_date, self.sch_time, self.procedure, self.aetitle
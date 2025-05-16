import pandas as pd #CSV DEPENDENCY
import random #RANDOM DEPENDENCY
from datetime import datetime, timedelta #DATETIME DEPENDENCY
import string #STRING DEPENDENCY

class patient: #PATTIENT CLASS
    #PATIENT DATA
    name = "" #PATIENT NAME
    surname = "" #PATIENT SURNAME
    full_name = "" #PATIENT FULL NAME
    date_of_birth ="" #PATIENT DATE OF BIRTH
    gender = "" #PATIENT GENDER
    id = "" #PATIENT ID
    md = "" #MODALITY
    md_desc = "" #MODALITY DESCRIPTION
    doc = "" #DOCTOR
    
    #LIST FROM FILES
    male_names = [] #MALE NAMES
    female_names = [] #FEMALE NAMES
    surnames = [] #SURNAME NAMES
    modalities = [] #MODALITY
    doctors = [] #DOCTORS

    #INTERNAL USEFULL VARIABLES
    min_age = 0 #MIN AGE TO GENERATE DATE OF BIRTH
    max_age = 100 #MAX AGE TO GENERATE DATE OF BIRTH
    len = 8 #LENGTH OF ID
   

    def __init__(self,_min_age='', _max_age=''): #CONSTRUCTOR
        if _min_age == '': self.min_age = 0 #SET MIN AGE
        if _max_age == '': self.max_age = 100 #SET MAX AGE
        self.db_names() #LOAD CSV FILES
        self.db_modalities() #LOAD MODALITY
        self.db_doctors() #LOAD DOCTORS

    def randomize_list(self, _list): #RANDOMIZE FUNCTION
        random.shuffle(_list)
        return _list
    
    def db_names(self): #LOAD CSV FILES
        csv_male_names = pd.read_csv("csv_data/male.csv", header=None, names=["male"])
        csv_female_names = pd.read_csv("csv_data/female.csv", header=None,names=["female"])
        csv_surnames = pd.read_csv("csv_data/surname.csv", header=None, names=["surname"])
        self.male_names = self.randomize_list(csv_male_names["male"].tolist())
        self.female_names = self.randomize_list(csv_female_names["female"].tolist())
        self.surnames = self.randomize_list(csv_surnames["surname"].tolist())

    def db_modalities(self): #LOAD CSV FILES
        csv_modalities = pd.read_csv("csv_data/modalities.csv", header=None, names=["modaility","description"])
        csv_modalities = csv_modalities.sample(frac=1).reset_index(drop=True)
        self.modalities = list(csv_modalities.itertuples(index=False, name=None))

    def db_doctors(self): #LOAD CSV FILES
        csv_doctors = pd.read_csv("csv_data/doctors.csv", header=None, names=["doctor"])
        self.doctors = self.randomize_list(csv_doctors["doctor"].tolist())

    #DATA GENERATION
    def gen_dob(self): #GENERATE DATE OF BIRTH
        dob = datetime.today() - timedelta(days=(random.randint(self.min_age, self.max_age) * 365 + random.randint(0, 364))) #GET CURRANT DATE AND SUBTRACT AGE IN DAYS CALCULATED BY RANDOM AGE BY YEARS AND ADD SOME DAYS
        return dob.date().isoformat() #FORMAT YYYY-MM-DD

    def gen_full_name(self): #GENERATE FULL NAME FROM GENDER
        if self.gender == "": self.gender = self.gen_gender()
        self.surname = random.choice(self.surnames)
        if self.gender == "M":
            self.name = male_name = random.choice(self.male_names)
            return male_name+" "+self.surname
        elif self.gender == "F":
            self.name = female_name = random.choice(self.female_names)
            return female_name+" "+self.surname
    
    def gen_gender(self): #GENERATE gENDER
        return random.choice(['M', 'F'])
    
    def gen_modality(self): #GENERATE MODALITY
        modalitie = random.choice(self.modalities)
        return modalitie[0], modalitie[1]
    
    def gen_id(self): #GENERATE ID
        chrs = string.ascii_uppercase + string.digits
        return ''.join(random.choices(chrs, k=self.len))

    def gen_doctor(self): #GENERATE DOCTOR
        return random.choice(self.doctors)
    
    def gen_patient(self): #GENERATE PATIENT
        if self.gender == "": self.gender = self.gen_gender()
        if self.full_name == "": self.full_name = self.gen_full_name()
        if self.date_of_birth == "": self.date_of_birth = self.gen_dob()
        if self.id == "": self.id = self.gen_id()
        if self.md == "": self.md, self.md_desc = self.gen_modality()
        if self.doc == "": self.doc = self.gen_doctor()

    def regen_patient(self): #REGENERATE PATIENT
        self.gender = self.gen_gender()
        self.full_name = self.gen_full_name()
        self.date_of_birth = self.gen_dob()
        self.id = self.gen_id()
        self.md, self.md_desc = self.gen_modality()
        self.doc = self.gen_doctor()

    #SETTERS
    def set_gender(self, _gender): #SET GENDER
        if _gender in ['M', 'F']:
            self.gender = _gender
        else:
            raise ValueError("Incorrect gender, should be M or F")
        
    def set_dob(self, _dob): #SET DATE OF BIRTH
        try:
            datetime.strptime(_dob, "%Y-%m-%d")
            self.date_of_birth = _dob
        except ValueError:
            raise ValueError("Incorrect date format, should be YYYY-MM-DD")
    
    def set_full_name(self, _full_name): #SET FULL NAME
        if _full_name == "":
            raise ValueError("Full name cannot be empty")
        else:
            self.full_name = _full_name
            name_parts = _full_name.split(" ")
            if len(name_parts) == 2:
                self.name = name_parts[0]
                self.surname = name_parts[1]
            else:
                raise ValueError("Full name should contain first and last name")
    
    def set_id(self, _id): #SET ID
        if _id == "":
            raise ValueError("ID cannot be empty")
        else:
            self.id = _id

    def set_modality(self, _modality, _modality_desc): #SET MODALITY
        if _modality == "" or _modality_desc == "":
            raise ValueError("Modality and description cannot be empty")
        else:
            self.md = _modality
            self.md_desc = _modality_desc

    def set_age_range(self, _min_age, _max_age): #SET AGE RANGE
        self.min_age = _min_age
        self.max_age = _max_age
    
    def set_len(self, _len): #SET LENGTH OF ID
        if _len < 1:
            raise ValueError("Length should be greater than 0")
        else:
            self.len = _len
    
    def set_doctor(self, _doctor): #SET DOCTOR
        if _doctor == "":
            raise ValueError("Doctor cannot be empty")
        else:
            self.doc = _doctor

    # GETTERS
    def get_gender(self): #GET GENDER
        return self.gender

    def get_dob(self): #GET DATE OF BIRTH
        if self.date_of_birth == "":
            self.date_of_birth = self.gen_dob()
        return self.date_of_birth

    def get_age(self): #GET AGE
        if self.date_of_birth == "":
            self.date_of_birth = self.gen_dob()
        dob = datetime.strptime(self.date_of_birth, "%Y-%m-%d")
        age = datetime.today().year - dob.year - ((datetime.today().month, datetime.today().day) < (dob.month, dob.day))
        return age
    
    def get_full_name(self): #GET FULL NAME
        if self.full_name == "":
            self.full_name = self.gen_full_name()
        return self.full_name
   
    def get_id(self): #GET ID
        if self.id == "":
            self.id = self.gen_id()
        return self.id
    
    def get_modality(self): #GET MODALITY
        if self.md == "":
            self.md, self.md_desc = self.gen_modality()
        return self.md, self.md_desc
    
    def get_doctor(self): #GET DOCTOR
        if self.doc == "":
            self.doc = self.gen_doctor()
        return self.doc
    
    def get_patient(self): # GET ALL DATA
        if self.full_name == "" or self.date_of_birth == "" or self.id == "" or self.md == "" or self.doc == "":
            self.gen_patient()
        return self.full_name, self.gender, self.date_of_birth, self.id, self.md, self.md_desc, self.doc
 


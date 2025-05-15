#IMPORT NATIVE DEPENDENCIES
import pandas as pd #CSV DEPENDENCY
import random #RANDOM DEPENDENCY
from datetime import datetime, timedelta #DATETIME DEPENDENCY
import string  #STRING DEPENDENCY
import os

#IMPORT EXTERNAL DEPENDENCIES
import pydicom
from pydicom.dataset import Dataset, FileDataset

#OWN CLASSES
class patient: #PATTIENT CLASS
    name = "" #PATIENT NAME
    surname = "" #PATIENT SURNAME
    full_name = "" #PATIENT FULL NAME
    date_of_birth ="" #PATIENT DATE OF BIRTH
    gender = "" #PATIENT GENDER
    id = "" #PATIENT ID
    
    male_names = [] #MALE NAMES
    female_names = [] #FEMALE NAMES
    surnames = [] #SURNAME NAMES
    modalities = [] #MODALITY
    doctors = [] #DOCTORS

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

    def gen_full_name(self): #GET FULL NAME FROM GENDER
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
    
    def gen_patient(self): #GENERATE PATIENT
        if self.gender == "": self.gender = self.gen_gender()
        if self.full_name == "": self.full_name = self.gen_full_name()
        if self.date_of_birth == "": self.date_of_birth = self.gen_dob()
        if self.id == "": self.id = self.gen_id()

    def regen_patient(self): #REGENERATE PATIENT
        self.gender = self.gen_gender()
        self.full_name = self.gen_full_name()
        self.date_of_birth = self.gen_dob()
    
    def gen_id(self):
        chrs = string.ascii_uppercase + string.digits
        return ''.join(random.choices(chrs, k=self.len))

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

    def set_age_range(self, _min_age, _max_age): #SET AGE RANGE
        self.min_age = _min_age
        self.max_age = _max_age
    
    def set_len(self, _len): #SET LENGTH OF ID
        if _len < 1:
            raise ValueError("Length should be greater than 0")
        else:
            self.len = _len

    # GETTERS
    def get_gender(self):
        return self.gender

    def get_dob(self): #GET DATE OF BIRTH
        if self.date_of_birth == "":
            self.date_of_birth = self.gen_dob()
        return self.date_of_birth

    def get_age(self):
        if self.date_of_birth == "":
            self.date_of_birth = self.gen_dob()
        dob = datetime.strptime(self.date_of_birth, "%Y-%m-%d")
        age = datetime.today().year - dob.year - ((datetime.today().month, datetime.today().day) < (dob.month, dob.day))
        return age
    
    def get_full_name(self): #GET FULL NAME
        if self.full_name == "":
            self.full_name = self.gen_full_name()
        return self.full_name

    def get_patient(self): # GET ALL DATA
        if self.full_name == "" or self.date_of_birth == "":
            self.gen_patient()
        return self.full_name, self.gender, self.date_of_birth, self.id
    
    def get_id(self): #GET ID
        if self.id == "":
            self.id = self.gen_id()
        return self.id

class patient_id: #PATIENT ID CLASS
    def gen_patient_id(self, _len=8):
        chrs = string.ascii_uppercase + string.digits
        return ''.join(random.choices(chrs, k=_len))

    def multiple_gen_patient_id(self, _total, _len=8):
        ids = set()
        while len(ids) < _total:
            ids.add(self.gen_patient_id(_len))
        return list(ids)


def crear_worklist(filepath, patient_name, patient_id, birth_date, sex, accession_number, study_date, modality="CT"):
    # Crear dataset principal
    ds = Dataset()

    # Tags requeridos (mínimos para un WL válido)
    ds.PatientName = patient_name
    ds.PatientID = patient_id
    ds.PatientBirthDate = birth_date
    ds.PatientSex = sex
    ds.AccessionNumber = accession_number
    ds.Modality = modality
    ds.ScheduledProcedureStepStartDate = study_date
    ds.ScheduledProcedureStepStartTime = "120000"
    ds.ScheduledPerformingPhysicianName = "Dr. House"
    ds.ScheduledProcedureStepDescription = "CT Abdomen"
    ds.ScheduledStationAETitle = "ORTHANC"
    ds.ScheduledProcedureStepID = "12345"
    ds.RequestedProcedureID = "54321"

    # Encapsularlo en un FileDataset
    meta = Dataset()
    meta.MediaStorageSOPClassUID = pydicom.uid.UID("1.2.840.10008.5.1.4.31")  # Modality Worklist Info Model - FIND
    meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
    meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian

    filename = os.path.join(filepath, f"{patient_id}.wl")
    file_meta = FileDataset(filename, {}, file_meta=meta, preamble=b"\0" * 128)

    # Copiar los datos
    for elem in ds:
        file_meta.add(elem)

    # Guardar archivo
    file_meta.is_little_endian = True
    file_meta.is_implicit_VR = True
    file_meta.save_as(filename)

    return filename

if __name__ == '__main__':
    print("go")
    num_items= 10
    pid = patient_id()
    id_list = pid.multiple_gen_patient_id(num_items, 8)
    pat = patient()
    for i in range(num_items):
        fn, g, dob, id = pat.get_patient()
        pat.set_id(id_list[i])        
        print("Full name: ", fn)
        print("gender: ", g)
        print("date of birth: ", dob)
        print("patient id: ", id,"\n")
        pat.regen_patient()
    crear_worklist(
        filepath=".",  # o un directorio como "./worklist"
        patient_name="Juan Perez",
        patient_id="P001",
        birth_date="19850101",
        sex="M",
        accession_number="ACC001",
        study_date="20250514"
    )

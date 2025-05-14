#IMPORT DEPENDENCIES
import pandas as pd #CSV DEPENDENCY
import random #RANDOM DEPENDENCY

#OWN CLASSES
class patient: #PATTIENT CLASS
    name = "" #PATIENT NAME
    surname = "" #PATIENT SURNAME
    dob ="" #PATIENT DATE OF BIRTH
    gender = "" #PATIENT GENDER

class pdata: #PATIENT DATABASE CLASS
    male_names = [] #MALE NAMES
    female_names = [] #FEMALE NAMES
    surnames = [] #SURNAME NAMES

    def randomize(self, _list): #RANDOMIZE FUNCTION
        random.shuffle(_list)
        return _list

    def get_patients_list(self, _gender): #GET FULL NAME FROM GENDER
        if _gender == "M":
            return random.choice(self.male_names)+" "+random.choice(self.surnames)
        elif _gender == "F":
            return random.choice(self.female_names)+" "+random.choice(self.surnames)
        else:
            _gender = random.choice(['M', 'F'])
            return self.get_patients_list(_gender)


    def __init__(self): #LOAD CSV FILES
        csv_male_names = pd.read_csv("csv_data/male.csv", header=None, names=["male"])
        csv_female_names = pd.read_csv("csv_data/female.csv", header=None,names=["female"])
        csv_surnames = pd.read_csv("csv_data/surname.csv", header=None, names=["surname"])
        self.male_names = self.randomize(csv_male_names["male"].tolist())
        self.female_names = self.randomize(csv_female_names["female"].tolist())
        self.surnames = self.randomize(csv_surnames["surname"].tolist())

if __name__ == '__main__':
    print("go")
    pdata = pdata()

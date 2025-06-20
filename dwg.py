#IMPORT NATIVE DEPENDENCIES
import pandas as pd #CSV DEPENDENCY
import os
import sys

#IMPORT EXTERNAL DEPENDENCIES
import pydicom
from pydicom.dataset import Dataset, FileDataset
import mysql.connector
from mysql.connector import Error

#OWN DEPENDENCIES
from patient import patient
from scheduling import scheduling
from idsgenerator import idsgenerator
from procgenerator import procgenerator

#GLOBAL VARIABLES
#DEBUGGING
isDebug = False


def worklistit(_filepath, _patient_name, _patient_id, _birth_date, _gender, _accession_number, _study_date, _study_time, _modality, _aetitle, _modality_desc, _doctor, _procedure_sid, _procedure_id, _or_name):
    if isDebug: print(_filepath, _patient_name, _patient_id, _birth_date, _gender, _accession_number, _study_date, _study_time, _modality, _aetitle, _modality_desc, _doctor, _procedure_sid, _procedure_id, _or_name)
    ds = Dataset() #DATASET
    sps = Dataset() #SCHEDULED PROCEDURE STEP SEQUENCE
    ds.PatientName = _patient_name
    ds.PatientID = _patient_id
    ds.PatientBirthDate = _birth_date
    ds.PatientSex = _gender
    ds.AccessionNumber = _accession_number
    sps.Modality = _modality
    sps.ScheduledProcedureStepStartDate = _study_date
    sps.ScheduledProcedureStepStartTime = _study_time
    sps.ScheduledStationName = _or_name
    sps.ScheduledPerformingPhysicianName = _doctor
    sps.ScheduledProcedureStepDescription = _modality_desc
    sps.ScheduledStationAETitle = _aetitle
    sps.ScheduledProcedureStepID = _procedure_sid
    ds.RequestedProcedureID = _procedure_id
    ds.ScheduledProcedureStepSequence = [sps] #ASSIGN SCHEDULED PROCEDURE STEP SEQUENCE

    meta = Dataset() #DATASET OF INTEGRATION IN WL
    meta.MediaStorageSOPClassUID = pydicom.uid.UID("1.2.840.10008.5.1.4.31")  #MODALITY WORKLIST INFO MODEL - FIND
    meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
    meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian

    filename = os.path.join(_filepath, f"{_patient_id}.wl")
    file_meta = FileDataset(filename, {}, file_meta=meta, preamble=b"\0" * 128)

    # Copiar los datos
    for elem in ds:
        file_meta.add(elem)

    # Guardar archivo
    file_meta.is_little_endian = True
    file_meta.is_implicit_VR = True
    file_meta.save_as(filename)

    return filename

def create_multiple_worklists(_how_many=10, _conn=None): #MULTIPLE WORKLIST CREATION
    num_items= _how_many
    sch = scheduling()
    pid = idsgenerator()
    id_list = pid.multiple_gen_id(num_items, 8)
    proc = procgenerator()
    proc_list = proc.multiple_gen_procedure(num_items, 8)
    pat = patient()
    for i in range(num_items):
        pat.set_id(id_list[i])
        fn, g, dob, id, md, md_dec, doc = pat.get_patient()
        sch.set_procedure(proc_list[i])
        date, time, procedure, aetitle, or_name = sch.get_schedule()
        if isDebug: print_worklist(fn, g, dob, md, md_dec, doc, id, date, time, procedure, aetitle, or_name)
        if _conn != None:
            try:
                cursor = conn.cursor()
                query = """
                    INSERT INTO worklist (
                        ScheduledProcedureStepID,
                        PatientID,
                        PatientName,
                        AccessionNumber,
                        StudyInstanceUID,
                        RequestedProcedureID,
                        RequestedProcedureDescription,
                        ScheduledProcedureStepStartDate,
                        ScheduledProcedureStepStartTime,
                        ScheduledPerformingPhysicianName,
                        ScheduledStationAETitle,
                        ScheduledProcedureStepDescription
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    procedure,
                    id,
                    fn,
                    'AACC001',
                    md,
                    procedure,
                    str(procedure)[::-1],
                    date,
                    time,
                    '',
                    'ORTHANC',
                    md_dec
                )
                cursor.execute(query, values)
                conn.commit()
            except Error as e:
                print(f"Data insert error: {e}")
        else:
            worklistit(
                _filepath="worklist_files/",  # FOLDER TO SAVE WL FILES
                _patient_name=fn,
                _patient_id=id,
                _birth_date=str(dob),
                _gender=g,
                _accession_number="ACC001",
                _study_date=str(date),
                _study_time=str(time),
                _aetitle=aetitle,
                _modality=md,
                _modality_desc=md_dec,
                _doctor=doc,
                _procedure_sid=str(procedure),
                _procedure_id=str(procedure)[::-1],
                _or_name=or_name,
            )
            pat.regen_patient()
            sch.regen_schedule()
    print(f"{num_items} worklists created in {os.path.abspath('worklist_files')}")
    print("--------------------------------------------------\n") 

def create_worklist(_conn=None): #WORKLIST CREATION
    pat = patient()
    fn, g, dob, id, md, md_dec, doc = pat.get_patient()
    sch = scheduling()
    date, time, procedure, aetitle = sch.get_schedule()
    if debug: print_worklist(fn, g, dob, md, md_dec, doc, id, date, time, procedure, aetitle)
    if _conn != None:
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO worklist (
                    ScheduledProcedureStepID,
                    PatientID,
                    PatientName,
                    AccessionNumber,
                    StudyInstanceUID,
                    RequestedProcedureID,
                    RequestedProcedureDescription,
                    ScheduledProcedureStepStartDate,
                    ScheduledProcedureStepStartTime,
                    ScheduledPerformingPhysicianName,
                    ScheduledStationAETitle,
                    ScheduledProcedureStepDescription
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                procedure,
                id,
                fn,
                'AACC001',
                md,
                procedure,
                str(procedure)[::-1],
                date,
                time,
                '',
                'ORTHANC',
                md_dec
            )
            cursor.execute(query, values)
            conn.commit()
        except Error as e:
            print(f"Data insert error: {e}")
    else:
        worklistit(
            _filepath="worklist_files/",  # FOLDER TO SAVE WL FILES
            _patient_name=fn,
            _patient_id=id,
            _birth_date=str(dob),
            _gender=g,
            _accession_number="ACC001",
            _study_date=str(date),
            _study_time=str(time),
            _aetitle=aetitle,
            _modality=md,
            _modality_desc=md_dec,
            _doctor=doc,
            _procedure_sid=str(procedure),
            _procedure_id=str(procedure)[::-1],
        )
    print(f"Worklist created in {os.path.abspath('worklist_files')}")
    print("--------------------------------------------------\n")

def create_worklist_manual(_conn = None): #MANUAL WORKLIST CREATION
    print("Enter the following data:")
    fn = input("Full name: ")
    g = input("Gender:")
    dob = input("Date of birth (YYYYMMDD): ")
    id = input("Patient ID: ")
    md = input("Modality: ")
    md_dec = input("Modality description: ")
    doc = input("Doctor: ")
    date = input("Intervention Date (YYYYMMDD): ")
    time = input("Intervention Time (HHMMSS): ")
    procedure = input("Procedure: ")
    print("--------------------------------------------------")
    pat = patient()
    pat.set_full_name(fn)
    pat.set_gender(g)
    pat.set_dob(dob)
    pat.set_modality(md, md_dec)
    pat.set_doctor(doc)
    if id == "": pat.set_id(pat.get_id())
    fn, g, dob, id, md, md_dec, doc = pat.get_patient()
    sch = scheduling()
    if procedure == "": sch.set_procedure(sch.get_procedure())
    sch.set_sch_date(date)
    sch.set_sch_time(time)
    date, time, procedure, aetitle = sch.get_schedule()
    if debug: print_worklist(fn, g, dob, md, md_dec, doc, id, date, time, procedure, aetitle)
    if _conn != None:
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO worklist (
                    ScheduledProcedureStepID,
                    PatientID,
                    PatientName,
                    AccessionNumber,
                    StudyInstanceUID,
                    RequestedProcedureID,
                    RequestedProcedureDescription,
                    ScheduledProcedureStepStartDate,
                    ScheduledProcedureStepStartTime,
                    ScheduledPerformingPhysicianName,
                    ScheduledStationAETitle,
                    ScheduledProcedureStepDescription
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                procedure,
                id,
                fn,
                'AACC001',
                md,
                procedure,
                str(procedure)[::-1],
                date,
                time,
                '',
                'ORTHANC',
                md_dec
            )
            cursor.execute(query, values)
            conn.commit()
        except Error as e:
            print(f"Data insert error: {e}")
    else:
        worklistit(
            _filepath="worklist_files/",  # FOLDER TO SAVE WL FILES
            _patient_name=fn,
            _patient_id=id,
            _birth_date=str(dob),
            _gender=g,
            _accession_number="ACC001",
            _study_date=str(date),
            _study_time=str(time),
            _aetitle=aetitle,
            _modality=md,
            _modality_desc=md_dec,
            _doctor=doc,
            _procedure_sid=str(procedure),
            _procedure_id=str(procedure)[::-1],
        )
    print(f"Worklist created in {os.path.abspath('worklist_files')}")
    print("--------------------------------------------------\n")

def print_worklist(_fn, _g, _dob, _id, _md, _md_dec, _doc, _date, _time, _procedure, _aetitle, _or_name): #PRINT DATA BEFORE CREATING WL
    print("full name: ", _fn)
    print("gender: ", _g)
    print("date of birth: ", _dob)
    print("modality: ", _md)
    print("modality description: ", _md_dec)
    print("doctor: ", _doc)
    print("patient id: ", _id)
    print("date: ", _date)
    print("time: ", _time)
    print("procedure: ", _procedure)
    print("aetitle: ", _aetitle,"\n")
    print("OR Name: ", _or_name,"\n")
    print("--------------------------------------------------")


def conectar_bd(_server, _db_name, _user, _pass): #CONNECTION TO MYSQL
    try:
        conn = mysql.connector.connect(
            host=_server, 
            port=3306, 
            user=_user,
            password=_pass,
            database=_db_name
        )
        if conn.is_connected():
            print("Connected to MySQL Server")
            return conn
    except Error as e:
        print(f"MySQL connection error: {e}")
        return None


if __name__ == '__main__':
    conn = None
    while True:
        print("Welcome to the Worklist Data Generator")
        print("--------------------------------------\n")
        mode = input("""Select the mode of operation:
Press F for create files
Press D for database
Press E for exit\n""").upper()
        while mode not in ["F", "D", "E"]:
            print("Invalid option")
            mode = input("""Select the mode of operation:
Press F for create files
Press D for database
Press E for exit\n""").upper()
        if mode == "F":
            print("Files mode")
            if not os.path.exists("worklist_files"):
                os.makedirs("worklist_files")
            print("Worklist files will be created in worklist_files folder")
        elif mode == "D":
            print("Database mode")
            db_server = input("Enter the database server: ")
            db_name = input("Enter the database name: ")
            db_user = input("Enter the database user: ")
            db_pass = input("Enter the database password: ")
            conn = conectar_bd(db_server, db_name, db_user, db_pass)
        elif mode == "E":
            print("Good Bye")
            sys.exit()
        else:
            print("Invalid option")
        print("--------------------------------------------------\n")

        print("""Press 1 to create one worklis
Press 2 to create multiple worklists
Press 3 for manual worklist creation
Press 4 to exit\n""")
        option = input("Option: ")
        if option == "1":
            create_worklist(conn)
        elif option == "2":
            num_items = int(input("How many worklists do you want to create? "))
            create_multiple_worklists(num_items, conn)
        elif option == "3":
            create_worklist_manual(conn)
        elif option == "4":
            print("Good Bye")
            sys.exit()
        else:
            print("Invalid option")

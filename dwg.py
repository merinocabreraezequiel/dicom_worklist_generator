#IMPORT NATIVE DEPENDENCIES
import pandas as pd #CSV DEPENDENCY
import os

#IMPORT EXTERNAL DEPENDENCIES
import pydicom
from pydicom.dataset import Dataset, FileDataset

#OWN DEPENDENCIES
from patient import patient
from scheduling import scheduling
from idsgenerator import idsgenerator
from procgenerator import procgenerator


def worklistit(_filepath, _patient_name, _patient_id, _birth_date, _gender, _accession_number, _study_date, _modality, _modality_desc, _doctor):
    ds = Dataset() #DATASET
    ds.PatientName = _patient_name
    ds.PatientID = _patient_id
    ds.PatientBirthDate = _birth_date
    ds.PatientSex = _gender
    ds.AccessionNumber = _accession_number
    ds.Modality = _modality
    ds.ScheduledProcedureStepStartDate = _study_date
    ds.ScheduledProcedureStepStartTime = "120000"
    ds.ScheduledPerformingPhysicianName = _doctor
    ds.ScheduledProcedureStepDescription = _modality_desc
    ds.ScheduledStationAETitle = "ORTHANC"
    ds.ScheduledProcedureStepID = "12345"
    ds.RequestedProcedureID = "54321"

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

if __name__ == '__main__':
    print("go")
    num_items= 10
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
        date, time, procedure, aetitle = sch.get_schedule()
        print("full name: ", fn)
        print("gender: ", g)
        print("date of birth: ", dob)
        print("modality: ", md)
        print("modality description: ", md_dec)
        print("doctor: ", doc)
        print("patient id: ", id)
        print("date: ", date)
        print("time: ", time)
        print("procedure: ", procedure)
        print("aetitle: ", aetitle,"\n")
        pat.regen_patient()
        sch.regen_schedule()
        #crear_worklist(
        #    filepath=".",  # o un directorio como "./worklist"
        #    patient_name="Juan Perez",
        #    patient_id="P001",
        #    birth_date="19850101",
        #    sex="M",
        #    accession_number="ACC001",
        #    study_date="20250514"
        #)

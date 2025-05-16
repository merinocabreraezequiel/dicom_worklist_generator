#IMPORT NATIVE DEPENDENCIES
import pandas as pd #CSV DEPENDENCY
import os

#IMPORT EXTERNAL DEPENDENCIES
import pydicom
from pydicom.dataset import Dataset, FileDataset

#OWN DEPENDENCIES
from patient import patient
from idsgenerator import idsgenerator


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
    pid = idsgenerator()
    id_list = pid.multiple_gen_id(num_items, 8)
    pat = patient()
    for i in range(num_items):
        fn, g, dob, id, md, md_dec, doc = pat.get_patient()
        pat.set_id(id_list[i])        
        print("full name: ", fn)
        print("gender: ", g)
        print("date of birth: ", dob)
        print("modality: ", md)
        print("modality description: ", md_dec)
        print("doctor: ", doc)
        print("patient id: ", id,"\n")
        pat.regen_patient()
    #crear_worklist(
    #    filepath=".",  # o un directorio como "./worklist"
    #    patient_name="Juan Perez",
    #    patient_id="P001",
    #    birth_date="19850101",
    #    sex="M",
    #    accession_number="ACC001",
    #    study_date="20250514"
    #)

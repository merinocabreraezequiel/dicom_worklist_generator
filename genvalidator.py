from pydicom import dcmread

# Ruta a tu archivo .wl
ds = dcmread("worklist_files/1MOGBSBU.wl")

# Mostrar si la secuencia obligatoria existe
if "ScheduledProcedureStepSequence" in ds:
    sps = ds.ScheduledProcedureStepSequence[0]
    print("✔️ La secuencia ScheduledProcedureStepSequence está presente.")
    print("ScheduledProcedureStepStartDate:", getattr(sps, "ScheduledProcedureStepStartDate", "NO DEFINIDO"))
    print("ScheduledProcedureStepStartTime:", getattr(sps, "ScheduledProcedureStepStartTime", "NO DEFINIDO"))
else:
    print("❌ Falta la secuencia ScheduledProcedureStepSequence.")

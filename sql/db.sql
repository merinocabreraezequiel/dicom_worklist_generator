CREATE DATABASE IF NOT EXISTS dicomweb;
USE dicomweb;
CREATE TABLE worklist (
  ScheduledProcedureStepID     VARCHAR(64),
  PatientID                    VARCHAR(64),
  PatientName                  VARCHAR(64),
  AccessionNumber              VARCHAR(64),
  StudyInstanceUID             VARCHAR(64),
  RequestedProcedureID         VARCHAR(64),
  RequestedProcedureDescription VARCHAR(64),
  ScheduledProcedureStepStartDate DATE,
  ScheduledProcedureStepStartTime TIME,
  ScheduledPerformingPhysicianName VARCHAR(64),
  ScheduledStationAETitle      VARCHAR(64),
  ScheduledProcedureStepDescription VARCHAR(64)
);
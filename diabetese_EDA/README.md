# ****************************************\*\*\*\*****************************************

## Project 1: Data cleaning & EDA case study

# ****************************************\*\*\*\*****************************************

## Project Goal

The goal of this project is to apply the skills, knowledge & concepts
of data science to an investigation of outcomes derived from this dataset. There
is an extensive amount of data to be examined, but the primary data that should
be used for measuring outcomes is stored in the files with "RTCGM" in the name.
RT-CGM stands for Real Time Continuous Glucose Monitor & is the
primary medical device / tool used today in diabetes management for patients with
Type 1 diabetes and for many with Type 2 / other forms of diabetes.
This project investigates data from a publically
available dataset focusing on Real-Time Continuous Glucose Monitor
use in patients with Type 1 Diabetes. As this is a public dataset
derived from a published Clinical Trial, the following disclaimer
applies in regard to the intent of use & results investigated while
using this dataset:

# ****************************************\*\*\*\*****************************************

**The source of the data is the _The Juvenile Diabetes Research Foundation
Continuous Glucose Monitoring Study Group_, but the analyses, content
and conclusions presented herein are solely the responsibility of the authors
and have not been reviewed or approved by the aforementioned study ownwers.**

Links to dataset & publication

- [data](xxx)
- [Publication 1: Outcomes for T1 patients with A1C <7%](https://diabetesjournals.org/care/article/32/8/1378/38871/The-Effect-of-Continuous-Glucose-Monitoring-in)
- [Publication 1: Outcomes for T1 patients with A1C ≥7%](https://www.nejm.org/doi/full/10.1056/NEJMoa0805017)

The data falls into 1 of 4 categories: (1) RT-CGM data, (2) Lab A1C values, (3) patient demographics & (4) patient responses to surveys (questionnaires).

The _primary_ tables utilized to generate new features from and calculate outcomes with are those with the: _tblADataRTCGM_ pattern, relating to (1) CGM data. These tables contain EGVs (see diabetes & CGM background) collected at sample frequencies with CGM for all patients, with one record per one CGM reading. There are several files (see study overview), and glucose data for both groups, so you will find CGM data for: 1. Baseline - Both groups - blinded (patients in both cohorts wearing CGM, neither having access to EGVs / readings at any point, used to get patients assimialted to wearing devices)

    	2. RTCGM group (treatment group) - first & second 26-week study period unblinded (patients wore CGM & can see EGVs via receiver or phone)

    	3. Control group - first 26-week period (blinded - patients wore CGM, but did not get any data / readings, data only stored and analyzed retrospectively) & second 26-week period (patients continued to wear CGM, but could now see data coming in through receiver or phone)

# Tombstone Toponym Identification using OCR and NER

This project utilizes Optical Character Recognition (OCR) and Natural Language Processing (NLP) techniques to automate the transcription and toponym identification from Dutch tombstone inscriptions. 
The goal is to enhance the efficiency and accuracy of digital cultural heritage documentation.

## Description

This research project addresses the challenge of preserving historical data inscribed on tombstones.
By applying advanced image preprocessing techniques and OCR, the project aims to transcribe tombstone text into a machine-readable format. 
The use of Named Entity Recognition (NER) further assists in identifying and resolving toponyms, providing a significant contribution to the field of digital heritage preservation.

## Usage
As input our systems takes an image of a tombstone in .jpg format, such as t00000.jpg, t00022.jpg & t000529.jpg.
As final output it delivers toponyms detected on the tombstone inscription in the form of a GeoNames identifier.

First we apply Tesseract-OCR to the image by running the following command:

for file in t00000.jpg t00022.jpg t00529.jpg ; do tesseract "$file" "${file%%.*}" ; done

Tesseract output will then be stored as t00000.txt, t00022.txt & t00529.txt.
These files can be used as input for our main program, toponym.py as follows:

for file in t00000.txt t00022.txt t00529.txt ; do python3 toponym.py "$file" "${file%%.*}" ; done

The toponyms detected by our system will be stored in a file named Found_Toponyms.txt.

This file can be evaluated for precision, recall & F1-score against our gold_standard.txt by running:
python3 evaluate.py

## Data
Our dataset is too large to upload to Github, we are currently working on a workaround!

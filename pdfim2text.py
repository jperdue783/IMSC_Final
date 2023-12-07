#!/usr/bin/python

import pytesseract
from pdf2image import convert_from_path
from PIL import Image 
from gtts import gTTS
from playsound import playsound
import os, pathlib, glob
from termcolor import colored

def takeInput():
    pmode = 0;
    IN = input("Enter a pdf or an image: ")
    if os.path.isfile(IN):
        path_stem = pathlib.Path(IN).stem
        path_ext  = pathlib.Path(IN).suffix
        if path_ext.lower() == '.pdf': pmode=1
    else:
        exit()
    return IN, path_stem, pmode

def pdf2txt(IN):

    pdf_path = IN

    pages = convert_from_path(pdf_path, 500)

    for pageNum, imgBlob in enumerate(pages):

        text = pytesseract.image_to_string(imgBlob, config=r'--psm 3', lang='eng')

        with open(f'{pdf_path[:-4]}_page{pageNum}.txt', 'w') as the_file:
            the_file.write(text)

def im2txt(IN):
    # Read to open the image file

    if IN == "": exit()
    image = Image.open(IN)

    # Perform OCR using PyTesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(image)

    # Print the extracted text
    return text

if __name__ == '__main__':
    IN, path_stem, pmode = takeInput()   #pmode=0:image; pmode=1:pdf
    if pmode:
        txt = pdf2txt(IN)
    else:
        txt = im2txt(IN)
        print(txt)

    # ----------------------------------------- unnecessary ----------------
    # audio = gTTS(text=txt, lang="en", slow=False);
    # WAV = '0000-' + path_stem + '-text.wav';
    # audio.save(WAV); print(colored('Text: saved to <%s>' %(WAV),'yellow'))
    # playsound(WAV); # This library and function do not work
    # os.remove(WAV) # The audio file is not removed so it can be played for verification.

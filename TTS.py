from gtts import gTTS
import speech_recognition as sr
from playsound import playsound
import os, pathlib
from pydub import AudioSegment

r = sr.Recognizer()

file = input("Enter an audio file or press enter to record: ")

# no filename, so record from mic
if file == "":
    while(1): # loop until mic hears something

        try: # Allows repeatedly throwing errors until audio is detected
            with sr.Microphone() as mic:

                r.adjust_for_ambient_noise(mic, duration=0.2)
                audio = r.listen(mic)

                MyText = r.recognize_google(audio) #SST

                #Sanity Check
                print("Did you say ",MyText)

                #Save file, play sound, remove sound
                tts = gTTS(MyText, lang='en')
                filename = '0000-my_gtts_file.mp3'
                tts.save(filename)
                playsound(filename)

                import os
                os.remove(filename)
                break

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occurred")

else: #if a filename was input

    #Check for file
    if os.path.isfile(file):
        path_stem = pathlib.Path(file).stem
        path_ext = pathlib.Path(file).suffix

        if path_ext.lower() == '.mp3': # Convert to WAV
            sound = AudioSegment.from_mp3("/path/to/file.mp3")
            sound.export("/output/path/file.wav", format="wav")


        with sr.AudioFile(file) as source:
            print("Converting WAV to audio file")
            r.pause_threshold = 0.6
            audio = r.record(source)

        MyText = r.recognize_google(audio)

        print("Did you say ", MyText)
        tts = gTTS(MyText, lang='en')
        filename = '0000-my_gtts_file.mp3'
        tts.save(filename)
        playsound(filename)

        import os

        os.remove(filename)

    else:
        print("File not found")

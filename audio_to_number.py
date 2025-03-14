import time
from vosk import Model, KaldiRecognizer,SetLogLevel
import wave
import json
import requests 
import io

def audio_to_number(url:str):
    start_time=time.time()
    audio_path="audio_01.wav"
    model_path="vosk-model-small-en-us-0.15"
    SetLogLevel(-1)
    
    number_map = {
    # Zero
    "zero": "0", "zirro": "0", "zeero": "0", "zaro": "0", 
    "zeerow": "0", "sero": "0", "zrow": "0", "zer": "0",
    
    # One
    "one": "1", "won": "1", "wun": "1", "on": "1", 
    "wone": "1", "wan": "1", "uhn": "1", "once": "1",
    
    # Two
    "two": "2", "too": "2", "to": "2", "tue": "2", 
    "twoo": "2", "tou": "2", "tu": "2", "tew": "2",
    
    # Three
    "three": "3", "tree": "3", "thre": "3", "free": "3", 
    "thwee": "3", "thri": "3", "tre": "3", "fwee": "3",
    
    # Four
    "four": "4", "for": "4", "fore": "4", "fo": "4", 
    "faur": "4", "fow": "4", "foe": "4", "phor": "4",
    
    # Five
    "five": "5", "fife": "5", "fiv": "5", "fyve": "5", 
    "faiv": "5", "fiev": "5", "fif": "5", "phive": "5",
    
    # Six
    "six": "6", "siks": "6", "sex": "6", "sik": "6", 
    "sick": "6", "sis": "6", "seks": "6", "zix": "6",
    
    # Seven
    "seven": "7", "sevn": "7", "sevan": "7", "saven": "7","said": "7",
    "sev": "7", "seben": "7", "sewen": "7", "sven": "7",
    
    # Eight
    "eight": "8", "ate": "8", "eit": "8", "eigt": "8", 
    "aight": "8", "eitgh": "8", "eyt": "8", "hate": "8",
    
    # Nine
    "nine": "9", "nyn": "9", "nin": "9", "naine": "9", 
    "nien": "9", "nyne": "9", "nign": "9", "nein": "9"
    }
    try:
        model = Model(model_path)
        recognizer = KaldiRecognizer(model, 16000)
        
        # Choose audio source
        if url:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            audio_data = io.BytesIO(response.content)
        else:
            audio_data = audio_path

        
        with wave.open(audio_data, "rb") as wf:
            recognizer.AcceptWaveform(wf.readframes(wf.getnframes()))
            text = json.loads(recognizer.Result())["text"]

        # Convert text to numbers
        words = text.split()
        words=words[-6:]
        print(words)
        number = "".join(number_map.get(word, "") for word in words)
        time_taken=float(time.time()-start_time)
        if time_taken<6:
            print('2 sec sleeping time for not getting blocked')
            time.sleep(2)
            
        print(f'Number { number if number else "none"} generating in .. {time_taken} sec')
        return number if number else None
    except Exception as e:
        print(f"Network error: {e}")
        return None
    
# audio_to_number("https://dd.prod.captcha-delivery.com/audio/2025-03-11/en/498c91f2e1787e81c55389b0e895386a.wav")
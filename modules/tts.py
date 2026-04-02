# -*- coding: utf-8 -*-
import subprocess

def speak(text):
    try:
        # Alle problematischen Zeichen ersetzen
        clean = text.encode('ascii', 'ignore').decode('ascii')
        clean = clean.replace('"', '').replace("'", '').replace('\n', ' ')
        
        cmd = f'espeak -v de -s 150 "{clean}" --stdout | sox -t wav - -t wav -r 48000 -c 2 - | aplay -D hw:1,0'
        subprocess.run(cmd, shell=True, check=False, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"TTS Fehler: {e}", flush=True)
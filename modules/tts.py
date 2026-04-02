# -*- coding: utf-8 -*-
import subprocess
import os

def speak(text):
    """Spricht Text über den WM8960 Lautsprecher"""
    try:
        # Sonderzeichen bereinigen
        clean_text = text.replace('"', '').replace("'", '').replace('\n', ' ')
        
        cmd = f'espeak -v de -s 130 "{clean_text}" --stdout | sox -t wav - -t wav -r 48000 -c 2 - | aplay -D hw:1,0'
        subprocess.run(cmd, shell=True, check=False,
                      stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"TTS Fehler: {e}", flush=True)
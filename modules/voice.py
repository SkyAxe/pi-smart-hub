# -*- coding: utf-8 -*-
import speech_recognition as sr
import threading
import time
import os
import sys

# ALSA Warnungen unterdrücken
os.environ['PYTHONWARNINGS'] = 'ignore'
devnull = os.open(os.devnull, os.O_WRONLY)
old_stderr = os.dup(2)

TRIGGER_WORDS = ["hey claude", "hallo claude", "claude"]
MIC_INDEX = 1
SAMPLE_RATE = 48000

class VoiceModule:
    def __init__(self, on_trigger_callback):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 1500
        self.recognizer.dynamic_energy_threshold = False
        self.on_trigger = on_trigger_callback
        self.is_listening = False
        self.is_processing = False
        self.thread = None

    def start(self):
        self.is_listening = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()
        print("Voice module started!", flush=True)

    def stop(self):
        self.is_listening = False

    def _contains_trigger(self, text):
        text_lower = text.lower()
    
        # Exakte Treffer
        exact_triggers = ["hey claude", "hallo claude", "claude"]
        for trigger in exact_triggers:
            if trigger in text_lower:
                return True
    
        # Fuzzy Treffer - häufige Mishearings abfangen
        fuzzy_triggers = [
            "hey claud", "hey klaud", "hey cloud",
            "hey klaus", "hallo klaud", "hallo cloud",
            "hey glad", "hey klaude", "a claude",
            "hey claw", "he claude"
        ]
        for trigger in fuzzy_triggers:
            if trigger in text_lower:
                return True
    
        return False

    def _listen_loop(self):
        print("Listen loop started!", flush=True)
        try:
            mic = sr.Microphone(device_index=MIC_INDEX, sample_rate=SAMPLE_RATE)
            
            # Kalibrieren
            print("Kalibriere...", flush=True)
            self.recognizer.energy_threshold = 500
            self.recognizer.dynamic_energy_threshold = False
            print(f"Kalibriert! Threshold: {self.recognizer.energy_threshold}", flush=True)
            
            while self.is_listening:
                if self.is_processing:
                    time.sleep(0.1)
                    continue

                try:
                    print("Hoere zu...", flush=True)
                    # ALSA stderr unterdrücken
                    os.dup2(devnull, 2)
                    with mic as source:
                        audio = self.recognizer.listen(
                            source,
                            timeout=5,
                            phrase_time_limit=6
                        )
                    os.dup2(old_stderr, 2)

                    print("Erkenne...", flush=True)
                    text = self.recognizer.recognize_google(audio, language='de-DE')
                    print(f"Heard: {text}", flush=True)

                    if self._contains_trigger(text):
                        command = text.lower()
                        for trigger in TRIGGER_WORDS:
                            command = command.replace(trigger, "").strip()
                        print(f"TRIGGER! Command: '{command}'", flush=True)
                        self.is_processing = True
                        self.on_trigger(command)

                except sr.WaitTimeoutError:
                    print("Timeout, nochmal...", flush=True)
                except sr.UnknownValueError:
                    print("Nichts verstanden", flush=True)
                except Exception as e:
                    os.dup2(old_stderr, 2)
                    print(f"Fehler: {e}", flush=True)
                    time.sleep(1)

        except Exception as e:
            print(f"Loop Fehler: {e}", flush=True)

    def set_processing_done(self):
        self.is_processing = False
        print("Processing done, hoere wieder zu...", flush=True)
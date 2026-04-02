# -*- coding: utf-8 -*-
import speech_recognition as sr
import threading
import time
import os

devnull = os.open(os.devnull, os.O_WRONLY)
old_stderr = os.dup(2)

TRIGGER_WORDS = ["hey claude", "hallo claude", "claude", "hey claud",
                 "hey klaud", "hey cloud", "hey klaus", "hallo klaud",
                 "hey glad", "hey klaude", "a claude", "hey claw"]
MIC_INDEX = 1
SAMPLE_RATE = 48000

class VoiceModule:
    def __init__(self, on_trigger_callback, on_listening_callback=None):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 1500
        self.recognizer.dynamic_energy_threshold = False
        self.on_trigger = on_trigger_callback
        self.on_listening = on_listening_callback
        self.is_listening = False
        self.is_processing = False
        self.thread = None
        self.mic = sr.Microphone(device_index=MIC_INDEX, sample_rate=SAMPLE_RATE)

    def start(self):
        self.is_listening = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()
        print("Voice module started!", flush=True)

    def stop(self):
        self.is_listening = False

    def _contains_trigger(self, text):
        text_lower = text.lower()
        return any(t in text_lower for t in TRIGGER_WORDS)

    def _extract_command(self, text):
        command = text.lower()
        for trigger in ["hey claude", "hallo claude", "claude", "hey claud",
                        "hey klaud", "hey cloud", "hey klaus", "hallo klaud",
                        "hey glad", "hey klaude", "a claude", "hey claw"]:
            command = command.replace(trigger, "")
        return command.strip()

    def _recognize(self, timeout=4, phrase_limit=8):
        os.dup2(devnull, 2)
        try:
            with self.mic as source:
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_limit)
            os.dup2(old_stderr, 2)
            return self.recognizer.recognize_google(audio, language='de-DE')
        except Exception as e:
            os.dup2(old_stderr, 2)
            raise e

    def _listen_loop(self):
        print("Listen loop gestartet!", flush=True)
        while self.is_listening:
            if self.is_processing:
                time.sleep(0.2)
                continue
            try:
                text = self._recognize(timeout=4, phrase_limit=6)
                print(f"Heard: {text}", flush=True)

                if self._contains_trigger(text):
                    command = self._extract_command(text)
                    
                    # Wenn kein Command — nochmal kurz zuhören
                    if not command:
                        if self.on_listening:
                            self.on_listening()
                        try:
                            command = self._recognize(timeout=6, phrase_limit=10)
                            print(f"Command: {command}", flush=True)
                        except:
                            command = "Was kann ich fuer dich tun?"

                    self.is_processing = True
                    self.on_trigger(command)

            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except Exception as e:
                print(f"Fehler: {e}", flush=True)
                time.sleep(0.5)

    def set_processing_done(self):
        self.is_processing = False
        print("Wieder bereit!", flush=True)
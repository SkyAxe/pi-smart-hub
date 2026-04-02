# -*- coding: utf-8 -*-
import speech_recognition as sr
import threading
import time

TRIGGER_WORDS = ["hey claude", "hallo claude", "claude"]
MIC_INDEX = 1
SAMPLE_RATE = 48000

class VoiceModule:
    def __init__(self, on_trigger_callback):
        self.recognizer = sr.Recognizer()
        self.on_trigger = on_trigger_callback
        self.is_listening = False
        self.is_processing = False
        self.thread = None

    def start(self):
        self.is_listening = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()
        print("Voice module started, listening for trigger word...")

    def stop(self):
        self.is_listening = False

    def _contains_trigger(self, text):
        text_lower = text.lower()
        for trigger in TRIGGER_WORDS:
            if trigger in text_lower:
                return True
        return False

    def _listen_loop(self):
        mic = sr.Microphone(device_index=MIC_INDEX, sample_rate=SAMPLE_RATE)
        with mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            # Fix: energy threshold manuell setzen
            self.recognizer.energy_threshold = 500
            self.recognizer.dynamic_energy_threshold = False
            print(f"Calibrated, energy threshold: {self.recognizer.energy_threshold}")

        while self.is_listening:
            if self.is_processing:
                time.sleep(0.1)
                continue
            try:
                with mic as source:
                    audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio, language='de-DE')
                print(f"Heard: {text}")

                if self._contains_trigger(text):
                    command = text.lower()
                    for trigger in TRIGGER_WORDS:
                        command = command.replace(trigger, "").strip()
                    print(f"Trigger detected! Command: {command}")
                    self.is_processing = True
                    self.on_trigger(command)

            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except Exception as e:
                print(f"Voice error: {e}")
                time.sleep(1)

    def set_processing_done(self):
        self.is_processing = False
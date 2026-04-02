# -*- coding: utf-8 -*-
import speech_recognition as sr
import threading
import time
import os

devnull = os.open(os.devnull, os.O_WRONLY)
old_stderr = os.dup(2)

TRIGGER_WORDS = ["hey claude", "hallo claude", "claude", "hey claud",
                 "hey klaud", "hey cloud", "hey klaus", "hallo klaud",
                 "hey glad", "hey klaude", "a claude", "hey claw",
                 "hey clot", "hey klot", "hey klau"]
MIC_INDEX = 1
SAMPLE_RATE = 48000

class VoiceModule:
    def __init__(self, on_trigger_callback, on_listening_callback=None):
        self.recognizer = sr.Recognizer()
        # Niedrigerer Schwellwert = empfindlicher; dynamic=True passt sich Umgebungslärm an
        self.recognizer.energy_threshold = 400
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.dynamic_energy_adjustment_damping = 0.15
        self.recognizer.dynamic_energy_ratio = 1.5
        # Kürzere Pausen → schnelleres Reagieren nach dem letzten gesprochenen Wort
        self.recognizer.pause_threshold = 0.5
        self.recognizer.non_speaking_duration = 0.3
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
        for trigger in TRIGGER_WORDS:
            command = command.replace(trigger, "")
        return command.strip()

    def _listen_loop(self):
        print("Listen loop gestartet!", flush=True)

        with self.mic as source:
            print("Kalibriere für Umgebungsgeräusche (1.5s)...", flush=True)
            os.dup2(devnull, 2)
            self.recognizer.adjust_for_ambient_noise(source, duration=1.5)
            os.dup2(old_stderr, 2)
            print(f"Energie-Schwellwert nach Kalibrierung: {self.recognizer.energy_threshold:.0f}", flush=True)

            while self.is_listening:
                if self.is_processing:
                    time.sleep(0.1)
                    continue

                try:
                    os.dup2(devnull, 2)
                    # phrase_limit=8s: erlaubt "Hey Claude, wie wird das Wetter heute?"
                    audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=8)
                    os.dup2(old_stderr, 2)

                    text = self.recognizer.recognize_google(audio, language='de-DE')
                    print(f"Heard: {text}", flush=True)

                    if self._contains_trigger(text):
                        command = self._extract_command(text)

                        if not command:
                            # Wake-Word ohne Befehl → kurz zuhören
                            if self.on_listening:
                                self.on_listening()
                            try:
                                os.dup2(devnull, 2)
                                audio2 = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                                os.dup2(old_stderr, 2)
                                command = self.recognizer.recognize_google(audio2, language='de-DE')
                                print(f"Command: {command}", flush=True)
                            except Exception:
                                os.dup2(old_stderr, 2)
                                command = "Was kann ich für dich tun?"

                        self.is_processing = True
                        # Trigger in eigenem Thread → Mikrofon-Loop bleibt reaktionsfähig
                        threading.Thread(
                            target=self.on_trigger, args=(command,), daemon=True
                        ).start()

                except sr.WaitTimeoutError:
                    pass
                except sr.UnknownValueError:
                    pass
                except Exception as e:
                    os.dup2(old_stderr, 2)
                    print(f"Fehler: {e}", flush=True)
                    time.sleep(0.5)

    def set_processing_done(self):
        self.is_processing = False
        print("Wieder bereit!", flush=True)

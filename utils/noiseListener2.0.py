import os
import time
import random
import scipy.io.wavfile as wav
import sounddevice as sd
import tkinter as tk
import tkinter.ttk as ttk
import threading

# Параметры записи
sample_rate = 44100  # Частота дискретизации
max_duration = 480   # Максимальная длина записи в секундах
min_duration = 120   # Минимальная длина записи в секундах
output_dir = 'audio_records'  # Директория для сохранения файлов

# Создание директории для аудиозаписей, если её нет
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

class AudioRecorder:
    def __init__(self, master):
        self.master = master
        self.master.title("Audio Recorder")
        self.recording = False
        self.recording_thread = None

        self.record_button = ttk.Button(master, text="Start Recording", command=self.start_recording)
        self.record_button.pack(pady=20)

        self.stop_button = ttk.Button(master, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=20)

    def record_audio(self, duration):
        print(f"Запись аудио в течение {duration:.2f} секунд...")
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float64')
        sd.wait()  # ожидание завершения записи
        return audio

    def save_audio(self, audio, filename):
        wav.write(filename, sample_rate, audio)
        print(f"Сохранено {filename}")

    def start_recording(self):
        self.recording = True
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # Запуск записи в отдельном потоке
        self.recording_thread = threading.Thread(target=self.record_audio_loop)
        self.recording_thread.start()

    def record_audio_loop(self):
        while self.recording:
            duration = random.uniform(min_duration, max_duration)  # случайная длина записи
            audio_data = self.record_audio(duration)  # запись аудио
            filename = os.path.join(output_dir, f"recording_{time.time()}.wav")  # имя файла
            self.save_audio(audio_data, filename)  # сохранение файла
            time.sleep(1)  # небольшая пауза перед следующей записью

    def stop_recording(self):
        self.recording = False
        self.recording_thread.join()  # ждем завершения потока
        self.stop_button.config(state=tk.DISABLED)
        self.record_button.config(state=tk.NORMAL)

# MAIN
if __name__ == "__main__":
    root = tk.Tk()
    app = AudioRecorder(root)
    root.mainloop()
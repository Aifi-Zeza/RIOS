import os
import tkinter as tk
import tkinter.ttk as ttk
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import uuid  # Импортируем модуль для генерации случайных имен

class AudioRecorder:
    def __init__(self, master):
        self.master = master
        self.master.title("Audio Recorder")
        self.recording = False
        self.audio_data = []

        self.record_button = ttk.Button(master, text="Record", command=self.record)
        self.record_button.pack(pady=20)
        
        self.stop_button = ttk.Button(master, text="Stop", command=self.stop, state=tk.DISABLED)
        self.stop_button.pack(pady=20)
        
        self.save_button = ttk.Button(master, text="Save", command=self.save_audio, state=tk.DISABLED)
        self.save_button.pack(pady=20)

        # Параметр обрезания в миллисекундах
        self.cutoff_label = ttk.Label(master, text="Cutoff time (ms):")
        self.cutoff_label.pack(pady=5)
        
        self.cutoff_entry = ttk.Entry(master)
        self.cutoff_entry.insert(0, "0")  # Ввод значения по умолчанию
        self.cutoff_entry.pack(pady=20)
        


        # Папка для сохранения аудиофайлов
        self.save_directory = "audio_records"
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)

    def record(self):
        self.recording = True
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.audio_data = []  # Clear previous audio data
        self.sample_rate = 44100  # Sample rate

        self.stream = sd.InputStream(samplerate=self.sample_rate, channels=1, callback=self.callback)
        self.stream.start()

    def callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.audio_data.append(indata.copy())

    def stop(self):
        self.recording = False
        self.stream.stop()
        self.stream.close()
        self.stop_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.NORMAL)
        self.record_button.config(state=tk.NORMAL)

    def save_audio(self):
        if self.audio_data:
            audio_data = np.concatenate(self.audio_data, axis=0)
            cutoff_ms = int(self.cutoff_entry.get())
            cutoff_samples = int((cutoff_ms / 1000) * self.sample_rate)

            # Обрезаем аудио данные
            audio_data = audio_data[:cutoff_samples]  # Обрезаем данные

            # Генерируем случайное имя файла
            unique_id = uuid.uuid4()  # Генерируем уникальный идентификатор
            file_name = f"{unique_id}.wav"  # Формируем имя файла
            file_path = os.path.join(self.save_directory, file_name)  # Полный путь к файлу
            write(file_path, self.sample_rate, audio_data)
            print(f"Audio saved as {file_path}")

# MAIN
if __name__ == "__main__":
    root = tk.Tk()
    app = AudioRecorder(root)
    root.mainloop()
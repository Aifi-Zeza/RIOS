import os
from pydub import AudioSegment

def convert_wav_to_mp3(input_dir, output_dir):
    # Убедитесь, что выходная папка существует
    os.makedirs(output_dir, exist_ok=True)

    # Проходим по всем файлам в входной директории
    for filename in os.listdir(input_dir):
        if filename.endswith(".wav"):
            wav_path = os.path.join(input_dir, filename)
            mp3_path = os.path.join(output_dir, filename.replace(".wav", ".mp3"))
            
            # Конвертация
            audio = AudioSegment.from_file(wav_path, format='wav')
            audio.export(mp3_path, format='mp3')
            print(f"Converted {filename} to {os.path.basename(mp3_path)}")

# Пример использования
input_directory = "audio_records"
output_directory = "audio_records_mp3"
convert_wav_to_mp3(input_directory, output_directory)
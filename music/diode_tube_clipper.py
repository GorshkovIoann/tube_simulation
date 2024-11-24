import numpy as np
import math
import scipy.io.wavfile as wavfile

# Чтение аудиофайла
def read_audio(file_path):
    sampling_rate, data = wavfile.read(file_path)
    # Если стерео, преобразуем в моно
    if len(data.shape) > 1:
        data = np.mean(data, axis=1).astype(data.dtype)
    return sampling_rate, data

# Обработка сигнала диодом (нелинейное обрезание)
def process_with_diode(signal, threshold=0.5):
    # Нормализуем сигнал в диапазон [-1, 1]
    max_val = np.max(np.abs(signal))
    normalized_signal = signal / max_val
    
    # Применяем обрезание
    processed_signal = np.tan(normalized_signal)
    
    # Возвращаем к исходному диапазону
    return processed_signal * max_val

# Сохранение обработанного аудиофайла
def save_audio(file_path, sampling_rate, data):
    wavfile.write(file_path, sampling_rate, data.astype(np.int16))

# Пример использования
try:
    # Загрузка файла
    sampling_rate, audio_data = read_audio("input.wav")
    
    # Обработка сигнала
    processed_audio = process_with_diode(audio_data, threshold=0.7)
    
    # Сохранение результата
    save_audio("output.wav", sampling_rate, processed_audio)
    print("Обработанный файл сохранён как 'output.wav'")
except FileNotFoundError:
    print("Пожалуйста, загрузите файл 'input.wav' в текущую папку.")
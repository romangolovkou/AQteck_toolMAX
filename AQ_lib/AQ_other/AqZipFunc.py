import os
import zipfile


def extract_zip_with_cyrillic(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            # Декодируем имя файла с использованием кодировки cp437 и затем перекодируем в utf-8
            filename = file_info.filename.encode('cp437').decode('cp866')
            file_path = os.path.join(extract_to, filename)

            # Создаем директории, если их еще нет
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Извлекаем каждый файл
            with open(file_path, 'wb') as file:
                file.write(zip_ref.read(file_info.filename))


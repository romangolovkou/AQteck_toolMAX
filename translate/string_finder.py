import os
import re

def find_patterns_in_py_files(directory, pattern):
    matching_parts = []

    # Рекурсивно обходим все файлы в указанной директории
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):  # Проверяем, что файл имеет расширение .py
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for line in lines:
                        matches = re.findall(pattern, line)  # Ищем все совпадения шаблона в строке
                        for match in matches:
                            matching_parts.append(match)

    return matching_parts

def save_matching_parts_to_file(matching_parts, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for part in matching_parts:
            f.write(f"{part}\n")

# Указываем директорию, в которой нужно искать файлы
directory = "../AQ_lib"
# Указываем шаблон строки
pattern = r'AqTranslateManager\.tr\((?:"|\')([^"\']+)'

print('Start script')

try:
    # Вызываем функцию для поиска совпадений
    matching_parts = find_patterns_in_py_files(directory, pattern)
    print('matches OK')

    # Указываем имя файла для сохранения результатов
    output_file = "Custom context strings.txt"

    # Вызываем функцию для сохранения результатов в файл
    save_matching_parts_to_file(matching_parts, output_file)
    print('File create OK')
except Exception as e:
    print('Error')
    print(e)

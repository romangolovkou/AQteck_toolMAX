def check_custom_context_ts_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # Прочитать содержимое файла
            content = file.read()
            # Проверить наличие строки в содержимом файла
            if '<name>Custom context</name>' in content:
                print("Строка <name>Custom context</name> найдена в файле.")
                return True
            else:
                print("Строка <name>Custom context</name> не найдена в файле.")
                return False
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")


def create_custom_context(_txt_filename, _ts_filename):
# странное расположение строк в этой функции не трогать!!!!
# меняются отступы в итоговом файле!!!
    try:
        # Открываем файл txt для чтения
        with open(_txt_filename, 'r', encoding='utf-8') as txt_file:
            # Читаем строки из файла txt
            lines = txt_file.readlines()

            # Создаем XML-структуру
            custom_ts_content = f'''<context>
    <name>Custom context</name>
'''
            for line in lines:
                # Удаляем лишние пробелы и переносы строки
                line = line.strip()
                # Добавляем каждую строку в XML-структуру
                custom_ts_content += f'''    <message>
        <source>{line}</source>
        <translation type="unfinished"></translation>
    </message>
'''
            custom_ts_content += '</context>'
# странное расположение строк в этой функции не трогать!!!!
# меняются отступы в итоговом файле!!!

        insert_string_into_ts_file(custom_ts_content, _ts_filename)

        # # Записываем XML-структуру в файл
        # with open(xml_filename, 'w', encoding='utf-8') as xml_file:
        #     xml_file.write(custom_ts_content)
        #
        # print(f'XML-файл успешно создан: {xml_filename}')

    except FileNotFoundError:
        print(f"Файл {txt_filename} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def insert_string_into_ts_file(string_to_insert, _ts_filename):
    try:
        # Открываем файл .ts для чтения
        with open(_ts_filename, 'r', encoding='utf-8') as ts_file:
            # Читаем все строки из файла .ts
            lines = ts_file.readlines()

        # Вставляем строку перед последней строкой
        lines.insert(-1, string_to_insert + '\n')

        # Записываем обновленное содержимое в файл .ts
        with open(_ts_filename, 'w', encoding='utf-8') as ts_file:
            ts_file.writelines(lines)

        print(f'Строка успешно вставлена в файл {_ts_filename}')

    except FileNotFoundError:
        print(f"Файл {ts_filename} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")



# Укажите путь к файлу .ts, который вы хотите проверить
ts_filename = "source_ua.ts"

# Проверка наличия блока Custom context в файле
custom_cont = check_custom_context_ts_file(ts_filename)

if custom_cont:
    pass
else:
    # Укажите путь к файлу .txt с вашими строками
    txt_filename = "Custom context strings.txt"
    # Укажите путь, по которому нужно сохранить XML-файл
    test_filename = "creator_test.txt"
    create_custom_context(txt_filename, ts_filename)

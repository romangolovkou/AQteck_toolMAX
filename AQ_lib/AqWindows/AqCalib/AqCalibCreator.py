import json
import os
import re


class AqCalibCreator(object):

    @classmethod
    def init(cls, _event_manager):
        cls.event_manager = _event_manager

    # @classmethod
    # def create_calibrator(cls, param_dict):

    @classmethod
    def prepare_json_file(cls, input_file, output_file):
        try:
            # Открытие оригинального файла с указанием кодировки
            with open(input_file, 'r', encoding='utf-8') as file:
                content = file.read()

            # Регулярное выражение для поиска комментариев: // и /* */
            # Убирает как однострочные, так и многострочные комментарии
            content_without_comments = re.sub(r'//.*|/\*[\s\S]*?\*/', '', content)

            # Попробуем загрузить данные, чтобы убедиться, что формат валиден
            data = json.loads(content_without_comments)

            # Сохранение обработанного JSON без комментариев
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            print(f"Файл успешно обработан и сохранен как {output_file}")

        except json.JSONDecodeError as e:
            print(f"Ошибка при разборе JSON: {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    @classmethod
    def load_json(cls, jsonFile_path):
        if os.path.isfile(jsonFile_path):
            jsonFile = os.path.abspath(os.path.join(os.getcwd(), jsonFile_path))
            jsonFile = open(jsonFile, encoding='utf-8')
            # Read file
            data = json.load(jsonFile)
            return data

        else:
            raise Exception("Error loading your JSON files : '" + str(jsonFile_path) + "' does not exist")

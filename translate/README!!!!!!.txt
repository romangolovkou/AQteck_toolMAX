Локалізація конфігуратору відбувається з використанням QtLinguist. 
Файли .ui створені у QtCreator огортають строки що повинні перекладатися у QCoreApplication.translate(*тут строка для перекладу*)
Усі строки для перекладу що не створюються у QtCreator повинні бути огорнуті AqTranslateManager.tr(*тут строка для перекладу*) з 
кастомного AqTranslateManager у проекті.

Для створення локалізаціі потрібно виконати декілька шагів:

1. Підготовка файлів до перекладу.

1.1створення файлу ts для його подальшого перекладу у QtLinguist відбувається викликом у терміналі команди:

	lupdate *шлях до директорії з файлами .ui* -recursive -ts *шлях до директорії з перекладами*\*назва_майбутьного файлу*.ts

	або викликати бат файл lupdate.bat попередньо змінив шляхи до директорій.
	call E:\git_new\venv\Lib\site-packages\PySide6\lupdate E:\git_new\AQteck_toolMAX\UI -recursive -ts .E:\git_new\AQteck_toolMAX\translate\source_ua.ts

1.2 Потім потрібно запустити пайтон-скрипт string_finder.py (попередньо виправивши шляхи до файлів та директорій), цей скрипт шукає строки для перекладу
	шаблоном AqTranslateManager.tr(*тут строка для перекладу*) та збрає їх у файл Custom context strings.txt

1.3 Потім потрібно запустити пайтон-скрипт modify_ts.py він створює у ts файлі розділ Custom context зі строками з файлу Custom context strings.txt
	або додає нові строки у вже існуючий розділ Custom context.  (Якщо скрипт modify_ts.py запускаеться вперше, то він створює в кінці
	ts файлу блок Custom context та заповнює його строками, якщо розділ Custom context вже існує, то скрипт додасть до розділу тільки нові строки яких
	досі не має у розділі. Повторні запуски необхідні при додаванні нових строк та єлементів інтерфейсу що повинні 
	перекладатися. Таким чином скрипт залишає раніше додані строки що вже мають переклад у ts файлі, та додає нові з маркером translation type="unfinished".)

2. Переклад
	Далі Файл ts відкриваємо у QtLinguist та створюємо переклади. Усі строки що були створені поза файлами .ui та огорнуті AqTranslateManager.tr(*тут строка для перекладу*)
	будуть розташовані в розділі Custom context. Зберігаємо зміни.

3. Створення файлу перекладів .qm
	Для створення файлу .qm потрібно викликати команду у теміналі
	lrelease *шлях до файлу ts* -qm *шлях до директорії з перекладами*\*назва_майбутьного файлу*.qm

	або викликати бат файл lrelease.bat попередньо змінив шляхи до файлів.
	call E:\git_new\venv\Lib\site-packages\PySide6\lrelease E:\git_new\AQteck_toolMAX\translate\source_ua.ts -qm E:\git_new\AQteck_toolMAX\translate\ua.qm

	Файл повинен мати назву співпадаючу з скороченням мови що використовується у коді конфігуратору. 
	приклад:
	- у коді 'UA' = назва файлу ua.qm 
	- у коді 'FR' = назва файлу fr.qm 
	- у коді 'DE' = назва файлу de.qm 
	

Для того щоб строки з розділу Custom context перекладалися на ходу без необхідності перезавантаження додатку
для них у їх об'ектах потрібно реалізувати функцію retranslate, та підписати цю функцію до AqTranslateManager
через метод subscribe. Тоді метод retranslate буде викликатися під час події зміни мови додатку "на ходу"
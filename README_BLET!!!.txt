Опасные места:
1. В библиотеке pymodbus, есть недоработки в функции read_file_record и классе ReadFileRecordRequest.
   Там остутствует агрумент slave_id и по этому в запросе всегда ставится 0. В исходниках бибки есть 
   файлы file_message.py и mixin.py. В них были внесены правки. 
	
	В mixin.py в функцию чтения файла добавлен агрумент slave_id:

	def read_file_record(self, slave_id, records: List[Tuple], **kwargs: Any) -> ModbusResponse:
        	"""Read file record (code 0x14).

        	:param records: List of (Reference type, File number, Record Number, Record Length)
        	:param kwargs: (optional) Experimental parameters.
        	:raises ModbusException:
        	"""
        	return self.execute(pdu_file_msg.ReadFileRecordRequest(slave_id, records, **kwargs)) 
	
	В file_message.py в class ReadFileRecordRequest добавлен агрумент slave_id:
	
		def __init__(self, slave_id, records=None, **kwargs):
        		"""Initialize a new instance.

        		:param records: The file record requests to be read
        		"""
        		ModbusRequest.__init__(self, slave_id, **kwargs)
        		self.records = records or []

2. (пункт нужно дополнить) В качестве IV для DES расшифровки используется 'superkey', а для ключа 
   используется хеш пароля прибора
   (функция hash8 в исходниках контейнерной) или значение EMPTY_HASH равное 0x23B246FCA76F5524 
   (в исходниках контейнерной используется свапнутая версия 0x24556FA7FC46B223).

3. В регситрах модбас байты поменяны местами. по этому для работы с вычитанными данными в проекте
   все проебразовуется функцией def swap_modbus_bytes(data, num_pairs). работает как с массивом байт
   так и со строками и байтовыми строками (до конца не тестировалась).
   
4. У парсінгу дескриптора пропущено обробку модификатора M0x0C (хз як розбирати і який його розмір, оскільки в проектах 
   його використання не виявлено - ігноримо) 
5. Є питання що до відображення дефолтних значень для enum, у індус-конфігураторі у деяких відображаеється
   у деяких ні (хоча саме дефолтне значення наявне і там і там), чому так і за якою ознакою - хз. 
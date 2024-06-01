from transliterate import translit
from os.path import exists
from os import mkdir
import csv


from files import Files
from additions import FileType

class Export():
    def __init__(self):
        self._io_disc_headers = [':IODisc','Group', 'Comment', 'Logged', 'EventLogged',
                        'EventLoggingPriority', 'RetentiveValue', 'InitialDisc',
                        'OffMsg', 'OnMsg', 'AlarmState', 'AlarmPri', 'DConversion','AccessName',
                        'ItemUseTagname', 'ItemName', 'ReadOnly', 'AlarmComment',
                        'AlarmAckModel', 'DSCAlarmDisable', 'DSCAlarminhibitor', 'SymbolicName'
                        ]
        self._io_real_headers = [':IOReal', 'Group', 'Comment', 'Logged', 'EventLogged',
                        'EventLoggingPriority', 'RetentiveValue', 'RetentiveAlarmParameters',
                        'AlarmValueDeadband', 'AlarmDevDeadband', 'EngUnits', 'InitialValue',
                        'MinEU', 'MaxEU', 'Deadband', 'LogDeadband', 'LoLoAlarmState',
                        'LoLoAlarmValue', 'LoLoAlarmPri', 'LoAlarmState', 'LoAlarmValue',
                        'LoAlarmPri', 'HiAlarmState', 'HiAlarmValue', 'HiAlarmPri',
                        'HiHiAlarmState', 'HiHiAlarmValue', 'HiHiAlarmPri',
                        'MinorDevAlarmState', 'MinorDevAlarmValue', 'MinorDevAlarmPri',
                        'MajorDevAlarmState', 'MajorDevAlarmValue', 'MajorDevAlarmPri',
                        'DevTarget', 'ROCAlarmState', 'ROCAlarmValue', 'ROCAlarmPri',
                        'ROCTimeBase', 'MinRaw', 'MaxRaw', 'Conversion', 'AccessName',
                        'ItemUseTagname', 'ItemName', 'ReadOnly', 'AlarmComment',
                        'AlarmAckModel', 'LoLoAlarmDisable', 'LoAlarmDisable', 'HiAlarmDisable',
                        'HiHiAlarmDisable', 'MinDevAlarmDisable', 'MajDevAlarmDisable', 'RocAlarmDisable',
                        'LoLoAlarmInhibitor', 'LoAlarmInhibitor', 'HiAlarmInhibitor', 'HiHiAlarmInhibitor',
                        'MinDevAlarmInhibitor', 'MajDevAlarmInhibitor','RocAlarmInhibitor',
                        'SymbolicName']
        self._opc_headers = ['Tag Name', 'Address', 'Data Type', 'Respect Data Type', 'Client Access', 'Scan Rate', 'Scaling',
                   'Raw Low', 'Raw High', 'Scaled Low', 'Scaled High', 'Scaled Data Type', 'Clamp Low', 'Clamp High',
                   'Eng Units', 'Description', 'Negate Value']
        if not exists('results'):
            mkdir('results')
    @property
    def io_disk_headers(self):
        return self._io_disc_headers
    
    @property
    def io_real_headers(self):
        return self._io_real_headers
    
    @property
    def opc_headers(self):
        return self._opc_headers
    
    def _get_onoff_message(desc:str)->tuple:
        res = tuple()
        alarm = ['авар' in desc.lower(), 'hi' in desc.lower(), 'lo' in desc.lower(), 'перегруз' in desc.lower()]
        control = ['включить' in desc.lower(), 'выключить' in desc.lower()]
        state = ['включен' in desc.lower()]
        if 'АУ' in desc:
            res = ('не автомат', 'автомат')
        elif any(state):
            res = ('не в работе', 'в работе')
        elif any(alarm):
            res = ('нет аварии','авария')
        elif any(control):
            res = (' ', 'cработка')
        else:
            res = ('сигнала нет', 'сигнал есть')       
        return res
    
    def export_to_kep(self, data:list, file_name:str=None):
        """Экспортируем данные из таблицы в  KEP Server
        Args:
            data (list): Список с кортежами данных из строк таблицы
            file_name (str, optional): Имя файла, если None ,будет
            сгенерировано само. Defaults to None.
        """
        _file_name = file_name if file_name is not None else Files.create_file_name(FileType.KEP)
        with open(f"results/{_file_name}", mode='w', encoding='cp1251' ) as fp:
            writer = csv.writer(fp, delimiter=';')
            _hd = True
            if _hd:
                writer.writerow(self.opc_headers)
                _hd = False                
            for row in data:
                res_row = [None for _ in range(len(self.opc_headers))]
                res_row[0] = f'{row[1]}{row[0]}' # Имя тега с постфиксом
                res_row[1] = row[2]              #  Адрес с командой    
                res_row[2] = row[5].lower()      # Формат данных
                res_row[3] = 1                   # Respect Data Type
                res_row[4] = 'R/W' if row[9] else 'RO' # Режим доступа
                res_row[5] = 100                 # Scan Rate не меняем. Не нужно
                res_row[15] = translit(row[3], 'ru', reversed=True) #Description
                writer.writerow(res_row)

    def export_to_intouch(self):
        pass

    def export_to_weintek(self):
        pass
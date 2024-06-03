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
    def io_disc_headers(self):
        return self._io_disc_headers
    
    @property
    def io_real_headers(self):
        return self._io_real_headers
    
    @property
    def opc_headers(self):
        return self._opc_headers
    
    def _get_onoff_message(self, desc:str)->tuple:
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

    def export_to_intouch(self, data:list, file_name:str=None):
        """Экспортируем данные из таблицы в базу Intouch

        Args:
            data (list): Список с кортежами из строк таблицы
            file_name (str, optional): Имя файла для экспорта. Если пустое, 
            будет сгенерировано самостоятельно
        """
        _file_name = file_name if file_name is not None else Files.create_file_name(FileType.INTOUCH)
        with open(f"results/{_file_name}", mode='w', encoding='cp1251') as fp:
            writer = csv.writer(fp, delimiter=';')
            # Сначала пишем только дискреты
            writer.writerow(self.io_disc_headers)
            for row in iter(data):
                if row[5] == 'Boolean':
                    res_row = [None for _ in range(len(self.io_disc_headers))]
                    res_row[0] = f'{row[1]}{row[0]}'    #IODisc имя тега
                    res_row[1] = row[0][1:].upper()     #Group upper для постффикса тега без символа _
                    res_row[2] = row[3]                 #Описание тега
                    res_row[3] = 'No'                   #Logged логирование значения в системе
                    res_row[4] = 'Yes'                  #EventLogged логирование событий тега (алармов и т.д.)
                    res_row[5] = 999                    #EventLoggingPriority
                    res_row[6] = 'No'                   #RetentiveValue
                    res_row[7] = 'Off'                  #InitialDIsc начальное значение по умолчанию
                    res_row[8],
                    res_row[9] = self._get_onoff_message(row[3]) #OffMsg, OnMsg
                    res_row[10] = 'None'                #AlarmState
                    res_row[11] = 220                   #AlarmPri почему именно 220? Хер его знает..
                    res_row[12] = 'Direct'              #DConversion преобразование сигнала
                    #TODO доработать возможность добавления AccessName для тего в Intouch
                    res_row[13] = 'K4_PCU'              #AccessName
                    res_row[14] = 'Yes'                 #ItemUseTagName
                    res_row[15] = res_row[0]            #ItemName
                    res_row[16] = 'No' if row[9] else 'Yes'  #ReadOnly
                    res_row[17] = res_row[0]            #AlarmComment
                    res_row[18] = 0                     #AlarkAckModel
                    res_row[19] = 0                     #DSCAlarmDisable                
                    writer.writerow(res_row)
            writer.writerow(self.io_real_headers)
            for row in iter(data):
                if row[5] in ['Float']:
                    res_row = [None for _ in range(len(self.io_real_headers))]
                    writer.writerow(res_row)  
                    res_row[0] = f'{row[1]}{row[0]}'    #IOReal имя тега
                    res_row[1] = row[0][1:].upper()   #Group upper для постффикса тега без символа _                                     
                    res_row[2] = row[3]                 #Описание тега
                    res_row[3] = 'No'                   #Logged логирование значения в системе
                    res_row[4] = 'No'                   #EventLogged логирование событий тега (алармов и т.д.)
                    res_row[5] = 0                      #EventLoggingPriority
                    res_row[6] = 'No'                   #RetentiveValue
                    res_row[7] = 'No'                   #RetentiveAlarmParameters 
                    res_row[8] = 0                      #AlarmValueDeadband Зона нечувствительности 
                    res_row[9] = 0                      #AlarmDevDeadband
                    res_row[10] = row[6]                #EngUnits  Единицы измерения
                    res_row[11] = 0                     #InitialValue начальное значение
                    res_row[12] = row[8]                #MinEU минимальное значение измерения
                    res_row[13] = row[7]                #MaxEU максимально измераемое значение
                    res_row[14] = 0                     #Deadband зона нечувствительности 
                    res_row[15] = 0                     #LogDeadeband
                    # Следующий блок параметров для включения LO LOLO HI HIHI значений
                    # на данный момент ставится в режим выключено, все значения по нулям
                    # в последствии этим блоком можно будет управлять
                    #TODO Реализовать управление порогами
                    res_row[16] = 'Off'                 #LoLoAlarmState
                    res_row[17] = 0                     #LoLoAlarmValue
                    res_row[18] = 1                     #LoLoAlarmPri  
                    res_row[19] = 'Off'                 #LoAlarmState
                    res_row[20] = 0                     #LoAlarmValue
                    res_row[21] = 1                     #LoAlarmPri
                    res_row[22] = 'Off'                 #HiAlarmState
                    res_row[23] = 0                     #HiAlarmValue
                    res_row[24] = 1                     #HiAlarmPri  
                    res_row[25] = 'Off'                 #HiHiAlarmState
                    res_row[26] = 0                     #HiHiAlarmValue
                    res_row[27] = 1                     #HiHiAlarmPri  
                    res_row[28] = 'Off'                 #MinorAlarmState
                    res_row[29] = 0                     #MinorAlarmValue
                    res_row[30] = 1                     #MinorAlarmPri  
                    res_row[31] = 'Off'                 #MajorAlarmState
                    res_row[32] = 0                     #MajorAlarmValue
                    res_row[33] = 1                     #MajorAlarmPri  
                    res_row[34] = 0                     #DevTarget
                    res_row[35] = 'Off'                 #ROCAlarmState
                    res_row[36] = 0                     #ROCAlarmValue
                    res_row[37] = 1                     #ROCAlarmPri
                    res_row[38] = 'Min'                 #ROCTimeBase
                    res_row[39] = row[8]                #MinRaw
                    res_row[40] = row[7]                #MaxRaw
                    res_row[41] = 'Linear'              #Conversion
                    res_row[42] = 'K4_PCU1'             #AccessName
                    res_row[43] = 'Yes'                 #ItemUseTagName
                    res_row[44] = res_row[0]            #ItemName
                    res_row[45] ='No' if row[9] else 'Yes' #ReadOnly
                    res_row[46] = res_row[0]            #AlarmComment
                    res_row[47] = 0                     #AlarmAckModel
                    res_row[48] = 0                     #LoLoAlarmDisable                                 
                    res_row[49] = 0                     #LoAlarmDisable                                 
                    res_row[50] = 0                     #HiAlarmDisable                                 
                    res_row[51] = 0                     #HiHiAlarmDisable
                    res_row[52] = 0                     #MinDevAlarmDisable                                      
                    res_row[53] = 0                     #MajDevAlarmDisable                                      
                    res_row[54] = 0                     #RocDevAlarmDisable                

    def export_to_weintek(self):
        pass
from transliterate import translit

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
    @property
    def io_disk_headers(self):
        return self._io_disc_headers
    
    @property
    def io_real_headers(self):
        return self._io_real_headers
    
    @property
    def opc_headers(self):
        return self._opc_headers
    

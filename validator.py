from typing import Union
from re import fullmatch

class Validator:
    def __init__(self):
        self._inputs: list


    @property
    def inputs(self)-> list:
        return self._inputs
    
    @inputs.setter
    def inputs(self, value:list) -> None:
        self._inputs = value
    

    def inputs_test(self) -> Union[list, bool]:
        res_list = []
        
        def postfix_check(value) -> str:
            return '' if fullmatch(r'\w{0,10}',value) is not None else 'Постфикс должен быть меньше 10 символов'
        
        def tagname_check(value) -> str:
            return '' if fullmatch(r'\w{0,20}', value) is not None  else 'В имени тега должны быть только буквы,  цифры и подчеркивания, не больше 20 символов'
        
        def address_check(value) -> str:
            """ Проверяем рег. выражением формат ввода должен быть вида 012453 или 012345.02
                если проверка не прошла возбуждаем исключение"""
            try:
                if fullmatch(r'(\d{6}\.\d{2})|\d{6}',  value) is None:
                    raise ValueError
                elif '.' in value:
                    lst_ = list(map(int, value.split('.')))
                    if lst_ not in range(1, 65536) or lst_ not in range(0, 16):
                        raise ValueError
                return ''
            except ValueError:
                 return 'В адресе могут быть только  числo [1..63535] и десятичная часть [1..15]'    
        
        def description_check(value) -> str:
            return '' if len(value) < 40 else 'Длина комментария меньше 40 символов'
            
        res_list = [postfix_check(self.inputs[0].value),
                    tagname_check(self.inputs[1].value),
                    address_check(self.inputs[2].value),
                    description_check(self.inputs[3].value),
                    ]
        return res_list if (any([len(i) for i in res_list])) else True
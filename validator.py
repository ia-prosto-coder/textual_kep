from typing import Union
from textual.widgets import Select
from re import fullmatch

class Validator:
    def __init__(self, inputs=[]):
        self._inputs = inputs
        
    


    @property
    def inputs(self)-> list:
        return self._inputs
    
    @inputs.setter
    def inputs(self, value:list) -> None:
        self._inputs = value
    

    def inputs_test(self, inputs) -> Union[list, bool]:
        self.inputs = inputs
        # TODO  Реализовать контроль первой цифры адреса(корректной команды MODBUS)
        res_list = []
        
        def postfix_check(value) -> str:
            return '' if fullmatch(r'\_\w{1,10}',value) is not None else 'Постфикс должен быть длиной от 1 до 10 символов и начинаться с _'
        
        def tagname_check(value) -> str:
            return '' if fullmatch(r'\w{1,20}', value) is not None  else 'В имени тега должны быть только буквы,  цифры и подчеркивания, от 1 до 20 символов'
        
        def address_check(value) -> str:
            """ Проверяем рег. выражением формат ввода должен быть вида 012453 или 012345.02
                если проверка не прошла возбуждаем исключение"""
            try:
                if fullmatch(r'\d{6}\.?(\d{2})?',  value) is None:
                    raise ValueError
                elif '.' in value:
                    lst_ = list(map(int, value.split('.')))
                    if lst_ not in range(1, 65536) or lst_ not in range(0, 16):
                        raise ValueError
                return ''
            except ValueError:
                 return 'В адресе могут быть только  числo [1..63535] и десятичная часть [1..15]'    
        
        def description_check(value) -> str:
            return '' if len(value) < 50 else 'Длина комментария не больше 50 символов'
        
        def select_check(select: Select) -> str:
            if select.value == Select.BLANK:
                return ['Номер функции не может быть пустым', 'Нужно выбрать единицу измерения'][1 if select.id == 'unit' else False]
            else:
                return ''
            
        def max_min_value_check(value, id) -> str:
            # Проверка цифрового значения должно быть целое или с плавающей точкой
            return '' if fullmatch(r'\-?\d+\.?(\d+)?', value) is not None else f'Для поля {id} допускается целое или вещественное число'
            
        res_list = [postfix_check(self.inputs[0].value),
                    tagname_check(self.inputs[1].value),
                    address_check(self.inputs[2].value),
                    description_check(self.inputs[3].value),
<<<<<<< HEAD
                    
=======
                    # Проверяем на пустое значение селекты-комбобоксы
                    select_check(self.inputs[4]),
                    select_check(self.inputs[5]),
                    # Проверка ввода числовых значений
                    max_min_value_check(self.inputs[6].value, self.inputs[6].id),
                    max_min_value_check(self.inputs[7].value, self.inputs[7].id)
>>>>>>> bd490388f49d3dac8ef578b0a4a56358443d357b
                    ]
        #  Возвращаем список косяков или True если все проверки пройдены
        return list(filter(lambda i:len(i), res_list)) if (any([len(i) for i in res_list])) else True
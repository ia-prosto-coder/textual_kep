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
            try:
                float(value)
                return ''
            except ValueError:
                 return 'В адресе могут быть только числа и одна десятичная точка'    
        

        res_list = [postfix_check(self.inputs[0].value),
                    tagname_check(self.inputs[1].value),
                    address_check(self.inputs[2].value)]
        return res_list if (any([len(i) for i in res_list])) else True
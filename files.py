
from os.path import exists
from os import mkdir
from textual.widgets import Static, Input, Button, DirectoryTree, Label
from textual.layouts import vertical, horizontal
import pickle as pkl
from datetime import datetime as dt
from additions import ExportType as et

class Files:
    def __init__(self, file_mode=et.RESULT):
        self._prefix = file_mode.name.lower()
        self._file_name = f"{self._prefix}_{dt.now().strftime('%Y%m%d_%H%')}"
        self._file_type = et.INTOUCH
        
        
    @property
    def file_name(self) -> str:
        return self._file_name

    @file_name.setter
    def file_name(self, value:str) -> None:
        if not len(value):
            self._file_name = f"{self._prefix}_{dt.now().strftime('%Y%m%d')}"
        else:    
            self._file_name = value

    @property
    def file_type(self) -> et:
        return self._file_type

    @file_type.setter
    def file_type(self, value:et):
        self._file_type = value

    def save_to_file(self, data) -> bool:
        """Сериализуем данные в файл
        Args:
            data (_type_): Данные для сохранения
        Returns:
            bool: В случае успешной записи возвращает True иначе False
        """
        try:
            if not exists('results'):
                mkdir('results')
            with open(f'results/{self.file_name}', mode='wb') as fp: 
                pkl.dump(data, fp)
                return None
        except Exception as e:
            return e
    
    def load_from_file(self, file_name=None):
        """Десериализация промежуточного результата
        Args:
            file_name (_type_, optional): Имя файла, если None, будет сгенерирован. Defaults to None.
        Returns:
            Any: если успешно, то вернет десериализованый объект иначе None
        """
        if file_name is not None:
            self.file_name = file_name
        try:
            with open(f"results/{self._file_name}", mode='rb') as fp:
                _data = pkl.load(fp)
            return _data
        except FileNotFoundError:
            return None    
    


        


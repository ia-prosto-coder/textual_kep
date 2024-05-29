
from os.path import exists
from os import mkdir
import pickle as pkl
from datetime import datetime as dt
from additions import FileType

class Files:
    @staticmethod
    def create_file_name(ft:FileType) -> str:
        _t = 'RESULT' if ft in [FileType.SAVE, FileType.LOAD] else ft.name
        return f"{_t}_{dt.now().strftime('%Y%m%d_%H:%M')}"

    def __init__(self, ft:FileType = FileType.SAVE):
        self._file_type = ft
        # _t = 'RESULT' if self._file_type in [FileType.SAVE, FileType.LOAD] else self._file_type.name
        # self._file_name = f"{_t}_{dt.now().strftime('%Y%m%d_%H:%M')}"
        self.file_name = Files.create_file_name(self._file_type)
    @property
    def file_name(self) -> str:
        return self._file_name

    @file_name.setter
    def file_name(self, value:str) -> None:
        if not len(value):
            _t = 'RESULT' if self._file_type in [FileType.SAVE, FileType.LOAD] else self._file_type.name
            self._file_name = f"{_t}_{dt.now().strftime('%Y%m%d_%H:%M')}"
        else:    
            self._file_name = value
        
    def save_to_file(self, data, file_name=None) -> bool:
        """Сериализуем данные в файл
        Args:
            data (_type_): Данные для сохранения
        Returns:
            bool: В случае успешной записи возвращает True иначе False
        """
        self.file_name = self.file_name if file_name is None else file_name
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
        self.file_name = self.file_name if file_name is None else file_name
        try:
            with open(f"results/{self._file_name}", mode='rb') as fp:
                _data = pkl.load(fp)
            return _data
        except Exception as e:
            return e

    def save_to_kep(self, file_name=None):
        self.file_name = self.file_name if file_name is None else file_name
         

    

    

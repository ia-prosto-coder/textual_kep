from textual.app import ComposeResult
from textual.widgets import Static, Input, Button, DirectoryTree, Label
from textual.layouts import vertical, horizontal
<<<<<<< HEAD
=======
import pickle as pkl
from datetime import datetime as dt
>>>>>>> 65dd6cc (zero level)

class Files:
    def __init__(self, f_name = 'file_name.io'):
        self._file_name: str
        
    @property
    def file_name(self) -> str:
        return self._file_name

    @file_name.setter
    def file_name(self, value:str) -> None:
        self._file_name = value
        
<<<<<<< HEAD
    def save_to_file(self, data):
        pass
    
    def load_from_file(self):
        _data = []
        return _data

class FileSaveDialog(Static):

    def compose(self):
        with vertical:
            yield Label("Path to save file")
            with horizontal: 
                yield Input(placeholder="Введите имя файла для сохранения")
                yield Button(id='select_dir_button', label='Каталог', classes='buttons')
            yield DirectoryTree()
=======
    def save_to_file(self, data) -> bool:
        """Сериализуем данные в файл
        Args:
            data (_type_): Данные для сохранения
        Returns:
            bool: В случае успешной записи возвращает True иначе False
        """
        if self.file_name in None or not len(self.file_name):
            try:
                pkl.dump(data, open(f"result_{dt.now().strftime('%d%m%Y')}", 'w'))
                return True
            except:
                return False
    
    def load_from_file(self, file_name=None):
        """Десериализация промежуточного результата
        Args:
            file_name (_type_, optional): Имя файла, если None, будет сгенерирован. Defaults to None.
        Returns:
            Any: если успешно, то вернет десериалихованый объект6 иначе None
        """
        if file_name is not None:
            self.file_name = file_name
        elif self.file_name is None or not len(self.file_name):
            self.file_name = f"result_{dt.now().strftime('%d%m%Y')}" 
        try:
            _data = pkl.load(open(self.file_name))
            return _data
        except FileNotFoundError:
            return None    
    

class FileSaveDialog(Static):
    def compose(self):
        with vertical:
            yield Label(id='path_label')
            with horizontal: 
                yield Input(placeholder="Введите имя файла для сохранения")
                yield Button(id='select_dir_button', label='Каталог', classes='buttons')
            yield DirectoryTree(path='~/', id='file_dialog')
>>>>>>> 65dd6cc (zero level)

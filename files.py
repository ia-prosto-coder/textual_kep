from textual.app import ComposeResult
from textual.widgets import Static, Input, Button, DirectoryTree, Label
from textual.layouts import vertical, horizontal

class Files:
    def __init__(self, f_name = 'file_name.io'):
        self._file_name: str
        
    @property
    def file_name(self) -> str:
        return self._file_name

    @file_name.setter
    def file_name(self, value:str) -> None:
        self._file_name = value
        
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
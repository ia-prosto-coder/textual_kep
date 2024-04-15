from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Input, DataTable, Button, RichLog
from textual.scroll_view import ScrollView
from textual.containers import ScrollableContainer, Container
from textual import on

from files import Files

NIGHT = True
class TextualKepApp(App):
    def __init__(self):
        super().__init__()
        self.inputs = [Input(id='postfix_button', placeholder='Постфикс тега'),
                Input(id='tag_name', classes='inputs', placeholder='Имя тега'),
                Input(id='address', classes='inputs', placeholder='Адрес регистра',),
                Input(id='description', classes='inputs', placeholder='Описание'),
                Input(id='command', classes='inputs', placeholder='Номер функции'),
                Input(id='unit', classes='inputs', placeholder='Ед. измерения'),
                Input(id='eu_max', classes='inputs', placeholder='Макс. значение'),
                Input(id='eu_min', classes='inputs', placeholder='Мин. значение'),
                ]
        self.sorts = set()
    

    CSS_PATH = 'main.tcss'
    BINDINGS = [
                ('L', 'load_file', 'Загрузить'),
                ('S', 'save_file', 'Сохранить'),
                ('C', 'copy_row', 'Дублировать'),
                ('T', 'swap_theme', 'Сменить тему'),
                ('Q', 'quit_app', 'Завершить приложение')
        ]
    
    def compose(self):
        yield Header()
        with Container(id='main_box'):
            with ScrollableContainer(id='left_box', classes='containers'):
                
                for inp in self.inputs:
                    yield inp 
                yield Button(id='add_button', label='Добавить тег',  classes='buttons')
                yield Button(id='post_button', label="Изменить строку", classes='buttons')
                yield Button(id='clear_button', label='Очистить поля', classes='buttons')
                yield Button(id='delete_button', label='Удалить строку', classes='buttons')


            with ScrollableContainer(id='data_box', classes='containers'):
                yield DataTable(id='data_table', cursor_type='row')

        yield RichLog()
        yield Footer()

    def on_mount(self):
        table = self.query_one(DataTable)
        table.add_columns(*[i.placeholder for i in self.inputs])
        self.dark = NIGHT
# ---- Обработка BINDINGS приложения -------
    def action_swap_theme(self):
        self.dark = not self.dark
        
    def action_save_file(self):
        """Сохраняем промежуточные данные при завершении работы"""
        f = Files()
        table_ = self.query_one(DataTable)  
        res = f.save_to_file([table_.get_row(key_) for key_ in table_.rows])
        self.query_one(RichLog).write([table_.get_row(key_) for key_ in table_.rows])
        if  res is None:
            self.query_one(RichLog).write('Файл успешно сохранен')
        else:
            self.query_one(RichLog).write(f'Файл не записан. Возникли проблемы {res}')

    def action_load_file(self):
        f = Files()
        """ Загружаем результаты работы из файла"""
        main_box = self.query_one("#data_box")
        main_box.mount(Input(id='load_file_name', placeholder='Имя файла для загрузки', value=f.file_name, classes='inputs'))
        main_box.refresh()
        
        
# --------------------------------------------

# ------------ обработчики событий виджетов
    @on(Input.Submitted, "#load_file_name")
    def load_file_name_submitted(self, event:Input.Submitted) -> None:
        res = Files().load_from_file(self.query_one('#load_file_name').value)
        if res is not None:
            table = self.query_one(DataTable)
            table.rows.clear()
            for row in res:
                table.add_row(*row)
            table.refresh()
            self.query_one(RichLog).write(f"Файл {self.query_one('#load_file_name').value} успешно загружен")
        else:
            self.query_one(RichLog).write(f"Файл {self.query_one('#load_file_name').value} не найден, или в файле ошибка")
        self.query_one('#load_file_name').remove()
        
            

    @on(Button.Pressed, "#add_button")
    def add_button_pressed(self, event:Button.Pressed) -> None:
        """При нажатии на кнопку копируется содержимое полей ввода в таблицу
        Args:
            event (Button.Pressed): Событие привязано к кнопке add_button
        """
        table = self.query_one('#data_table')
        res = (tuple([i.value for i in self.inputs]))
        self.query_one(RichLog).write(res)
        table.add_row(*res,)
        
    @on(Button.Pressed, '#clear_button')
    def clear_button_pressed(self) -> None:
        """Очищает поля ввода кроме постфикса для тега
        """
        for i in self.inputs[1:]:
            i.value = ''
    
    @on(Button.Pressed, '#delete_button')
    def delete_button_pressed(self) -> None:
        """Удаляем строку после выделения
        если таблица пустая, предупреждение в лог
        """
        table = self.query_one(DataTable)
        if table.row_count:
            row_key_, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
            table.remove_row(row_key_)
        else:
            self.query_one(RichLog).write("Table is empty!!")

        
    @on(DataTable.RowSelected, "#data_table")
    def data_table_row_selected(self) -> None:
        """Возвращаем значения из выбраной строки таблицы в поля ввода"""
        table = self.query_one(DataTable)
        key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
        for index, data in enumerate(table.get_row(row_key=key)):
            self.inputs[index].value = data        
            
    @on(Button.Pressed, "#post_button")
    def edit_button_pressed(self) -> None:
        """Записываем изменения в существующую запись"""
        table = self.query_one(DataTable)
        row_key, col_key = table.coordinate_to_cell_key(table.cursor_coordinate)
        self.query_one(RichLog).write()
        
    @on(DataTable.HeaderSelected)
    def header_selected(self, event:DataTable.HeaderSelected) -> None:
        def get_reverse(s:str) -> bool:
            reversed =  s in self.sorts
            if reversed:
                self.sorts.remove(s)
            else:
                self.sorts.add(s)
            return reversed    
            
        table = self.query_one(DataTable)
        table.sort(event.column_key, reverse=get_reverse(event.column_index))
                        
if __name__ == '__main__':
    appl = TextualKepApp()
    appl.run()
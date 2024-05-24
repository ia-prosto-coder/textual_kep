from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Input, DataTable, Button, RichLog, Select
from textual.scroll_view import ScrollView
from textual.containers import ScrollableContainer, Container
from textual import on

from validator import Validator
from files import Files
from additions import FileType

NIGHT = False
class TextualKepApp(App):
    def __init__(self):
        super().__init__()
        self.units = [('МПа', 0), ('С', 1), ('мм/с', 2), ('КПа', 3), ('Гц', 4), ('А', 5)]
        self.rtu_commands  =[
            ('01 Чтение DO', 1),
            ('02 Чтение DI', 2),
            ('03 Чтение AO', 3),
            ('04 Чтение AI', 4),
            ('05 Запись одного DO', 5),
            ('06 Запись одного AO', 6),
            ('15 Запись нескольких DO', 15),
            ('16 Запись нескольких AO', 16)
        ]
        self.inputs = [Input(id='postfix_button', placeholder='Постфикс тега'),
                Input(id='tag_name', classes='inputs', placeholder='Имя тега'),
                Input(id='address', classes='inputs', placeholder='Адрес регистра',),
                Input(id='description', classes='inputs', placeholder='Описание'),
                Select(id='command', classes='selects', options=self.rtu_commands, prompt='Команды  RTU'),
                Select(id='unit', classes='selects', options=self.units, prompt='Ед.измерения'),
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
    
    def compose(self) -> ComposeResult:
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
        for i in self.inputs:
            try:
                table.add_column(i.placeholder)
            except AttributeError as e:
                if isinstance(i, Select):
                    if i.id == 'unit':
                        table.add_column('Ед.измерения')
                    if i.id == 'command':
                        table.add_column('Команда RTU')
                    
        self.dark = NIGHT
# ---- Обработка BINDINGS приложения -------
    def action_swap_theme(self):
        self.dark = not self.dark
        
    def action_save_file(self):
        """Сохраняем промежуточные данные при завершении работы"""
        self.load_save_file(FileType.SAVE)


    def action_load_file(self):
        """ Загружаем результаты работы из файла"""
        self.load_save_file(FileType.LOAD)
    
    def load_save_file(self, ft:FileType):
        main_box = self.query_one("#data_box")
        match ft:
            case FileType.SAVE:
                f = Files(FileType.SAVE)
                _id = 'save_file_name'
                _placeholder = 'Имя файла для сохранения'
            case FileType.LOAD:
                f = Files(FileType.LOAD)
                _id = 'load_file_name'
                _placeholder = 'Имя файля для загрузки'
        try:
            main_box.mount(Input(id=_id, placeholder=_placeholder, value=f.file_name, classes='inputs'))
        except Exception:
            pass
# --------------------------------------------

# ------------ обработчики событий виджетов
    @on(Input.Submitted)
    def load_file_name_submitted(self, event:Input.Submitted) -> None:
        res = None
        table = self.query_one(DataTable)
        if event.input.id == 'load_file_name':        
# ------------ Если происходит загрузка файла, очищаем таблицу и загружаем данные из файла                
            res = Files(FileType.LOAD).load_from_file(self.query_one('#load_file_name').value)
            oper_string = f'Загрузка из файла {event.input.value}'
            if res is not None:
                table.rows.clear()
                for row in res:
                    table.add_row(*row)
                table.refresh()
        elif event.input.id == 'save_file_name':
# ----------- Если происходит сохранение файла выгружаем данные таблицы в список и сериализуем его 
            res = Files(FileType.SAVE).save_to_file([table.get_row(key_) for key_ in table.rows])    
            oper_string = f'Сохранение в файл {event.input.value}'
# ----------- Сообщаем всему миру об успехе или неудаче операции 
        if res is not None:
            self.query_one(RichLog).write(f"Файл {oper_string} успешно завершено")
        else:
            self.query_one(RichLog).write(f"Файл {event.input.value} не найден, или в файле ошибка")
        self.query_one(f'#{event.input.id}').remove()

    @on(Input.Submitted, "#save_file_name")
    def save_file_name_submitted(self, event:Input.Submitted) -> None:
        f = Files()
        table_ = self.query_one(DataTable)  
        res = f.save_to_file([table_.get_row(key_) for key_ in table_.rows])
        self.query_one(RichLog).write([table_.get_row(key_) for key_ in table_.rows])
        if  res is None:
            self.query_one(RichLog).write('Файл успешно сохранен')
        else:
            self.query_one(RichLog).write(f'Файл не записан. Возникли проблемы {res}')       
        

    @on(Button.Pressed, "#add_button")
    def add_button_pressed(self, event:Button.Pressed) -> None:
        """При нажатии на кнопку копируется содержимое полей ввода в таблицу
        Args:
            event (Button.Pressed): Событие привязано к кнопке add_button
        """
        def get_title(select:Select) -> str:
            lst_ = self.units if select.id == 'unit' else self.rtu_commands
            res_  = list(filter(lambda x:x[1]==select.value, lst_))[0][0]
            return res_
        
        table = self.query_one('#data_table')
        # self.query_one(RichLog).write(res)
        val = Validator().inputs_test(self.inputs)
        if val == True:
            res = (tuple([i.value if isinstance(i, Input) else get_title(i) for i in self.inputs]))
            table.add_row(*res,)
        else:
            for row in val:
                self.query_one(RichLog).write(row)
        
    @on(Button.Pressed, '#clear_button')
    def clear_button_pressed(self) -> None:
        """Очищает поля ввода кроме постфикса для тега
        """
        for i in self.inputs[1:]:
            try:
                i.value = ''
            except:
                i.clear()
                
    
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
            self.query_one(RichLog).write("Таблица пустая!!!")

        
    @on(DataTable.RowSelected, "#data_table")
    def data_table_row_selected(self) -> None:
        """Возвращаем значения из выбраной строки таблицы в поля ввода"""
        def get_select_key(id:str,  data) -> int:
            sel_ = None
            if id == 'command':
                sel_ = self.rtu_commands
            elif id == 'unit':
                sel_ = self.units  
            return list(filter(lambda x:x[0]==data, sel_))[0][1]
   
        
        table = self.query_one(DataTable)
        key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
        for index, data in enumerate(table.get_row(row_key=key)):
            if isinstance(self.inputs[index], Input):
                self.inputs[index].value = data
            elif isinstance(self.inputs[index], Select):
                self.inputs[index].value = get_select_key(self.inputs[index].id, data)
            
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

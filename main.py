from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Input, DataTable, Button, RichLog, Select, Switch, Label
from textual.scroll_view import ScrollView
from textual.containers import ScrollableContainer, Container, Horizontal
from textual import on

from validator import Validator
from files import Files
from export import Export
from additions import FileType, DataTypes,  PLACEHOLDERS

NIGHT = True
class TextualKepApp(App):
    def __init__(self):
        super().__init__()
        self.units = [('МПа', 0), ('С', 1), ('мм/с', 2), ('КПа', 3), ('Гц', 4), ('А', 5)]
        self.file_type = FileType.LOAD
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
        self.data_types = [
            (DataTypes.FLOAT.value, DataTypes.FLOAT),
            (DataTypes.INTEGER.value, DataTypes.INTEGER),
            (DataTypes.BOOLEAN.value, DataTypes.BOOLEAN)
        ]
        
        self.inputs = [Input(id='postfix_button', placeholder='Постфикс тега'),
                Input(id='tag_name', classes='inputs', placeholder='Имя тега'),
                Input(id='address', classes='inputs', placeholder='Адрес регистра',),
                Input(id='description', classes='inputs', placeholder='Описание'),
                Select(id='command', classes='selects', options=self.rtu_commands, prompt='Команды  RTU'),
                Select(id='data_type', classes='select', options=self.data_types, prompt='Тип данных'),
                Select(id='unit', classes='selects', options=self.units, prompt='Ед.измерения'),
                Input(id='eu_max', classes='inputs', placeholder='Макс. значение'),
                Input(id='eu_min', classes='inputs', placeholder='Мин. значение'),
                Switch(id='rw_switch', classes='Switch')
                ]
        self.sorts = set()
    

    CSS_PATH = 'main.tcss'
    BINDINGS = [
                ('L', 'load_file', 'Загрузить'),
                ('S', 'save_file', 'Сохранить'),
                ('C', 'copy_row', 'Дублировать'),
                ('T', 'swap_theme', 'Сменить тему'),
                ('W', 'weintek_export', 'Экспорт для панели Weintek'),
                ('I', 'intouch_export', 'Экспортв в Intouch'),
                ('K', 'kep_export', 'Экспорт в Kep'),
                ('Q', 'quit_app', 'Завершить приложение')
        ]
    
    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id='main_box'):           
                with ScrollableContainer(id='left_box', classes='containers'):
                    for inp in self.inputs:
                        if isinstance(inp, Switch):
                            with Horizontal():
                                yield Label('Режим доступа "R/W"', id='rw_label', classes='label')
                                yield inp
                        else:    
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
                    if i.id == 'data_type':
                        table.add_column("Тип данных")
                elif isinstance(i, Switch):
                    table.add_column('R/W')   
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

    def action_intouch_export(self):
        """Экспортируем результаты для загрузки в Intouch"""
        self.load_save_file(FileType.INTOUCH)

    def action_kep_export(self):
        """Экспортируем результаты для загрузки в Kep"""
        self.load_save_file(FileType.KEP)
    
    def action_weintek_export(self):
        """Экспортируем результаты для загрузки в Weintek"""
        self.load_save_file(FileType.WEINTEK)

    def load_save_file(self, ft:FileType):
        self.file_type = ft
        main_box = self.query_one("#data_box")
        try:
            main_box.mount(Input(id='file_name_input', placeholder=PLACEHOLDERS[ft.value], value=Files.create_file_name(ft), classes='inputs'))
        except Exception:
            self.query('#file_name_input').remove()
        main_box.refresh(layout=True)
# -------------------------------------------

# ------------ обработчики событий виджетов
    # @on(Switch.Changed, '#rw_switch')
    # def rw_switch_changed(self, event:Switch.Changed) -> None:

    @on(Input.Submitted, '#file_name_input')
    def file_name_input_submitted(self, event:Input.Submitted) -> None:
        res = None
        table = self.query_one(DataTable)
        match self.file_type:
            case FileType.LOAD:
# ------------ Если происходит загрузка файла, очищаем таблицу и загружаем данные из файла                
                res = Files(FileType.LOAD).load_from_file(self.query_one('#file_name_input').value)
                oper_string = f'Загрузка из файла {event.input.value}'
                if res is not None and isinstance(res, list):
                    table.rows.clear()
                    for row in res:
                        table.add_row(*row)
                    table.refresh()
                    self.query_one(RichLog).write(f"{oper_string} успешно завершенa")
                else:
                    self.query_one(RichLog).write(f"Ошибка загрузки из {event.input.value}.{res}")
            case FileType.SAVE:
# ----------- Если происходит сохранение файла выгружаем данные таблицы в список и сериализуем его 
                res = Files(FileType.SAVE).save_to_file([table.get_row(key_) for key_ in table.rows], self.query_one('#file_name_input').value)    
                oper_string = f'Сохранение в файл {event.input.value}'
                if res is None:
                    self.query_one(RichLog).write(f"{oper_string} успешно завершено")
                else:
                    self.query_one(RichLog).write(f"Ошибка сохранения {event.input.value}.{res}")    
            case FileType.KEP:
                Export().export_to_kep([table.get_row(key_) for key_ in table.rows], file_name=event.input.value)
                oper_string = f'Экспорт в KEP {event.input.value}'
        self.query_one(f'#{event.input.id}').remove()

    def get_title(self, select:Select) -> str:
        lst_ = self.rtu_commands
        match select.id:
            case 'unit':
                lst_ = self.units
            case 'command':
                lst_ = self.rtu_commands
            case 'data_type':
                lst_ = self.data_types    
        res_  = list(filter(lambda x:x[1]==select.value, lst_))[0][0]
        return res_

    @on(Button.Pressed, "#add_button")
    def add_button_pressed(self, event:Button.Pressed) -> None:
        """При нажатии на кнопку копируется содержимое полей ввода в таблицу
        Args:
            event (Button.Pressed): Событие привязано к кнопке add_button
        """

        table = self.query_one('#data_table')
        # Проверяем заполнение полей формы 
        val = Validator().inputs_test(self.inputs)
        if val == True:
            res = (tuple([self.get_title(i) if isinstance(i, Select) else i.value for i in self.inputs]))
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
            match id:
                case 'command':
                    sel_ = self.rtu_commands
                case 'unit':
                    sel_ = self.units
                case 'data_type':
                    sel_ = self.data_types  
            return list(filter(lambda x:x[0]==data, sel_))[0][1]
        
        table = self.query_one(DataTable)
        key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
        for index, data in enumerate(table.get_row(row_key=key)):
            if isinstance(self.inputs[index], Input):
                self.inputs[index].value = data
            elif isinstance(self.inputs[index], Switch):
                self.inputs[index].value = data    
            elif isinstance(self.inputs[index], Select):
                self.inputs[index].value = get_select_key(self.inputs[index].id, data)
            
    @on(Button.Pressed, "#post_button")
    def edit_button_pressed(self) -> None:
        """Записываем изменения в существующую запись"""
        table = self.query_one(DataTable)
        _row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
        _col_keys = list(table.columns.keys())
        val = Validator().inputs_test(self.inputs)
        if val == True:
            iter_cols = iter(_col_keys)
            for i in self.inputs:
                cur_col =  next(iter_cols)
                table.update_cell(row_key=_row_key, column_key=cur_col, value=self.get_title(i) if isinstance(i, Select) else i.value)
        
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

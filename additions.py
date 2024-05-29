import enum

class FileType(enum.Enum):
    INTOUCH = 0
    KEP = 1
    WEINTEK = 2
    LOAD = 3
    SAVE = 4

PLACEHOLDERS = ['Имя файла для выгрузки в Intouch',
                'Имя файла для выгрузки в KEP',
                'Имя файла для выгрузки в Weintek',
                'Имя файла для загрузки',
                'Имя файла для сохранения']

        
ID = 'ID'
SCHOOL_CODE = 'SCHOOL_CODE'
GRADE = 'GRADE'
NAME = 'NAME'
SURNAME = 'SURNAME'
PATRONYMIC = 'PATRONYMIC'
SHORT_TASKS = 'SHORT_QUESTS'
DETAIL_TASKS = 'DETAIL_TASKS'
RAW_SCORE = 'RAW_SCORE'
FINAL_SCORE = 'FINAL_SCORE'

__MARK = 'Оценка'
__SCORE = 'Балл'

_DEFAULT_COLUMN_NAMES = {
    ID: '№',
    SCHOOL_CODE: 'Код ОО',
    GRADE: 'Класс',
    SURNAME: 'Фамилия',
    NAME: 'Имя',
    PATRONYMIC: 'Отчество',
    SHORT_TASKS: 'Задания с кратким ответом',
    DETAIL_TASKS: 'Задания с развёрнутым ответом',
    RAW_SCORE: 'Первичный балл',
    FINAL_SCORE: ['Оценка', 'Балл'],
}


def get_default_cоlumn_names(grade):
    if grade == 9:
        _DEFAULT_COLUMN_NAMES[FINAL_SCORE] = __MARK
    elif grade == 11:
        _DEFAULT_COLUMN_NAMES[FINAL_SCORE] = __SCORE
    else:
        raise ValueError('Grade must be a number equal to 9 or 11')
    return _DEFAULT_COLUMN_NAMES

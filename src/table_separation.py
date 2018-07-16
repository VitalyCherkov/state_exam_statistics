import pandas

from src.constants.binay_task_indicators import BINARY_TASK_INDICATORS, BINARY_TASK_VALUES
from src.constants.default_column_names import SHORT_TASKS, DETAIL_TASKS


def process_short_tasks(table, short_tasks_col_name):
    """
    обрабатывает столбец задач с коротким ответом:
    разбивает на отдельные столбцы для каждой задачи,
    преобразовывая '+' и '-' в 1 и 0,
    создает массив с максимально возможными баллами для каждой задачи
    """

    # Разделяем столбец с +--01+ на отдельные колонки
    short_task_cols = table[short_tasks_col_name]\
        .apply(lambda row: pandas.Series(list(row)))

    # Создаем массив из максимальных баллов для текущей задачи
    max_results = [
        (
            lambda x: 1 if x in BINARY_TASK_INDICATORS else 2
        )(short_task_cols[col].iloc[0])
        for col in short_task_cols
    ]

    # Заменяем + на 1, - на 0
    for indicator in BINARY_TASK_INDICATORS:
        short_task_cols = short_task_cols.replace(indicator, BINARY_TASK_VALUES[indicator])
    short_task_cols = short_task_cols.applymap(lambda x: int(x))

    return short_task_cols, max_results


def parse_detail_tasks_line(detail_results_line):
    """
    преобразовывает строку с резальтатам отдельного ученика
    по задачам с детальным ответом
    в массив объектов, хранящих информацию
        - о текущем балле ученика по данной задаче
        - о максимально возможном балле по данной задаче
    """
    detail_results_array = detail_results_line.split(')')
    parsed_results = []
    for res in detail_results_array:
        try:
            [cur, max] = res.split('(')
            parsed_results.append({
                'cur': int(cur), 'max': int(max)
            })
        except Exception:
            pass
    return parsed_results


def process_detail_tasks(table, detail_tasks_col_name):
    """
    обрабатывает столбец задач с детальным ответом:
    разбивает на отдельные столбцы по каждой задаче,
    формирует массив максимально возможных баллов по каждой задаче
    """

    # получение максимально возможного балла для каждой задачи
    first_line = table[detail_tasks_col_name].iloc[0]
    split_first_line = parse_detail_tasks_line(first_line)
    max_results = [item['max'] for item in split_first_line]

    # выбирает столбец с результатами задач с развернутым ответом
    # и разделяет его на отдельные стобцы с текущим результатом
    # по каждой задаче
    detail_task_cols = table[detail_tasks_col_name]\
        .apply(
            lambda row: pandas.Series(
                [item['cur'] for item in parse_detail_tasks_line(row)]
            )
        )

    return detail_task_cols, max_results


def get_merged_table(table, column_names):
    """
    возвращает итоговую таблицу с результатами:
    объединяет столбцы задач с детальным ответом и столбцы с коротким ответом
    """

    short_task_cols, short_task_maxes = \
        process_short_tasks(table, column_names[SHORT_TASKS])
    detail_task_cols, detail_task_maxes = \
        process_detail_tasks(table, column_names[DETAIL_TASKS])

    merged_cols = pandas.concat([short_task_cols, detail_task_cols], axis=1)
    merged_cols.columns = [i for i in range(1, len(merged_cols.columns) + 1)]

    merged_maxes = short_task_maxes
    merged_maxes.extend(detail_task_maxes)

    return merged_cols, merged_maxes

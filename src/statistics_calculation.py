import functools
import operator

from src.constants.common_parameter_names import ACADEMIC_PERFORMANCE, QUALITY, AVERAGE_GRADE
from src.weight_functions import (
    get_academic_performance_weight,
    get_quality_weight,
    get_average_grade_weight
)


def calc_percentages_per_task(columns, max_results):
    """
    возвращает массив суммарных баллов по каждой задаче
    и массив процентов решений каждой задачи
    """
    rows_number = columns.shape[0]
    total_by_task = columns.sum(axis=0)
    total_by_task = [value for index, value in total_by_task.iteritems()]
    percentages_by_task = [
        round(value / (max_results[index] * rows_number) * 100)
        for index, value in enumerate(total_by_task)
    ]
    return percentages_by_task


def calc_common_statistics_via_func(marks_column, weight_func):
    """
    подсчитывет статистику для данной задачи
    по переданной весовой функции
    """
    total_count = len(marks_column)
    weighted_sequence = [
        mark
        for index, mark in
        marks_column.apply(weight_func).iteritems()
    ]

    total_weight = functools.reduce(operator.add, weighted_sequence, 0)
    return round(total_weight / total_count * 100)


def get_common_statistics(table, marks_column_name):
    """
    подсчитывает статистики для девятых классов
    """
    marks_column = table[marks_column_name]\
        .apply(lambda x: int(x))

    academic_performance = calc_common_statistics_via_func(
        marks_column=marks_column,
        weight_func=get_academic_performance_weight
    )
    quality = calc_common_statistics_via_func(
        marks_column=marks_column,
        weight_func=get_quality_weight
    )
    average_grade = calc_common_statistics_via_func(
        marks_column=marks_column,
        weight_func=get_average_grade_weight
    )

    return {
        ACADEMIC_PERFORMANCE: str(academic_performance),
        QUALITY: str(quality),
        AVERAGE_GRADE: str(average_grade),
    }

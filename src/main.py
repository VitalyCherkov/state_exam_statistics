import pandas
from django.template import Context

from src.constants.default_column_names import get_default_cоlumn_names, FINAL_SCORE, SURNAME, NAME, PATRONYMIC, ID, \
    SCHOOL_CODE, RAW_SCORE
from src.constants.row_names import MAX_SCORE_ROW_TITLE, NAME_COLUMN_TITLE, TOTAL_BY_TASK_ROW_TITLE, \
    PERCENTAGE_BY_TASK_ROW_TITLE
from src.statistics_calculation import calc_percentages_per_task, get_common_statistics
from src.table_separation import get_merged_table
from src.templator import get_html


def read_file(file_name, col_names):
    raw_data = pandas.read_csv(file_name, header=0, index_col=col_names[ID])
    selected_cols = [raw_data[col] for col in raw_data]
    selected_df = pandas.concat(selected_cols, axis=1)
    return selected_df


def get_full_names_col(table, col_names):
    name_col = table[col_names[NAME]].apply(lambda x: '{0}.'.format(x[0]))
    patronumic_col = table[col_names[PATRONYMIC]].apply(lambda x: '{0}.'.format(x[0]))
    full_names_col = table[col_names[SURNAME]] \
                       + ' ' + name_col + patronumic_col
    return full_names_col


def append_row(table, row, title=None):

    if title:
        row = [title] + row

    table.loc[table.shape[0] + 1] = row
    return table


def get_pd_col_as_df(title, data):
    return pandas.DataFrame(data={
        title: data
    }).applymap(lambda x: str(x))


def get_additional_cols_for_students(table, col_names):
    full_names_df = get_pd_col_as_df(
        title=NAME_COLUMN_TITLE,
        data=get_full_names_col(table, col_names)
    )
    school_code_df = get_pd_col_as_df(
        title=col_names[SCHOOL_CODE],
        data=table[col_names[SCHOOL_CODE]]
    )
    raw_score_df = get_pd_col_as_df(
        title=col_names[RAW_SCORE],
        data=table[col_names[RAW_SCORE]]
    )
    final_score_df = get_pd_col_as_df(
        title=col_names[FINAL_SCORE],
        data=table[col_names[FINAL_SCORE]]
    )
    return full_names_df, school_code_df, raw_score_df, final_score_df


def get_final_calculations(table, col_names):

    full_names_df, school_code_df, raw_score_df, final_score_df \
        = get_additional_cols_for_students(table, col_names)

    final_cols, final_maxes = get_merged_table(table, col_names)
    percentages_by_task = calc_percentages_per_task(final_cols, final_maxes)

    tasks_statistics = pandas.DataFrame(columns=['', *final_cols])
    tasks_statistics = append_row(tasks_statistics, final_maxes, MAX_SCORE_ROW_TITLE)
    tasks_statistics = append_row(tasks_statistics, percentages_by_task, PERCENTAGE_BY_TASK_ROW_TITLE)

    final_table = pandas.concat([
        school_code_df,
        full_names_df,
        final_cols,
        raw_score_df,
        final_score_df
    ], axis=1)
    final_table = final_table.sort_values(by=[
        col_names[SCHOOL_CODE],
        NAME_COLUMN_TITLE
    ])

    return final_table, tasks_statistics


def get_marks_stats(table, col_names):
    counts = [
        (
            grade,
            table[
                table[col_names[FINAL_SCORE]] == str(grade)
            ].count()
        ) for grade in range(3, 6)
    ]
    return counts


def get_statistics_9th_grade():
    col_names = get_default_cоlumn_names(9)
    table = read_file(file_name='../data/9_geo.csv', col_names=col_names)

    final_table, tasks_statistics = get_final_calculations(table, col_names)

    common_statistics = {
        'common': get_common_statistics(table, col_names[FINAL_SCORE]),
        'marks': get_marks_stats(final_table, col_names)
    }

    return final_table, tasks_statistics, common_statistics


def get_statistics_11th_grade():
    col_names = get_default_cоlumn_names(11)
    table = read_file(file_name='../data/11_geo.csv', col_names=col_names)

    final_table, tasks_statistics = get_final_calculations(table, col_names)
    return final_table, tasks_statistics, {}


def prepare_final_table_context(table):
    return {
        'header': [str(item) for item in list(table.columns)],
        'rows': [
            [str(row[col]) for col in table.columns]
            for index, row in table.iterrows()
        ]
    }


def prepare_context(final_table, tasks_statistics, common_statistics=None):
    return Context({
        'students_table': prepare_final_table_context(final_table),
        'tasks_statistics_table': prepare_final_table_context(tasks_statistics),
        'common_statistics': common_statistics
    })


def main():
    print('11th')
    results = get_statistics_11th_grade()
    context = prepare_context(*results)
    get_html(context)


main()

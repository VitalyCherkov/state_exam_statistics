# УСП 9 класс
def get_academic_performance_weight(value):
    return 1 if value != 2 else 0


# КАЧ 9 класс
def get_quality_weight(value):
    return 1 if value > 3 else 0


# СОУ 9 класс
def get_average_grade_weight(value):
    if value == 5:
        return 1
    elif value == 4:
        return 0.64
    elif value == 3:
        return 0.36
    else:
        return 0.12

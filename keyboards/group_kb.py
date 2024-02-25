from keyboards.inline import create_buttons_inline


FIRST_COURSE_KB = create_buttons_inline(
    buttons={
        '131': '131',
        '132': '132',
        '133': '133',
        '134': '134',
        '135': '135',
        '136': '136',
        '137': '137',
        '31': '31',
        '32': '32',
        'Назад': 'group_dashboard',
        'В начало': 'home'
    },
    sizes=(2, 2, 1, 1, 1, 2, 2)
)

SECOND_COURSE_KB = create_buttons_inline(
    buttons={
        '221': '221',
        '222': '222',
        '223': '223',
        '224': '224',
        '225': '225',
        '226': '226',
        '227': '227',
        '21': '21',
        '22': '22',
        'Назад': 'group_dashboard',
        'В начало': 'home'
    },
    sizes=(2, 2, 1, 1, 1, 2, 2)
)

THIRD_COURSE_KB = create_buttons_inline(
    buttons={
        '311': '311',
        '312': '312',
        '313': '313',
        '314': '314',
        '315': '315',
        '316': '316',
        '11': '11',
        '12': '12',
        'Назад': 'group_dashboard',
        'В начало': 'home'
    },
    sizes=(2, 2, 1, 1, 2, 2)
)

FOURTH_COURSE_KB = create_buttons_inline(
    buttons={
        '401': '401',
        '402': '402',
        '403': '403',
        '404': '404',
        '405': '405',
        '406': '406',
        'Назад': 'group_dashboard',
        'В начало': 'home'
    },
    sizes=(2, 2, 1, 1, 2)
)

group_dict = {1: FIRST_COURSE_KB, 2: SECOND_COURSE_KB, 3: THIRD_COURSE_KB, 4: FOURTH_COURSE_KB}

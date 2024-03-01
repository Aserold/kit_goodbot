from keyboards.inline import create_buttons_inline

FIRST_COURSE_KB = create_buttons_inline(
    buttons={
        "131": "groupnum_131",
        "132": "groupnum_132",
        "133": "groupnum_133",
        "134": "groupnum_134",
        "135": "groupnum_135",
        "136": "groupnum_136",
        "137": "groupnum_137",
        "31": "groupnum_31",
        "32": "groupnum_32",
        "Назад": "group_dashboard",
        "В начало": "home",
    },
    sizes=(2, 2, 1, 1, 1, 2, 2),
)

SECOND_COURSE_KB = create_buttons_inline(
    buttons={
        "221": "groupnum_221",
        "222": "groupnum_222",
        "223": "groupnum_223",
        "224": "groupnum_224",
        "225": "groupnum_225",
        "226": "groupnum_226",
        "227": "groupnum_227",
        "21": "groupnum_21",
        "22": "groupnum_22",
        "Назад": "group_dashboard",
        "В начало": "home",
    },
    sizes=(2, 2, 1, 1, 1, 2, 2),
)

THIRD_COURSE_KB = create_buttons_inline(
    buttons={
        "311": "groupnum_311",
        "312": "groupnum_312",
        "313": "groupnum_313",
        "314": "groupnum_314",
        "315": "groupnum_315",
        "316": "groupnum_316",
        "11": "groupnum_11",
        "12": "groupnum_12",
        "Назад": "group_dashboard",
        "В начало": "home",
    },
    sizes=(2, 2, 1, 1, 2, 2),
)

FOURTH_COURSE_KB = create_buttons_inline(
    buttons={
        "401": "groupnum_401",
        "402": "groupnum_402",
        "403": "groupnum_403",
        "404": "groupnum_404",
        "405": "groupnum_405",
        "406": "groupnum_406",
        "Назад": "group_dashboard",
        "В начало": "home",
    },
    sizes=(2, 2, 1, 1, 2),
)

group_dict = {
    1: FIRST_COURSE_KB,
    2: SECOND_COURSE_KB,
    3: THIRD_COURSE_KB,
    4: FOURTH_COURSE_KB,
}

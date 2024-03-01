import requests
from bs4 import BeautifulSoup


def parse_schedule():
    url = 'https://spb-kit.ru/studentam/raspisanie_zanyatiy_zameny/'

    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')

    schedule_divs = soup.find_all('div', class_='schedule-block-main-content')

    # Список, чтобы хранить все данные расписания для всех групп
    all_schedule_data = []

    # Вытащим данные для всех групп
    for schedule_div in schedule_divs:
        group_number = int(schedule_div['data-tab'])
        schedule_table = schedule_div.find('table', class_='schedule-block-main-content-table-main')
        group_schedule_data = []
        for row in schedule_table.find_all('tr')[1:]:  # Пропускаем первый день, так как там дни недели
            columns = row.find_all('td')
            time = columns[0].find('div', class_='schedule-table-row-time').text.strip()[:5]
            for idx, column in enumerate(columns[1:]):  # пропускаем первый столбец, так как там время
                day = idx + 1
                lesson_info = column.find('div', class_='schedule-table-row-text')  # находим инфу о предметах
                if lesson_info:  # если там не пусто
                    lesson = lesson_info.text.strip()  # получаем предмет
                    group_schedule_data.append({'group': group_number, 'time': time, 'day': day, 'lesson': lesson})
        all_schedule_data.extend(group_schedule_data)

    # Сортируем данные и обрезаем, чтобы не дублировались
    sorted_schedule_data = sorted(all_schedule_data, key=lambda x: (x['group'], x['day'], x['time']))[::2]

    # Для проверки данных
    # for entry in sorted_schedule_data:
    #     print(f"Group: {entry['group']}, Day: {entry['day']}, Time: {entry['time']}, Lesson: {entry['lesson']}")
    return sorted_schedule_data

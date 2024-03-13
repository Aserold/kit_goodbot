from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def parse_subs():
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Remote(
        command_executor="http://localhost:4444/wd/hub", options=chrome_options
    )

    driver.get("http://rep.spb-kit.online:8005/replacements/view.html")

    try:
        body_element = driver.find_element(By.TAG_NAME, "html")

        html = body_element.get_attribute("innerHTML")
        soup = BeautifulSoup(html, "html.parser")

    except Exception as e:
        print("Error occurred:", e)
        return

    driver.quit()
    schedule_data = []
    header = soup.find("td", class_="header").text.split()
    day = header[1]
    date = header[2]
    schedule_data.append({"day": day})
    schedule_data.append({"date": date})

    group_list = [
        group.text
        for group in soup.find_all("td", class_="section")
        if group.text not in [
            '.',
            '*',
            'Расписание и замены смотри на сайте '
            'www.spbkit.edu.ru в разделе "студентам"'
        ]
    ]

    for group in group_list:
        group_data = {"group": group, "lectures": []}
        schedule_data.append(group_data)

    current_group = None
    for row in soup.find_all("tr"):
        if row.find("td", class_="section"):
            current_group = row.text.strip()
        elif row.find("td", class_="content"):
            pair_data = [
                cell.text.strip() for cell in row.find_all(
                    "td", class_="content"
                )
            ]
            if len(pair_data) >= 5:
                pair_info = {
                    "lecture_number": pair_data[0],
                    "subject": pair_data[1],
                    "substitute_teacher": pair_data[2],
                    "new_subject": pair_data[3],
                    "classroom": pair_data[4],
                }
                for item in schedule_data:
                    if "group" in item and item["group"] == current_group:
                        item["lectures"].append(pair_info)
                        break
            elif len(pair_data) == 4:
                pair_info = {
                    "lecture_number": pair_data[0],
                    "subject": pair_data[1],
                    "substitute_teacher": "ПАРА ПЕРЕНЕСЕНА",
                    "new_subject": "",
                    "classroom": "",
                }
                for item in schedule_data:
                    if "group" in item and item["group"] == current_group:
                        item["lectures"].append(pair_info)
                        break

    default_pair_info = {
        "lecture_number": "№ пары",
        "subject": "Заменяемый предмет",
        "substitute_teacher": "Заменяющий преподаватель",
        "new_subject": "Новый предмет",
        "classroom": "Кабинет",
    }

    for item in schedule_data:
        if "group" in item:
            item["lectures"] = [
                pair for pair in item["lectures"] if pair != default_pair_info
            ]

    return schedule_data

# print(parse_subs())

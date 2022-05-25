import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def get_page_data():
    url = 'https://www.marathonbet.ru/su/live/announces'
    driver = webdriver.Chrome()
    driver.maximize_window()
    try:
        driver.get(url=url)
        driver.implicitly_wait(10)
        driver.find_element(By.CLASS_NAME, 'announce-filter').find_element(By.TAG_NAME, 'a').click()
        driver.implicitly_wait(10)

        announces_today = driver.page_source

        driver.find_element(By.XPATH, "//*[contains(text(), 'Завтра')]").click()
        time.sleep(5)

        announces_tomorrow = driver.page_source

        with open("announces_today.html", 'w', encoding='utf-8') as file:
            file.write(announces_today)
        with open("announces_tomorrow.html", 'w', encoding='utf-8') as file:
            file.write(announces_tomorrow)
    except:
        print(Exception)
    finally:
        driver.quit()


def gather_data_today():
    with open("announces_today.html", 'r', encoding='utf-8') as file:
        html = file.read()
    soup = BeautifulSoup(html, 'lxml')
    announces = soup.find('div', class_='announce-page').find_all('table')
    del announces[0]

    with open("announces_today.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Event",
                "Description",
                "Time"
            )
        )

    for announce in announces:
        try:
            event = announce.find('td', class_='label-container').find(class_='event').text
        except:
            event = None

        try:
            description = []
            container_description = announce.find('td', class_='label-container description').find_all('span', class_='nowrap')
            for item in container_description:
                item = item.text
                description.append(item)
        except:
            description = None

        try:
            time = announce.find('td', class_='right-container').text.strip()
        except:
            time = None

        with open("announces_today.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow(
                (
                    event,
                    description,
                    time
                )
            )


def gather_data_tomorrow():
    with open("announces_tomorrow.html", 'r', encoding='utf-8') as file:
        html = file.read()
    soup = BeautifulSoup(html, 'lxml')
    announces = soup.find('div', class_='announce-page').find_all('table')
    del announces[0]

    with open("announces_tomorrow.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Event",
                "Description",
                "Time"
            )
        )

    for announce in announces:
        try:
            event = announce.find('td', class_='label-container').find(class_='event').text
        except:
            event = None

        try:
            description = []
            container_description = announce.find('td', class_='label-container description').find_all('span',
                                                                                                       class_='nowrap')
            for item in container_description:
                item = item.text
                description.append(item)
        except:
            description = None

        try:
            time = announce.find('td', class_='right-container').text.strip()
        except:
            time = None

        with open("announces_tomorrow.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow(
                (
                    event,
                    description,
                    time
                )
            )


def main():
    get_page_data()
    gather_data_today()
    gather_data_tomorrow()

if __name__ == '__main__':
    main()
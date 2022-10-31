import time
import csv

from openpyxl import load_workbook

from selenium.webdriver.common.by import By

from settings_chrome import driver


def create_details_csv(details):
    with open("details.csv", mode="a", encoding='utf-8') as w_file:
        titles = [
            'name',
            'description',
        ]
        for detail in details:
            file_writer = csv.DictWriter(w_file, delimiter=",", lineterminator="\r", fieldnames=titles)
            file_writer.writeheader()
            file_writer.writerow(detail)


def get_articles():
    excel_file = load_workbook(filename='1000артикулов.xlsx')
    sheet = excel_file['Sheet1']
    column_a = sheet['A']
    articles = [column_a[row].value for row in range(len(column_a))]
    return articles


def main():
    main_url = 'https://partscatalog.deere.com/jdrc/search/type/parts/term/'

    details = []
    for article in get_articles():
        try:
            url = main_url + article
            driver.get(url)
            driver.implicitly_wait(30)
            time.sleep(5)

            detail = driver.find_element(By.CSS_SELECTOR,
                                         '#applicationContainer > div.userInterface > div.content > div.viewContent > '
                                         'div.viewContentContainer > app-search > div > div.catalogResults > '
                                         'app-search-results > div > div.linkList.ng-star-inserted > a:nth-child(1)')
            detail.click()

            name = driver.find_element(By.CLASS_NAME, 'locationtext')
            description = driver.find_element(By.CLASS_NAME, 'partremarkstext')

            detail = {
                'name': name.text,
                'description': description.text,
            }

            details.append(detail)

        except Exception as error:
            print(error)

    create_details_csv(details)


if __name__ == '__main__':
    main()

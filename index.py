from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import getpass
import time
import Gmail


def login(driver, username_str, password_str):
    driver.get('https://www.huntington.com')
    username = driver.find_element_by_id("personal-username")
    password = driver.find_element_by_id("personal-password")

    username.send_keys(username_str)
    password.send_keys(password_str)

    button = driver.find_element_by_xpath("//button[contains(@class,\"btn--gray\") and contains(@aria-label,"
                                          "\"Log in to Huntington Online Banking\")]")
    button.click()


def register_device(driver):
    error = "Huntington National Bank - Device Registration"
    h2_val = error in driver.title
    return h2_val


def select_verification(driver):
    checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div[1]/div/div[5]/div/div/div/main/div/form/div[8]/div/label')))
    if not checkbox.is_selected():
        checkbox.click()

    driver.find_element_by_xpath('/html/body/div[1]/div/div[5]/div/div/div/main/div/form/div[12]/button').submit()


def do_verification(driver):
    veri_code = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/div[1]/div/div[5]/div/div/div/main/div/form/div[5]/input')))

    veri_code.send_keys(Gmail.main())

    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div[1]/div/div[5]/div/div/div/main/div/form/div[7]/button')))
    button.submit()


def do_question_verification(driver, answer):
    answer_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/div[1]/div/div[5]/div/div/div/main/div/form/div[4]/input')))
    answer_box.send_keys(answer)


def answer_to_question(question):
    answer = ' '
    with open('testquestions.txt') as f:
        for line in f:
            line = line.strip()
            if line == question:
                answer = next(f)
                break
    return answer


def dont_register_device(driver):
    dont_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="Register_False_span"]')))
    dont_button.click()

    go_to_my_accounts = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="btnContinue"]')))
    go_to_my_accounts.submit()


def get_into_checking_account(driver):
    lol = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="primaryHubContent"]/div/div[6]/main/div[1]/div[4]/div[2]/div[1]/div/div/div/div'
                   '[2]/div/div[2]/div/div[2]')))
    lol.click()


def create_excel_file(file_name, date_time, company, type_trans, price):
    with open('Data/%s.csv' % file_name, 'a+', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Details', 'Transaction Type', 'Price'])
        writer.writerow([date_time, company, type_trans, price])


def write_excel_file(file_name, date_time, company, type_trans, price):
    with open('Data/%s.csv' % file_name, 'a+', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([date_time, company, type_trans, price])


# fix this lol
def transferToExcel(driver):
    date_month = 0
    date_year = 0

    while True:
        time.sleep(3)
        try:
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            elm = driver.find_element_by_xpath("//button[contains(@class,\"b-g-bare\") and contains(@aria-label,"
                                               "\"Goto Next Page\")]")

            for date in soup.find_all('div', {"class": 'c-g-account-details-table__row'})[1:]:
                date1 = date.get('data-date')
                company = date.get('data-description')
                type_trans = date.get('data-tran-type')
                price = date.get('data-amount')

                date_array = date1.split(' ')
                date_string = date_array[0]
                size = len(date_string)

                if (date_month != date_string[:2]) or (date_year != date_string[size - 4:size]):
                    date_month = date_string[:2]
                    date_year = date_string[size - 4:size]
                    create_excel_file(str(date_month) + " " + str(date_year), date_string, company, type_trans, price)
                else:
                    write_excel_file(str(date_month) + " " + str(date_year), date_string, company, type_trans, price)
            if elm.get_attribute("display") != 'none':
                elm.click()
            else:
                break
        except:
            break


def main():
    username_str = input("Enter Huntington Username: ")
    password_str = getpass.getpass(prompt="Enter Huntington Password:")
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome('./chromedriver', options=options)
    driver.maximize_window()

    login(driver, username_str, password_str)
    time.sleep(5)
    if register_device(driver):
        select_verification(driver)
        time.sleep(10)
        do_verification(driver)
        time.sleep(3)
        label = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="formContent"]/div[4]/label')))
        answer = answer_to_question(label.text)
        time.sleep(3)
        do_question_verification(driver, answer)
        time.sleep(3)
        dont_register_device(driver)

    get_into_checking_account(driver)
    dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="CurrentDateRange__dropdown"]')))
    dropdown.click()

    six_months = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="CurrentDateRange_container_option-4"]')))
    six_months.click()

    transferToExcel(driver)

    print("Done!")
    driver.quit()


if __name__ == '__main__':
    main()

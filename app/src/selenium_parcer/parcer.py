from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from app.src.selenium_parcer.selenium_instance import driver
from app.settings import settings

group = 1

def get_all_students(wait) -> list:
    fio_divs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "fio")))
    all_students = []
    global group
    # Извлечение текстового содержимого
    with open(f"group{group}", 'w') as students:
        for div in fio_divs:
            student = div.text
            student = student[:student.find('\n')] #только фамилии
            all_students.append(student)
            students.write(student + '\n')
    group+=1
    return all_students

    # print(div.text)  # Печатаем текст внутри div

def run_registration(links: list) -> list:
    try:
        driver.get(settings.MFUA)
        driver.implicitly_wait(10)
        wait = WebDriverWait(driver, 10)  # Можно заменить на более динамическое ожидание
        login_input = driver.find_element(By.NAME, "USER_LOGIN")
        login_input.send_keys(settings.LOGIN)

        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Войти')]")
        login_button.click()

        driver.implicitly_wait(10)
        password_button = wait.until(EC.element_to_be_clickable((By.ID, "FormsAuthentication")))
        password_button.click()

        print("Кнопка 'Вход с помощью пароля' нажата")

        driver.implicitly_wait(10)
        password_input = driver.find_element(By.ID, "passwordInput")
        password_input.send_keys(settings.PASSWORD)

        submit_button = driver.find_element(By.ID, "submitButton")
        submit_button.click()

        # Ожидание загрузки страницы после логина
        driver.implicitly_wait(10)

        # Сохранение cookies после полной авторизации
        cookies = driver.get_cookies()
        print("Сохраненные cookies:", cookies)

        # Переход на страницу с классом студентов
        driver.delete_all_cookies()
        students = []
        for link in links:
            driver.get(link)

            # Устанавливаем сохраненные cookies
            for cookie in cookies:
                driver.add_cookie(cookie)

            # Перезагружаем страницу после установки cookies
            driver.refresh()
            wait = WebDriverWait(driver, 10)

            students_row = get_all_students(wait)
            for student in students_row:
                students.append(student)

            print('round ' + str(group))
        return students
    finally:
        driver.quit()


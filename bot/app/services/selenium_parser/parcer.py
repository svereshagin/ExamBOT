from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bot.app.services.selenium_parser.selenium_instance import driver
from bot.app.config import settings
from bot.app.services.selenium_parser.utils import get_links
from bot.app.logger.logger_file import logger


group: int = 1
logger.info(msg=settings)


def get_all_students(wait) -> list:
    """
    Returns parsed students
    """
    fio_divs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "fio")))
    all_students = []
    global group
    # Извлечение текстового содержимого
    with open(f"group{group}", "w") as students:
        for div in fio_divs:
            student = div.text
            student = student[: student.find("\n")]  # только фамилии
            all_students.append(student)
            students.write(student + "\n")
            logger.info(f"Добавлен студент: {student}")  # Логируем добавление студента
    group += 1
    logger.info(
        f"Обработана группа: {group - 1}, общее количество студентов: {len(all_students)}"
    )  # Логируем информацию о группе
    return all_students


def get_students_from_site(user_data: tuple) -> list:
    """
    Принимает пользовательские данные данные в видео кортежа из
    login, password, links
    и заходит по ним в аккаунт
    по ссылкам переходит и достаёт учеников
    Runs registration and after successful registration
    returns a list of students into main program
    """
    # links = get_links()
    try:
        logger.info("Начало процесса получения студентов с сайта.")
        logger.info(str(user_data[0]))
        logger.info(str(user_data[1]))
        logger.info(str(user_data[2]))
        driver.get(settings.MFUA)
        driver.implicitly_wait(10)

        logger.info("Ввод логина.")
        login_input = driver.find_element(By.NAME, "USER_LOGIN")
        login_input.send_keys(user_data[0])

        logger.info('Нажатие кнопки "Войти".')
        login_button = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Войти')]"
        )
        login_button.click()

        driver.implicitly_wait(10)
        logger.info("Ожидание кнопки для ввода пароля.")
        password_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "FormsAuthentication"))
        )
        password_button.click()

        logger.info("Кнопка 'Вход с помощью пароля' нажата.")

        driver.implicitly_wait(10)
        logger.info("Ввод пароля.")
        password_input = driver.find_element(By.ID, "passwordInput")
        password_input.send_keys(user_data[1])

        logger.info('Нажатие кнопки "Отправить".')
        submit_button = driver.find_element(By.ID, "submitButton")
        submit_button.click()

        # Ожидание загрузки страницы после логина
        driver.implicitly_wait(10)

        # Сохранение cookies после полной авторизации
        cookies = driver.get_cookies()
        logger.info("Сохраненные cookies получены.")

        # Переход на страницу с классом студентов
        driver.delete_all_cookies()
        students = []
        links: list = user_data[2]
        for link in links:
            logger.info(f"Переход на страницу: {link}")
            driver.get(link)

            # Устанавливаем сохраненные cookies
            for cookie in cookies:
                driver.add_cookie(cookie)

            # Перезагружаем страницу после установки cookies
            driver.refresh()
            wait = WebDriverWait(driver, 10)

            students_row = get_all_students(wait)
            students.extend(students_row)

            logger.info(
                f"Обработан раунд {group - 1}, добавлено студентов: {len(students_row)}"
            )

        logger.info(f"Общее количество студентов, полученных с сайта: {len(students)}")
        return students
    except Exception as e:
        logger.error(f"Ошибка при получении студентов: {e}")
    finally:
        logger.info("Закрытие драйвера.")
        driver.quit()

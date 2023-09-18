import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from decouple import config

from rate import models

logger = logging.getLogger(__name__)

chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--headless")


def initialize_driver():
    return webdriver.Chrome(options=chrome_options)


def get_url(driver, url):
    a = driver.get(url)
    logger.debug(a)


def click_show_more(driver, btn) -> bool:
    """
    Функция для раскрытия страницы
    :param driver:
    :return: bool
    """
    try:
        show_more_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, btn))
        )
        print(11, show_more_button)

        show_more_button.click()
        return True
    except:
        logger.info('Все страницы раскрыты.')
        return False


def update_or_create_rate(data) -> None:
    """
    Функция добавления или обновления данных.
    :param data:
    :return: None
    """
    try:
        rate = models.Rate.objects.get(card_title=data['card_title'])

        logger.info('Обновляем данные.')
        for key, value in data.items():
            setattr(rate, key, value)
        rate.save()
    except models.Rate.DoesNotExist:
        logger.info('Если записи не существует, создаем новую')
        models.Rate.objects.create(**data)


def extract_card_data(card_element) -> dict:
    """
    Функция для извлечения данных из карточки услуг.
    :param card_element: данные карточки услуг.
    :return: возвращаем словарь с данными услуг.
    """
    data = {}

    try:
        badge_text = card_element.find_element(By.CSS_SELECTOR, config('BADGE_TEXT')).text
    except:
        badge_text = ''

    card_title = card_element.find_element(By.CSS_SELECTOR, config('CARD_TITLE')).text
    data['card_title'] = card_title

    try:
        card_description = card_element.find_element(By.CSS_SELECTOR, config('CARD_DESCRIPTION')).text
        data['card_description'] = card_description
    except:
        data['card_description'] = ''
    try:
        feature_elements = card_element.find_element(By.CLASS_NAME, config('FEATURE_WRAPPER')).text
        for feature_element in feature_elements:
            feature_text = feature_element.find_element(By.CLASS_NAME, config('FEATURE_DESCRIPTION')).text

            if "ГБ" in feature_text:
                data['internet'] = feature_text
            elif "минут" in feature_text:
                data['calls'] = feature_text
            elif "бит/с" in feature_text:
                data['speed'] = feature_text
            elif "ТВ" in feature_text:
                data['tv'] = feature_text
    except:
        pass

    try:
        price_main = card_element.find_element(By.CLASS_NAME, config('PRICE_MAIN')).find_element(By.CLASS_NAME,
                                                                                                 'price-text').text

        price_quota = card_element.find_element(By.XPATH,
                                                config('PRICE_QUOTA')).text
        data['price_main'] = price_main.replace(' ', '')
        data['price_quota'] = price_quota
    except:
        data['price_main'] = None
        data['price_quota'] = ''

    try:
        price_sale = card_element.find_element(By.CLASS_NAME, config('PRICE_SALE')).find_element(By.CLASS_NAME,
                                                                                                 'price-text').text
        data['price_sale'] = price_sale.replace(' ', '')
    except:
        data['price_sale'] = None

    try:
        annotate_price = card_element.find_element(By.CLASS_NAME, config('ANNOTATE_PRICE')).text
        if badge_text:
            data['annotate_price'] = badge_text + '.' + annotate_price
        else:
            data['annotate_price'] = annotate_price
    except:
        data['annotate_price'] = ''

    logger.info('Возвращаем карточку услуг.')
    return data


def run_parser():
    """
    Функция запуска парсера.
    :return: None
    """
    driver = None
    try:
        logger.info('Ищем все карточки услуг на сайте.')
        urls = [config('URL1'), config('URL2'), config('URL3'), config('URL4')]

        driver = initialize_driver()

        for url in urls:
            get_url(driver, url)
            while click_show_more(driver, config('BTN')):
                time.sleep(1)

            card_elements = driver.find_elements(By.XPATH, config('ELEMENTS'))

            logger.info(card_elements)

            card_data_list = []
            for card_element in card_elements:
                card_data = extract_card_data(card_element)
                card_data_list.append(card_data)

            logger.info(card_data_list)

            logger.info('Добавляем (обновляем) карточки услуг в базе.')
            for item in card_data_list:
                update_or_create_rate(item)
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_parser()

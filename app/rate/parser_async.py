import logging
import time
import asyncio
import aiohttp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from rate import models

logger = logging.getLogger(__name__)

chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--headless")


async def initialize_driver():
    return webdriver.Chrome(options=chrome_options)



async def get_url(driver, url):
    a = await driver.get(url)
    logger.debug(a)



async def click_show_more(driver) -> bool:
    """
    Функция для раскрытыя страницю
    :param driver:
    :return: bool
    """
    try:
        show_more_button = await asyncio.wait_for(
            driver.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn.btn_secondary'))
            ), timeout=10)
        show_more_button.click()
        return True
    except:
        logger.info('Все страницы раскрыты.')
        return False



async def update_or_create_rate(data) -> None:
    """
    Функция добавления или обновления данных.
    :param data:
    :return: None
    """
    try:
        # Попытка получить существующую запись по критериям (например, по card_title)
        rate = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: models.Rate.objects.get(card_title=data['card_title'])
        )


        logger.info('Обновляем данные.')
        for key, value in data.items():
            setattr(rate, key, value)
        await asyncio.get_event_loop().run_in_executor(None, rate.save)
    except models.Rate.DoesNotExist:
        logger.info('Если записи не существует, создаем новую')
        await asyncio.get_event_loop().run_in_executor(
            None, lambda: models.Rate.objects.create(**data)
        )

async def extract_card_data(card_element) -> dict:
    """
    Функция для извлечения данных из карточки услуг.
    :param card_element: данные карточки услуг.
    :return: возвращаем словарь с данными услуг.
    """
    data = {}

    try:
        badge_text = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: card_element.find_element(By.CSS_SELECTOR, '.badge-text').text)
    except:
        badge_text = ''


    card_title = await asyncio.get_event_loop().run_in_executor(
        None,
        lambda: card_element.find_element(By.CSS_SELECTOR, '.card-title__link').text)
    data['card_title'] = card_title

    try:
        card_description = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: card_element.find_element(By.CSS_SELECTOR, '.card-description.card-description__margin').text)
        data['card_description'] = card_description
    except:
        data['card_description'] = ''

    feature_elements = await asyncio.get_event_loop().run_in_executor(
        None,
        lambda: card_element.find_element(By.CLASS_NAME, 'feature__wrapper').text)
    for feature_element in feature_elements:
        feature_text = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: feature_element.find_element(By.CLASS_NAME, 'feature-description__text').text)

        if "ГБ" in feature_text:
            data['internet'] = feature_text
        elif "минут" in feature_text:
            data['calls'] = feature_text
        elif "бит/с" in feature_text:
            data['speed'] = feature_text
        elif "ТВ" in feature_text:
            data['tv'] = feature_text

    try:
        price_main = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: card_element.find_element(By.CLASS_NAME, 'price-main').find_element(By.CLASS_NAME,
                                                                                         'price-text').text)

        price_quota =  await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: card_element.find_element(By.XPATH,
                                                '//span[contains(@class, "price-text") and contains(@class, "price-quota") and contains(@class, "price-text__quota-margin")]').text)
        data['price_main'] = price_main.replace(' ', '')
        data['price_quota'] = price_quota
    except:
        data['price_main'] = None
        data['price_quota'] = ''

    try:
        price_sale = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: card_element.find_element(By.CLASS_NAME, 'price-sale__margin').find_element(By.CLASS_NAME,
                                                                                                 'price-text')).text
        data['price_sale'] = price_sale.replace(' ', '')
    except:
        data['price_sale'] = None

    try:
        annotate_price = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: card_element.find_element(By.CLASS_NAME, 'price-annotation__margin')).text
        if badge_text:
            data['annotate_price'] = badge_text + '.' + annotate_price
        else:
            data['annotate_price'] = annotate_price
    except:
        data['annotate_price'] = ''
    logger.info('Возвращаем карточку услуг.')
    return data


async def run_parser():
    """
    Функция запуска парсера.
    :return: None
    """
    try:
        logger.info('Ищем все карточки услуг на сайте.')
        url = "https://moskva.mts.ru/personal/mobilnaya-svyaz/tarifi/vse-tarifi/mobile-tv-inet"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()

        driver = await initialize_driver()
        await get_url(driver, 'data:text/html;charset=utf-8,' + html)
        #logger.info(a)
        while await click_show_more(driver):
            await asyncio.sleep(1)

        card_elements = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: driver.find_elements(By.XPATH,'//div[contains(@class, "card__wrapper")]')
        )

        card_data_list = []
        for card_element in card_elements:
            card_data = await extract_card_data(card_element)
            card_data_list.append(card_data)

        logger.info('Добавляем (обновляем) карточки услуг в базе.')
        await asyncio.gather(*(update_or_create_rate(item) for item in card_data_list))
    finally:
        if driver:
            await asyncio.get_event_loop().run_in_executor(None, driver.quit)



if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_parser())

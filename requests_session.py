import creds
import os
import time
from rich.console import Console
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

console = Console()

payload = {
    "username": creds.user,
    "password": creds.password,
}

timing = time.ctime().replace(":", " ")


def logging():
    '''
    login to the website
    '''
    if page.is_visible('input#username'):
        page.fill("input#username", creds.user)
        page.fill("input#password", creds.password)
        page.press('input#password', 'Enter')
    else:
        time.sleep(1)
        logging()


with sync_playwright() as sp:
    browser = sp.firefox.launch(headless=False, slow_mo=30)
    page = browser.new_page()
    page.goto(creds.loging_url)
    for i in range(2):
        logging()
        time.sleep(1)
        if page.url == creds.loging_url:
            print("Login failed")
            logging()
        else:
            print("Login successful")
            page.goto(creds.usb_manage)
            break
    print(page.url)
    html = page.inner_html('#content')
    soup = BeautifulSoup(html, 'html.parser')

    # with open('output.html', 'w') as f:
    #     f.truncate(0)
    #     f.write(soup.prettify())

    # console.print(soup.prettify(), style="dim")
    # class_list = [' ]

    page.locator("span[contains(@class, 'js-accordion-chevron bills-accordion__chevron'").click()
    item = soup.find_all(
        class_="grid__item grid__item--gutter grid__item--middle grid__item--sm-1/1 grid__item--1/4 grid__item--center")
    console.print(item, style="dim")

    # TODO ==> serch for the correct way to click the dynamic toggle button!!
    # page.locator("text= New Generic At Home 300LE").click()
    page.mouse.wheel(delta_x=0, delta_y=100)
    page.screenshot(path=f"./screenshot {timing} .png")
    browser.close()

    # html = page.inner_html('#content')
    # soup = BeautifulSoup(html, 'html.parser')
    # console.log(soup.prettify(), style="dim")
    # # class_list = ['grid__item grid__item--gutter grid__item--middle
    # grid__item--sm-1/1 grid__item--1/4 grid__item--center',
    # #               ]
    # item = soup.find_all(class_="bundle-circle bundle-circle-red")
    # print(item)

from rich.console import Console
import creds
import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import os

console = Console()

payload = {
    "username": creds.user,
    "password": creds.password,
}


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
    for i in range(3):
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
    page.locator(class="js-accordion-heading bills-accordion__heading").click()
    item = soup.find_all(class_="grid__item grid__item--gutter grid__item--middle grid__item--sm-1/1 grid__item--1/4 grid__item--center")
    console.print(item, style="dim")
    browser.close()

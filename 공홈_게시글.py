import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

if __name__ == "__main__":
    공홈 = pd.read_csv('공홈.csv')

    driver = webdriver.Chrome('chromedriver.exe')

    data_text = []

    for _ in range(len(공홈)):
        url = 공홈['링크'][_]
        driver.get(url)
        
        if _ % 100 == 0:
            print(f"{_}번째 글 크롤링중...")
        
        wait = WebDriverWait(driver, 3)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#jwxe_main_content > div.jwxe_board > div > dl > dd > div.cont_area")))
        soup = BeautifulSoup(element.get_attribute('outerHTML'), 'html.parser')
        text = ' '.join(soup.stripped_strings)
        data_text.append([url, text])
    
    driver.quit()

    df_게시글 = pd.DataFrame(data_text, columns=["링크", "본문"])

    공식홈페이지 = pd.merge(공식홈페이지, df_게시글, on = '링크', how = 'left')

    공식홈페이지.to_csv('공식홈페이지.csv', index = False)
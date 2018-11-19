from selenium import webdriver
from selenium.webdriver.chrome.options import Options
 
url = 'https://www.python.org/'
 
options = Options()
options.add_argument('--headless')
 
browser = webdriver.Chrome(chrome_options=options)
browser.implicitly_wait(3)
 
browser.get(url)
browser.save_screenshot('python.png')
 
browser.quit()
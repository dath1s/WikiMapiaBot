from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.common.by import By
import time
import uuid


def getAPIKey(username, pw) -> str:
    payload = {
        'username': username,
        'pw1': pw,
    }

    lastKey = '31B06847-E251A1CF-9C47236E-01D3FC9A-C74EA018-294BB69E-43921E67-99220EBC'

    svc = webdriver.ChromeService(executable_path=binary_path)
    driver = webdriver.Chrome(service=svc)

    try:
        driver.get('https://wikimapia.org/')
        time.sleep(1)

        enterBtn = driver.find_element(By.CLASS_NAME, 'n-0-2')
        enterBtn.click()
        time.sleep(1)

        driver.switch_to.frame(driver.find_element(By.CLASS_NAME, 'modal-body'))
        username = driver.find_element(By.NAME, 'username')
        username.clear()
        username.send_keys(payload['username'])
        username = driver.find_element(By.NAME, 'pw1')
        username.clear()
        username.send_keys(payload['pw1'])
        logInBtn = driver.find_element(By.CLASS_NAME, 'login-submit')
        logInBtn.click()
        time.sleep(1)

        driver.get('https://wikimapia.org/api/?action=create_key')
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, 'checkbox').click()
        driver.find_element(By.NAME, 'site_name').send_keys(str(uuid.uuid1()))
        driver.find_element(By.CLASS_NAME, 'btn-primary').click()
        time.sleep(1)

        driver.get('https://wikimapia.org/api/?action=my_keys')
        lastKey = driver.find_elements(By.TAG_NAME, 'dd')[1:][::4][-1].text.split()[0]
    except Exception as e:
        pass
    finally:
        driver.close()
        driver.quit()

    return lastKey

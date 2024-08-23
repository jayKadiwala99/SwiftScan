from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# Set up the webdriver (you may need to download the appropriate webdriver for your browser)
company = input("Enter: ")
url = "https://www.screener.in"
driver = webdriver.Chrome()

driver.get(url)
elem = driver.find_element(By.XPATH, "/html/body/main/div[2]/div/div/div/input")
elem.send_keys(company)
time.sleep(2)
elem = driver.find_elements(By.CLASS_NAME, "active")
elem[1].click()
wait = WebDriverWait(driver, 10)  # 10 seconds timeout
elem = wait.until(EC.presence_of_element_located((By.ID, "top-ratios")))
data = elem.text

lst = data.split("\n")
map = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}

print()
for k,v in map.items():
    print(k,"->",v)
print("\nDONE")
driver.quit()
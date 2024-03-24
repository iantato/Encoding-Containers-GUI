
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.utils.csv import PointTransactions
from app.exceptions.login import IncorrectLogin
from app.config import DOWNLOAD_DIR

class Webdriver:
    
    def __init__(self) -> None:
        self.setup()
    
    def setup(self) -> None:
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--enable-chrome-browser-cloud-management')
        chrome_options.add_experimental_option('prefs', {
            "download.default_directory": DOWNLOAD_DIR,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
        })
        
        self.driver = Chrome(options=chrome_options)
    
    def login(self, driver: Chrome, username: str, password: str, url: str) -> None:
        
        match url:
            case 'https://ictsi.vbs.1-stop.biz':
                
                driver.get(url)
                try:
                    # Username input field.
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.ID, 'USERNAME'))
                    ).send_keys(username)
                    
                    # Password input field.
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.ID, 'PASSWORD'))
                    ).send_keys(password)
                    
                    # Submit the form/Login to the website.
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div[3]/form'))
                    ).submit()

                    # Incorrect password/username handler.
                    try:
                        WebDriverWait(driver, 5).until(
                            EC.visibility_of_element_located((By.ID, 'vbs_new_selected_FACILITYID'))
                        )
                    except TimeoutException:
                        try:
                            error = WebDriverWait(driver, 5).until(
                                EC.visibility_of_element_located((By.ID, 'msgHolder'))
                            )
                            
                            if error.size != 0:
                                raise IncorrectLogin("Incorrect Login")
                    
                        except TimeoutException:
                            pass
                    finally:
                        pass
                    
                finally:
                    pass
                
    def download_csv(self, driver: Chrome, start: str, end: str) -> None:
        
        # Asian Terminal Inc.
        driver.get('https://atimnl.vbs.1-stop.biz/default.aspx?vbs_new_selected_FACILITYID=ATIMNL&vbs_Facility_Changed=true')
        
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/form/div[6]/div[4]/div[3]/div/table/tbody/tr/td[2]/span/span/input'))
            ).click()
            
            PointTransactions(driver, start, end, "ATIMNL")
            
        except TimeoutException:
            pass
        finally:
            pass
        
        
        # Manila International Container Terminal Services, Inc.
        driver.get('https://ictsi.vbs.1-stop.biz/Default.aspx?vbs_Facility_Changed=true&vbs_new_selected_FACILITYID=ICTSI&attempt=0')
        
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/form/div[6]/div[4]/div[3]/div/table/tbody/tr/td/span/span/input'))
            ).click()
            
            PointTransactions(driver, start, end, "ICTSI")
        except TimeoutException:
            pass
        finally:
            pass
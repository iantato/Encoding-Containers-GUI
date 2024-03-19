
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.exceptions.login import IncorrectLogin

class Webdriver:
    
    def __init__(self) -> None:
        self.setup()
    
    def setup(self) -> None:
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--enable-chrome-browser-cloud-management')
        # chrome_options.add_experimental_option('prefs', {
        #     "download.default_directory": DIR + '\\data',
        #     "download.prompt_for_download": False,
        #     "download.directory_upgrade": True,
        #     "plugins.always_open_pdf_externally": True
        # })
        
        self.driver = Chrome(options=chrome_options)

    
    def login(self, driver: Chrome,
              username: str, password: str, url: str) -> None:
        
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
                        error = WebDriverWait(driver, 5).until(
                            EC.visibility_of_element_located((By.ID, 'msgHolder'))
                        )
                        
                        if error.size != 0:
                            raise IncorrectLogin("Incorrect Login")
                    
                    except TimeoutException:
                        pass
                    
                finally:
                    pass
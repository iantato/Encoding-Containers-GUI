
import datetime

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.config import BASE_DIR, DOWNLOAD_DIR

class PointTransactions:
    
    def download(self, driver: Chrome, start: datetime.date, end: datetime.date, max: int):
        
        driver.get("https://ictsi.vbs.1-stop.biz/PointsTransactions.aspx")
        
        if start.weekday() != 0 and max >= 7:
            calc = 7 - start.weekday()
            max -= calc
            end = start + datetime.timedelta(days = calc)
            
        elif max >= 7:
            calc = 7
            max -= calc
            end = start + datetime.timedelta(days = calc)
            
        elif 0 < max < 7:
            calc = max
            max -= calc
            end = start + datetime.timedelta(days = calc)
        
        # Start date.
        try:
            date_from = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "PointsTransactionsSearchForm___DATEFROM"))
            )
            driver.execute_script(
                "arguments[0].removeAttribute('readonly')",
                date_from
            )
            date_from.clear()
            date_from.send_keys(f'{start.day}/{start.month}/{start.year}')
        except TimeoutException:
            pass
        # End date.
        try:
            date_to = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "PointsTransactionsSearchForm___DATETO"))
            )
            driver.execute_script(
                "arguments[0].removeAttribute('readonly')",
                date_from
            )
            date_to.clear()
            date_to.send_keys(f'{end.day}/{end.month}/{end.year}')
        except TimeoutException:
            pass
        # Submit and download.
        try:
            WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.ID, "PointsTransactionsSearchForm___REFERENCE"))
            ).click()
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "Search"))
            ).click()
            
            WebDriverWait(driver, 120).until(
                EC.element_to_be_clickable((By.ID, "CSV"))
            ).click()
        except TimeoutException:
            pass
        
        if max > 0:
            return self.download(driver, start + datetime.timedelta(days = calc), end, max)
    
    def move_files(self) -> None:
        pass
            
    
    # def download_mictsi(self, driver: Chrome, start: datetime.date, end: datetime.date) -> None:
    #     pass
    
    # def move_files(self, file_name: str) -> None:
    #     pass
    
    # def clean(self) -> None:
    #     pass
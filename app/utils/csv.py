
import datetime
import os
from time import sleep

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.config import DOWNLOAD_DIR

class PointTransactions:
    
    def __init__(self, driver: Chrome, start: str, end: str, file_name: str) -> None:
        
        start = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        end = datetime.datetime.strptime(end, "%Y-%m-%d").date()
        
        max = (end - start).days + 1
        
        self.download(driver, start, end, max, file_name)
    
    def download(self, driver: Chrome, start: datetime.date, end: datetime.date, max: int, file_name: str):
        
        sleep(2)
        driver.get(f'https://{file_name.lower()}.vbs.1-stop.biz/PointsTransactions.aspx')
        
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
                WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable(date_from)
                )
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
                WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable(date_to)
                )
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
        
        finally:
            self.move_files(start, end, file_name)
        
        if max > 0:
            return self.download(driver, start + datetime.timedelta(days = calc), end, max, file_name)
    
    def move_files(self, start: datetime.date, end: datetime.date, file_name: str) -> None:
        
        file = DOWNLOAD_DIR + "\\PointsTransactions.csv"
        file_name = f'{start.strftime("%B %d, %Y")} - {end.strftime("%B %d, %Y")} ({file_name}).csv'
        
        while not os.path.exists(file):
            sleep(1)
            
            if os.path.isfile(file):
                os.rename(file, f'{DOWNLOAD_DIR}\\sheets\\{file_name}')
                return
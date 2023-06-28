import os
import sys
import subprocess
from time import sleep
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chromium.options import ChromiumOptions

load_dotenv()


class Agent:
    def __init__(self):
        self.link = 'https://web.whatsapp.com/'
        option = ChromiumOptions()
        option.headless = False
        self.driver = webdriver.Chrome(options=option)

    def make_login(self):

        self.driver.get(url=self.link)

        input('Type something to continue: ')

    def enter_conversation(self, contact_name: str):
        span_element = self.driver.find_element(By.XPATH, f"//span[@title='{contact_name}']")
        span_element.click()

    def search_by_specific_message(self, message: str):
        seconds_pass = 0
        while True:
            try:
                self.driver.find_element(By.XPATH, f"//span[.='{message}']")
                print("Element found!")
                self.play_song('acorda_pedrinho.mp3')
                break
            except:
                sleep(1)
                seconds_pass += 1
                print(f'Not Found. Waiting more... Total {seconds_pass} seconds')

        sleep(30)

        self.driver.close()

    @staticmethod
    def play_song(song_path: str):
        if sys.platform.startswith('darwin'):
            # macOS
            subprocess.run(['afplay', song_path])
        elif sys.platform.startswith('win'):
            # Windows
            os.startfile(song_path)
        elif sys.platform.startswith('linux'):
            # Linux
            subprocess.run(['xdg-open', song_path])
        else:
            print('Unsupported platform. Cannot play song.')



contact_name = os.getenv('CONTACT_NAME')

agent = Agent()
agent.make_login()
agent.enter_conversation(contact_name)
agent.search_by_specific_message('.')

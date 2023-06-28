from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep

class Agent:
    def __init__(self):
        self.link = 'https://sports.bwin.com/pt-br/sports/futebol-4/aposta/brasil-33/brasileir%C3%A3o-s%C3%A9rie-a-102838'
        options = Options()
        options.headless = False
        self.driver = webdriver.Chrome(options=options)

    def collect_texts(self):
        # Find all ms-event-group elements
        self.driver.get(url=self.link)
        # input('Press enter when finish load: ')
        sleep(8)

        self.driver.find_element(By.CLASS_NAME, 'ui-icon.theme-ex').click()

        ms_event_groups = self.driver.find_elements(By.TAG_NAME, 'ms-event-group')

        days: list[Day] = []
        for ms_event_group in ms_event_groups:
            header_wrapper = ms_event_group.find_element(By.CLASS_NAME, 'header-wrapper')
            ms_date_header = header_wrapper.find_element(By.TAG_NAME, 'ms-date-header')
            text = ms_date_header.text

            ms_events = self.driver.find_elements(By.TAG_NAME, 'ms-event')
            for event in ms_events:
                pass

            # games = Game()
            days.append(Day(text, []))

        for day in days:
            print(day.name, day.games)

        input('Press to exit: ')
        self.driver.close()


from dataclasses import dataclass

@dataclass
class Game:
    name: str

@dataclass
class Day:
    name: str
    games: list[Game]


agent = Agent()
agent.collect_texts()

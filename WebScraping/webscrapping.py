from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
from bs4 import BeautifulSoup



class User:
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.link = 'https://siga.cps.sp.gov.br/aluno/login.aspx'


    def getAbsences(self):
        option = Options()
        option.headless = False # Hide driver
        driver = webdriver.Firefox(options=option)
        driver.get(url=self.link)

        campo_user = driver.find_element_by_css_selector('#vSIS_USUARIOID')
        sleep(1)
        campo_user.send_keys(self.user)
        field_password = driver.find_element_by_css_selector('#vSIS_USUARIOSENHA')
        field_password.send_keys(self.password)

        btn_login = driver.find_element_by_css_selector('.Button')
        btn_login.click()

        sleep(3)

        driver.find_element_by_id('ygtvlabelel10Span').click()
        sleep(3)

        element = driver.find_element_by_id('Grid3ContainerDiv')
        html_content = element.get_attribute('outerHTML')
        soup = BeautifulSoup(html_content, 'html.parser')


        subjects = []
        elements = soup.find_all('span')
        for i in elements:
            if i.next_element == 'Disciplina':
                subjects.append(i.next_element)


        faltas = {}


        for i in range(len(subjects)):
            # print('Matéria: ', soup.find('span', {'id': f'span_CTLACD_DISCIPLINASIGLA1_000{i+1}'}).next_element)
            # print('Faltas: ', soup.find('span', {'id': f'span_CTLACD_ALUNOHISTORICOITEMQTDFALTAS_000{i+1}'}).next_element)
            faltas[soup.find('span', {'id': f'span_CTLACD_DISCIPLINASIGLA1_000{i+1}'}).next_element] = (
                soup.find('span', {'id': f'span_CTLACD_ALUNOHISTORICOITEMQTDFALTAS_000{i+1}'}).next_element).strip()

        driver.quit()

        return faltas


userFatec_input = input('User: ')
passwordFatec_input = input('Password: ')

userFatec = User(userFatec_input, passwordFatec_input)
print(userFatec.getAbsences())
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

class MySeleniumTests(StaticLiveServerTestCase):
    # carregar una BD de test
    fixtures = ['testdb.json',]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        # tanquem browser
        # comentar la propera línia si volem veure el resultat de l'execució al navegador
        #cls.selenium.quit()
        super().tearDownClass()

    def _setSelected(self, option):
       if not option.is_selected():
          option.click()


    def _unsetSelected(self, option):
        if option.is_selected():
            option.click()

    def test_user(self):
        # anem directament a la pàgina d'accés a l'admin panel
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))


        # comprovem que el títol de la pàgina és el que esperem
        self.assertEqual( self.selenium.title , "Log in | Django site admin" )

        # introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('isard')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()

        # testejem que hem entrat a l'admin panel comprovant el títol de la pàgina
        self.assertEqual(self.selenium.title , "Site administration | Django site admin")

        # anem a la pàgina d'usuaris de l'admin panel
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/auth/user/'))

        # testejem que hem entrat a l'administració d'usuaris comprovant el títol de la pàgina
        self.assertEqual(self.selenium.title , "Select user to change | Django site admin")

        #clica botó ADD USER
        self.selenium.find_element(By.CSS_SELECTOR,"#content-main .object-tools li a").click()

        #omple dades de l'usuari, pàgina
        self.assertEqual(self.selenium.title , "Add user | Django site admin")

        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('usuari_test')
        password_input = self.selenium.find_element(By.ID,"id_password1")
        password_input.send_keys('StudentIOC@2024')
        password_input = self.selenium.find_element(By.ID,"id_password2")
        password_input.send_keys('StudentIOC@2024')

        #clica botó Save and continue editing
        self.selenium.find_element(By.XPATH,'//input[@value="Save and continue editing"]').click()

        #omple dades de l'usuari, pàgina2
        self.assertEqual(self.selenium.title , "usuari_test | Change user | Django site admin")

        #marca permís Staff
        self.selenium.find_element(By.ID,"id_is_staff").click()

        #tria permisos	
        #select_element = self.selenium.find_element(By.CSS_SELECTOR,"#id_user_permissions_from")
        #elf.selenium.find_element(By.ID,"id_user_permissions_from")
        select_element = self.selenium.find_element(By.ID,'id_user_permissions_from')
        #objSelect.selectByVisibleText("Automation");
        #select = Select(select_element)
        #select.select_by_value('13')
        if select_element.get_attribute('multiple'):
            option = self.selenium.find_element(By.XPATH,"//select[@multiple]/option[contains(text(), 'Authentication and Authorization | user | Can add user')]").click()
        
        self.selenium.find_element(By.ID,"id_user_permissions_add_link").click()
        if select_element.get_attribute('multiple'):
            option = self.selenium.find_element(By.XPATH,"//select[@multiple]/option[contains(text(), 'Authentication and Authorization | user | Can view user')]").click()

        self.selenium.find_element(By.ID,"id_user_permissions_add_link").click()

        #clica SAVE per finalizar
        self.selenium.find_element(By.NAME,"_save").click()

        # testejem que hem entrat a l'administració d'usuaris comprovant el títol de la pàgina
        self.assertEqual(self.selenium.title , "Select user to change | Django site admin")

        #clica LOG OUT per sortir i comprobar permisos entrant amb l'usuari creat
        #self.selenium.find_element(By.NAME,"_save").click()

        self.selenium.find_element(By.XPATH,"//button[text()='Log out']").click()

        self.assertEqual( self.selenium.title , "Logged out | Django site admin" )
        self.selenium.find_element(By.LINK_TEXT, 'Log in again').click()

        #comprovem que el títol de la pàgina és el que esperem
        self.assertEqual( self.selenium.title , "Log in | Django site admin" )

        #introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('usuari_test')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('StudentIOC@2024')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()

        #testejem que hem entrat a l'admin panel comprovant el títol de la pàgina
        self.assertEqual(self.selenium.title , "Site administration | Django site admin")

        
        #testejem que el mòdule Questions no existeix per l'usuari usuari_test
        try:
            self.selenium.find_element(By.XPATH,"//a[text()='Questions']")
            assert False, "Trobat element que NO hi ha de ser"
        except NoSuchElementException:
            pass

        self.selenium.find_element(By.XPATH,"//button[text()='Log out']").click()

        self.assertEqual(self.selenium.title , "Logged out | Django site admin")

from selenium import webdriver
import unittest
import random

class Register(unittest.TestCase):
    def setUp(self):
        self.wd = webdriver.Chrome("C:/WebDrivers/chromedriver.exe")
        self.wd.maximize_window()
        self.wd.implicitly_wait(5)
    def Reg(self, name, surname, mail, phone, password, password_confirm):
        self.wd.get("https://dev.devse.xyz/register")
        self.wd.find_element_by_xpath("//body/div[1]/div[1]/div[2]/form[1]/div[1]/input[1]").send_keys(str(name))
        self.wd.find_element_by_xpath("//body/div[1]/div[1]/div[2]/form[1]/div[2]/input[1]").send_keys(str(surname))
        self.wd.find_element_by_xpath("//body/div[1]/div[1]/div[2]/form[1]/div[3]/input[1]").send_keys(str(mail))
        self.wd.find_element_by_xpath("//body/div[1]/div[1]/div[2]/form[1]/div[4]/input[1]").send_keys(str(phone))
        self.wd.find_element_by_xpath("//body/div[1]/div[1]/div[2]/form[1]/div[5]/input[1]").send_keys(str(password))
        self.wd.find_element_by_xpath("//body/div[1]/div[1]/div[2]/form[1]/div[6]/input[1]").send_keys(str(password_confirm))
        self.wd.find_element_by_xpath("//body/div[1]/div[1]/div[2]/form[1]/div[7]/label[1]/input[1]").click()
        print(" E-mail =", str(mail))

    def Check(self, check_temp):
        self.wd.find_element_by_xpath("//button[contains(text(),'Регистрация')]").click()
        self.wd.find_element_by_xpath(str(check_temp))

    def tearDown(self):
        self.wd.quit()

    @staticmethod
    def Mail():
        mail_temp = "test" + str(random.randint(1, 1000)) + "@gmail.com"
        return mail_temp

    @staticmethod
    def Phone():
        phone_temp = "+380" + str(random.randint(100000000, 999999999))
        return phone_temp

# Позитивный кейс на регистрацию
    def test_1(self):

        Register.Reg(self, name="name", surname="surname", mail=Register.Mail(),
                     phone=Register.Phone(), password="1234567a", password_confirm="1234567a")
        Register.Check(self, check_temp="//div[contains(text(),'Информация по аккаунту')]")
        Register.tearDown(self)

# Кейс на проверку количества символов в пароле
    def test_2(self):
        Register.Reg(self, name="name", surname="surname", mail=Register.Mail(),
                     phone=Register.Phone(), password="123456a", password_confirm="123456a")
        Register.Check(self, check_temp="//li[contains(text(),'The Пароль must be at least 8 characters.')]")
        Register.tearDown(self)

# Кейс на проверку несоответствия пароля и подтвержденного пароля
    def test_3(self):
        Register.Reg(self, name="name", surname="surname", mail=Register.Mail(),
                     phone=Register.Phone(), password="123456a", password_confirm="1234567a")
        Register.Check(self, check_temp="//li[contains(text(),'Поле Пароль не совпадает с подтверждением.')]")
        Register.tearDown(self)

# Кейс на проверку правильного заполнения поля "E-mail" (бэк валидация)
    def test_4(self):
        Register.Reg(self, name="name", surname="surname", mail="test" + str(random.randint(1, 1000)),
                     phone=Register.Phone(), password="1234567a", password_confirm="1234567a")
        elem = self.wd.find_element_by_xpath("//body/div[1]/div[1]/div[2]/form[1]/div[3]/input[1]")
        self.wd.execute_script("arguments[0].type = 'text';", elem)
        Register.Check(self, check_temp="//li[contains(text(),'Поле E-Mail адрес должно быть действительным элект')]")
        Register.tearDown(self)

# Кейс на проверку правильного заполнения поля "Телефон"
    def test_5(self):
        Register.Reg(self, name="name", surname="surname", mail=Register.Mail(),
                     phone="ffff" + str(random.randint(100000000, 999999999)), password="1234567a",
                     password_confirm="1234567a")
        # Register.Check(self, check_temp="//li[contains(text(),"")]")
        self.wd.find_element_by_xpath("//button[contains(text(),'Регистрация')]").click()
        print(self.wd.current_url)
        assert self.wd.current_url == "https://dev.devse.xyz/register"
        Register.tearDown(self)

# Кейс на проверку установленного флажка "Я согласен с Условиями..."
    def test_6(self):
        Register.Reg(self, name="name", surname="surname", mail=Register.Mail(),
                     phone=Register.Phone(), password="1234567a", password_confirm="1234567a")
        self.wd.find_element_by_xpath("//body/div[1]/div[1]/div[2]/form[1]/div[7]/label[1]/input[1]").click()
        elem = self.wd.find_element_by_xpath("//body/div[1]/div[1]/div[2]/form[1]/div[7]/label[1]/input[1]")
        self.wd.execute_script('arguments[0].removeAttribute("required")', elem)
        self.wd.find_element_by_xpath("//button[contains(text(),'Регистрация')]").click()
        print(self.wd.current_url)
        assert self.wd.current_url == "https://dev.devse.xyz/register"
        # Register.Check(self, check_temp="//li[contains(text(),'Вы не согласились с условиями')]")
        Register.tearDown(self)

# Кейс на проверку регистрации пользователя с уже существующим E-Mail в системе
    def test_7(self):
        mail_current_user = Register.Mail()
        Register.Reg(self, name="name", surname="surname", mail=mail_current_user,
                     phone=Register.Phone(), password="1234567a", password_confirm="1234567a")
        Register.Check(self, check_temp="//div[contains(text(),'Информация по аккаунту')]")
        self.wd.find_element_by_xpath("//span[contains(text(),'Выйти')]").click()
        Register.Reg(self, name="name", surname="surname", mail=mail_current_user,
                     phone=Register.Phone(), password="1234567a", password_confirm="1234567a")
        Register.Check(self, check_temp="//li[contains(text(),'Пользователь с таким E-Mail уже существует')]")
        Register.tearDown(self)

# Кейс на проверку регистрации c незаполненной формой регистрации
    def test_8(self):
        Register.Reg(self, name="", surname="", mail="", phone="", password="", password_confirm="")
        elem = self.wd.find_element_by_xpath("//body/div[1]/div[1]/div[2]/form[1]/div[1]/input[1]")
        self.wd.execute_script('arguments[0].removeAttribute("required")', elem)
        elem = self.wd.find_element_by_xpath("//body/div[1]/div[1]/div[2]/form[1]/div[2]/input[1]")
        self.wd.execute_script('arguments[0].removeAttribute("required")', elem)
        elem = self.wd.find_element_by_xpath("//body/div[1]/div[1]/div[2]/form[1]/div[3]/input[1]")
        self.wd.execute_script("arguments[0].type = 'text';", elem)
        elem = self.wd.find_element_by_xpath("//body/div[1]/div[1]/div[2]/form[1]/div[3]/input[1]")
        self.wd.execute_script('arguments[0].removeAttribute("required")', elem)
        elem = self.wd.find_element_by_xpath("//body/div[1]/div[1]/div[2]/form[1]/div[4]/input[1]")
        self.wd.execute_script('arguments[0].removeAttribute("required")', elem)
        elem = self.wd.find_element_by_xpath("//body/div[1]/div[1]/div[2]/form[1]/div[5]/input[1]")
        self.wd.execute_script('arguments[0].removeAttribute("required")', elem)
        elem = self.wd.find_element_by_xpath("//body/div[1]/div[1]/div[2]/form[1]/div[6]/input[1]")
        self.wd.execute_script('arguments[0].removeAttribute("required")', elem)
        self.wd.find_element_by_xpath("//button[contains(text(),'Регистрация')]").click()
        self.wd.find_elements_by_xpath("//li")
        Register.tearDown(self)

if __name__ == "__main__":
    unittest.main()

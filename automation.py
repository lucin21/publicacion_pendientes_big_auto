from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from explicity_wait import ExplicitWaitType
from selenium.webdriver.common.keys import Keys
from escribir_archivo import Escribir_informacion


class Automation(Escribir_informacion):
    def __init__(self):
        self.titulo = "No se encontró una categoría acorde al título de la publicación."
        self.precio = "El precio debe ser mayor o igual a 35."
        self.modelo = "El atributo Modelo es obligatorio."
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.baseUrl = "https://ecommerce.bigauto.solutionslion.com/items?estado=no_publicar&perPage=5"
        self.driver.get(self.baseUrl)
        self.driver.implicitly_wait(0.7)
        self.wait = ExplicitWaitType(self.driver)

    def login(self):
        login_element = self.wait.waitForElement(locator="input-40")
        self.wait.sendKeys("developer@lionintel.com", login_element)
        password_element = self.wait.waitForElement(locator="input-44")
        self.wait.sendKeys("SolutionsLion*", password_element)
        acceder_element = self.wait.waitForElement(
            locator='//*[@id="app"]/div/main/div/div/div[2]/div/div/form/div/div/div[4]/button/span',
            locatorType='xpath')
        self.wait.elementClick(acceder_element)

    def obtener_total_publicaciones(self):
        page_final_element = self.wait.waitForElement(
            locator="#app > div.v-application--wrap > main > div > div > div.container > div.v-card.v-card--flat.v-sheet.theme--light.rounded > header > div > span > span > span",
            locatorType='css')
        page_final = page_final_element.text
        paginas_totales = int(page_final)
        return paginas_totales

    def pagina_actual(self, total):
        self.driver.get(f"https://ecommerce.bigauto.solutionslion.com/items?estado=no_publicar&page={total}&perPage=5")
        total += 1
        return total

    def obtener_informacion(self, n):
        estado_element1 = self.wait.waitForElement(
            locator=f"#app > div.v-application--wrap > main > div > div > div.container > div.v-data-table.mt-5.theme--light > div > table > tbody > tr:nth-child({n}) > td.text-center > span > span",
            locatorType="css")
        if estado_element1.text == "Por corregir":
            numero_parte = self.wait.waitForElement(
                locator=f"#app > div.v-application--wrap > main > div > div > div.container > div.v-data-table.mt-5.theme--light > div > table > tbody > tr:nth-child({n}) > td:nth-child(5)",
                locatorType="css")
            numero_parte = numero_parte.text
            ver_validaciones_element = self.wait.waitForElement(
                locator=f"#app > div.v-application--wrap > main > div > div > div.container > div.v-data-table.mt-5.theme--light > div > table > tbody > tr:nth-child({n}) > td.text-end > button > span",
                locatorType="css")
            self.wait.elementClick(ver_validaciones_element)
            descipcion_element2 = self.wait.waitForElement(
                locator="#app > div.v-dialog__content.v-dialog__content--active > div > div > div > div.v-data-table.mb-5.v-data-table--dense.theme--light > div > table > tbody > tr > td.text-start",
                locatorType='css')
            if descipcion_element2 == None:
                self.escribir("resultados/validacioes_externas", numero_parte)
            else:
                descripcion = descipcion_element2.text
                if descripcion == self.titulo:
                    self.escribir("resultados/categoria_no_acorde_al_titulo", numero_parte)
                elif descripcion == self.precio:
                    self.escribir("resultados/precios_que-deben_ser_mayor_a_35", numero_parte)
                elif descripcion == self.modelo:
                    self.escribir("resultados/atributo_modelo_obligatorio", numero_parte)
                else:
                    self.escribir("resultados/otra descripcion", numero_parte)
        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

    def escribir(self, titulo, numero_parte):
        with open(f"{titulo}.txt", "a") as file:
            file.write(f"{numero_parte}\n")


from automation import Automation
import time

automation = Automation()

automation.login()
time.sleep(2)
paginas_totales = automation.obtener_total_publicaciones()
numero_pagina_actual = automation.pagina_actual(total=1) -1
while paginas_totales >0:
    numero_pagina_actual = automation.pagina_actual(numero_pagina_actual)
    for n in range(1,6):
        automation.obtener_informacion(n)
        paginas_totales -= 1
        if paginas_totales == 0:
            break
        print(paginas_totales)
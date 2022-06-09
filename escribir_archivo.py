class Escribir_informacion:
    def escribir(self, titulo, numero_parte):
        with open(f"{titulo}.txt", "a") as file:
            file.write(f"{numero_parte}\n")

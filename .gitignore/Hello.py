def saludar():
    print("¡Hola, mundo!")

def interaccion():
    respuesta = input("Di algo: ")
    if respuesta.lower() == "hola":
        print("¡Hola! ¡Qué gusto saludarte!")
    else:
        print("Sé un poco más educado...")

if __name__ == "__main__":
    interaccion()

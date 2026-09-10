def calcular_resistencias(Vin, I, Vout):

    R2 = Vout / I
    R1 = (Vin - Vout) / I

    P1 = I**2 * R1
    P2 = I**2 * R2

    if P1 <= 0.25:
        potencia_R1 = "1/4 W"
    elif P1 <= 0.5:
        potencia_R1 = "1/2 W"
    else:
        potencia_R1 = "1 W"

    if P2 <= 0.25:
        potencia_R2 = "1/4 W"
    elif P2 <= 0.5:
        potencia_R2 = "1/2 W"
    else:
        potencia_R2 = "1 W"

    resultados = [R1, R2, potencia_R1, potencia_R2]

    return resultados



while True:
    voltaje_in = input("\n°ingrese su voltaje inicial (Vin)\n\n")
    if voltaje_in.isdigit():
        Vin = float(voltaje_in)
        break
    else:
        print("ingresa una variable valida por favor")

while True:
    corriente = input("\n°ingrese la corriente (I)\n\n")
    if corriente.isdigit() and corriente != "0":
        I = float(corriente)
        break
    else:
        print("ingresa una variable valida por favor")


while True:
    voltaje_sal = input("\n°ingrese su voltaje de salida (Vout)\n\n")
    if voltaje_sal.isdigit():
        Vout = float(voltaje_sal)
        break
    else:
        print("ingresa una variable valida por favor")


resultado = calcular_resistencias(Vin, I, Vout)


print("\nLista de resultados:")
print(resultado)

print("\nResultados:")
print("R1 =", resultado[0], "ohmios")
print("R2 =", resultado[1], "ohmios")
print("Potencia R1 =", resultado[2])
print("Potencia R2 =", resultado[3])

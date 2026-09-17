Vin = 5
I = 0.0001
resultados = []
cantidad = int(input("¿Cuántos valores de Vout desea ingresar? "))
for i in range(cantidad):

    Vout = float(input("Ingrese el valor de Vout: "))


    while Vout <= 0 or Vout >= 5:
        print("Valor no válido. Vout debe ser mayor que 0 y menor que 5.")
        Vout = float(input("Ingrese nuevamente Vout: "))


    R2 = Vout / I
    R1 = (Vin - Vout) / I

  
    resultados.append([Vout, R1, R2])



print("\nResultados:")

for resultado in resultados:
    print("Vout =", resultado[0], "V")
    print("R1 =", resultado[1], "ohm")
    print("R2 =", resultado[2], "ohm")

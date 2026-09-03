#divisor de voltaje
Vin = float(input("ingrese el voltaje de entrada:"))
R1 = float(input("ingrese R1:"))
watt1 = float(input("ingrese watts resistencia 1:"))
R2 = float(input("ingrese R2:"))
watt2 = float(input("ingrese watts resistencia 2:"))
#calcular la corriente 
def calcular_corriente(Vin, R1, watt1, R2, watt2):
    I = Vin / (R1 + R2)
    P1 = I**2 * R1
    P2 = I**2 * R2
    r1_rango = P1 <= watt1
    r2_rango = P2 <= watt2
    return {

    "corriente": I,
    "r1": P1,
    "r2": P2,
    "PT1": r1_rango,
    "PT2": r2_rango
}
resultado = calcular_corriente(Vin, R1, watt1, R2, watt2)
if resultado["PT1"] and resultado["PT2"]:
    print("Ambas resistencias estan en su rango de potencia.")
else:
    print("Al menos una de las resistencias excede su rango de potencia.")
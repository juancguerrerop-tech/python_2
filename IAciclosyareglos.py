def calcular_resistencias(v_in=5.0, corriente=100e-6):
    """
    Solicita al usuario una cantidad de voltajes de salida (Vout),
    valida los datos y calcula las resistencias R1 y R2.
    Imprime las listas finales junto con sus valores maximos y minimos.
    """
    # 1. Solicitar y validar la cantidad de voltajes
    while True:
        try:
            num_voltajes = int(input("Ingrese la cantidad de voltajes de salida (Vout): "))
            if num_voltajes > 0:
                break
            print("Por favor, ingrese un numero entero mayor a 0.")
        except ValueError:
            print("Entrada no valida. Ingrese un numero entero.")

    lista_r1 = []
    lista_r2 = []

    # Capturar y validar cada valor de Vout
    for i in range(num_voltajes):
        while True:
            try:
                v_out = float(input(f"Ingrese Vout #{i + 1} (en voltios, 0 < Vout < {v_in}V): "))
                if 0 < v_out < v_in:
                    break
                print(f"El voltaje debe ser mayor a 0V y menor a {v_in}V.")
            except ValueError:
                print("Entrada no valida. Ingrese un valor numerico.")

        # Ecuaciones del divisor de tension con corriente fija
        r2 = v_out / corriente
        r1 = (v_in - v_out) / corriente

        lista_r1.append(r1)
        lista_r2.append(r2)

    # 2. Obtener e imprimir valores maximos y minimos
    max_r1, min_r1 = max(lista_r1), min(lista_r1)
    max_r2, min_r2 = max(lista_r2), min(lista_r2)

   
    print("RESULTADOS DEL CALCULO DE RESISTENCIAS")
 
    print(f"R1 -> Maximo: {max_r1:,.2f}  | Minimo: {min_r1:,.2f} ")
    print(f"R2 -> Maximo: {max_r2:,.2f}  | Minimo: {min_r2:,.2f} ")

    return lista_r1, lista_r2

# Ejecucion de la funcion
calcular_resistencias()

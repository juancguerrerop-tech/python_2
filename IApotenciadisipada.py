def evaluar_potencia_resistencias(v_in, r1, p1_max, r2, p2_max):
    """
    Calcula la potencia disipada en dos resistencias en serie y 
    determina si superan su límite permitido.
    """
    r_total = r1 + r2
    i_total = v_in / r_total
    
    # Potencias disipadas: P = I^2 * R
    p1_calc = (i_total ** 2) * r1
    p2_calc = (i_total ** 2) * r2
    
    # Evaluación dentro del rango
    r1_en_rango = p1_calc <= p1_max
    r2_en_rango = p2_calc <= p2_max
    
    return {
        "p1": p1_calc,
        "r1_ok": r1_en_rango,
        "p2": p2_calc,
        "r2_ok": r2_en_rango
    }


# --- Entrada de datos ---
v_in = float(input("Ingrese el voltaje de entrada (Vin en V): "))
r1 = float(input("Ingrese el valor de R1 (en Ω): "))
p1_max = float(input("Potencia máx. de R1 (0.25 para 1/4W, 0.5 para 1/2W, o 1): "))

r2 = float(input("Ingrese el valor de R2 (en Ω): "))
p2_max = float(input("Potencia máx. de R2 (0.25 para 1/4W, 0.5 para 1/2W, o 1): "))

# --- Llamada a la función ---
res = evaluar_potencia_resistencias(v_in, r1, p1_max, r2, p2_max)

# --- Impresión de resultados ---
print("\n--- Resultados ---")

print(f"R1 disipa {res['p1']:.4f} W (Máx: {p1_max} W)")
if res['r1_ok']:
    print("-> R1 está funcionando dentro del rango permitido.")
else:
    print("-> ¡ALERTA! R1 excede la potencia máxima y podría dañarse.")

print(f"R2 disipa {res['p2']:.4f} W (Máx: {p2_max} W)")
if res['r2_ok']:
    print("-> R2 está funcionando dentro del rango permitido.")
else:
    print("-> ¡ALERTA! R2 excede la potencia máxima y podría dañarse.")

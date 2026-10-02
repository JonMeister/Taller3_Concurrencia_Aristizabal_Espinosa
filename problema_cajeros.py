"""
Taller 3: Concurrencia
Asignatura: Infraestructuras Paralelas y Distribuidas
Universidad del Valle

Problema: Simulación de retiros concurrentes en cajeros automáticos.
Varios cajeros intentan modificar el saldo de una cuenta bancaria a la vez.
Cada cajero se simula mediante un hilo (Thread) y la cuenta representa la memoria compartida.
Se utiliza un cerrojo (Lock) para garantizar la exclusión mutua y evitar condiciones de carrera.
"""

import threading
import time

# Cerrojo para controlar el acceso a la sección crítica (memoria compartida)
lock = threading.Lock()


def cuenta(id_cajero, saldo_a_retirar):
    """
    Función que ejecuta cada hilo (cajero).
    Modifica el saldo global de la cuenta asegurando que solo un hilo
    acceda a la vez a la sección crítica.
    """
    global saldo_actual

    # SECCIÓN CRÍTICA:
    # Solo 1 cajero puede verificar y modificar el saldo a la vez.
    # De lo contrario, dos cajeros podrían leer el mismo saldo y causar inconsistencias.
    with lock:
        print(f"[Cajero {id_cajero}] Solicitando retiro de: ${saldo_a_retirar:,}")
        time.sleep(0.05)  # Simula el tiempo que tarda el cajero en comunicarse y procesar

        # Verificamos si hay saldo suficiente para este retiro específico
        if saldo_actual < saldo_a_retirar:
            print(f"  -> [Cajero {id_cajero}] Error: Saldo insuficiente. Saldo disponible: ${saldo_actual:,}\n")
        else:
            saldo_actual -= saldo_a_retirar
            print(f"  -> [Cajero {id_cajero}] Retiro exitoso. Saldo restante en la cuenta: ${saldo_actual:,}\n")


if __name__ == "__main__":
    # Saldo inicial de la cuenta compartida
    saldo_actual = 1_000_000

    # Definimos un caso de prueba con 4 cajeros y montos definidos
    # El total solicitado ($1,200,000) supera el saldo inicial ($1,000,000)
    # para demostrar que el control de concurrencia protege la cuenta de quedar en números negativos.
    montos = [300_000, 400_000, 200_000, 300_000]
    total_solicitado = sum(montos)

    print("=" * 65)
    print("  SIMULACIÓN CONCURRENTE: RETIROS EN CAJEROS AUTOMÁTICOS")
    print(f"  Saldo inicial en la cuenta: ${saldo_actual:,}")
    print(f"  Total solicitado a retirar: ${total_solicitado:,}")
    print("=" * 65)

    for i, monto in enumerate(montos, 1):
        print(f"Cajero {i} preparado para retirar: ${monto:,}")

    print("\n--- INICIANDO TRANSACCIONES CONCURRENTES (HILOS) ---\n")

    # Creamos un hilo por cada cajero
    cajeros = [
        threading.Thread(target=cuenta, args=(i, monto))
        for i, monto in enumerate(montos, 1)
    ]

    # Iniciamos todos los cajeros
    for cajero in cajeros:
        cajero.start()

    # Esperamos a que todos los cajeros terminen sus operaciones
    for cajero in cajeros:
        cajero.join()

    print("--- TODAS LAS TRANSACCIONES HAN FINALIZADO ---\n")
    print(f"Saldo final que queda en la cuenta: ${saldo_actual:,}")
    print("=" * 65)

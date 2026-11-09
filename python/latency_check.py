# ============================================
# TEST DE COMUNICACION EN TIEMPO REAL
# ============================================

import serial
import time

PUERTO_SERIAL = "COM3"  # ⚠️ CAMBIA ESTO
BAUDIOS = 115200

def test_comunicacion():
    print(" TEST DE COMUNICACION EN TIEMPO REAL")
    print("="*50)
    
    try:
        puerto = serial.Serial(PUERTO_SERIAL, BAUDIOS, timeout=1)
        time.sleep(2)
        
        lecturas = 0
        errores = 0
        tiempo_inicio = time.time()
        tiempos_entre_lecturas = []
        ultima_lectura = time.time()
        
        print("Midiendo durante 10 segundos...\n")
        
        while (time.time() - tiempo_inicio) < 10:
            try:
                linea = puerto.readline().decode('utf-8').strip()
                tiempo_actual = time.time()
                delta = tiempo_actual - ultima_lectura
                tiempos_entre_lecturas.append(delta)
                ultima_lectura = tiempo_actual
                lecturas += 1
                
                if lecturas <= 5:
                    print(f"  Lectura #{lecturas}: {linea} ({delta*1000:.1f} ms)")
            except:
                errores += 1
        
        tiempo_total = time.time() - tiempo_inicio
        frecuencia = lecturas / tiempo_total
        promedio_delta = sum(tiempos_entre_lecturas) / len(tiempos_entre_lecturas) if tiempos_entre_lecturas else 0
        
        print("\n" + "="*50)
        print("📊 RESULTADOS DEL TEST")
        print("="*50)
        print(f"  Total de lecturas:     {lecturas}")
        print(f"  Errores:               {errores}")
        print(f"  Tiempo total:          {tiempo_total:.2f} segundos")
        print(f"  Frecuencia:            {frecuencia:.1f} lecturas/segundo")
        print(f"  Tiempo entre lecturas: {promedio_delta*1000:.1f} ms")
        
        if frecuencia >= 15:
            print("\n  ✅ EXCELENTE: Comunicación en tiempo real válida!")
        elif frecuencia >= 10:
            print("\n  ⚠️ ACEPTABLE: Comunicación funcional")
        else:
            print("\n  ❌ LENTO: Revisa la configuración")
        
        puerto.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_comunicacion()

import statistics
import matplotlib.pyplot as plt
import random
import simpy


RANDOM_SEED = 50
MEMORIA_INICIAL = 100
INTERVALO = 10
TIEMPO_EJECUCION = 1
INSTRUCCIONES_POR_TIEMPO = 3
NUM_PROCESOS = [25, 50, 100, 150, 150, 200]

tiempos_promedio = []
desviaciones_estandar = []

class Proceso:

    def __init__ (self, id, env, RAM, cpu):        self.id = id
        self.env = env
        self.tiempo_llegada = env.now
        self.memoria = random.randint(1, 10)
        self.cpu_time = random.expovariate(1.0/10)
        self.RAM = RAM
        self.cpu = cpu
        self.instrucciones = 10*self.cpu_time
        
    def ejecutar(self):
        yield self.env.timeout(random.expovariate(1.0/INTERVALO))
        tiempo_inicio = self.env.now
        
        with self.RAM.get(self.memoria) as req:
        
            yield req
            
            while self.instrucciones > 0:
                
                with self.cpu.request() as req:
                    yield req
                    yield self.env.timeout(TIEMPO_EJECUCION)
                    self.instrucciones -= INSTRUCCIONES_POR_TIEMPO
                    
            self.RAM.put(self.memoria)
        
        tiempo_fin = self.env.now
        tiempo_total = tiempo_fin - tiempo_inicio
        return tiempo_total

def simular(env, RAM, cpu, num_procesos):
    
    tiempos = []
    
    for i in range(num_procesos):
        proceso = Proceso(i, env, RAM, cpu)
        proceso_ejecutar = env.process(ejecutar(self, cpu))
        tiempo_total = yield proceso_ejecutar
        tiempos.append(tiempo_total)
        
    tiempo_promedio = sum(tiempos)/num_procesos
    desviacion_estandar = statistics.stdev(tiempos)
    
    return tiempo_promedio, desviacion_estandar

#Configurar semilla aleatoria
random.seed(RANDOM_SEED)

#Realizar la simulación para diferentes números de procesos
for num_procesos in NUM_PROCESOS:
    env = simpy.Environment()
    RAM = simpy.Container(env, init = MEMORIA_INICIAL, capacity = MEMORIA_INICIAL)
    cpu = simpy.Resource (env, capacity = 1)
    tiempo_promedio, desviacion_estandar = simular(env, RAM, cpu, num_procesos)
    tiempos_promedio.append(tiempo_promedio)
    desviaciones_estandar.append(desviacion_estandar)
    

#Mostrar los resultados
for i, num_procesos in enumerate(NUM_PROCESOS):
    print(f"Simulación con {num_procesos} procesos:")
    print(f"Tiempo promedio: {tiempos_promedio[i]:.2f}")
    print(f"Desviación estándar: {desviaciones_estandar[i]:.2f}")
    
    #Graficar los resultados
    plt.plot(NUM_PROCESOS, tiempos_promedio, "ro-")
    plt.xlabel("Número de procesos")
    plt.ylabel("Tiempo promeido")
    plt.show()
    
'''
    yield proceso.RAM.get(proceso.memoria)
    yield CPU.request()
    yield env.timeout(proceso.cpu_time)
    yield CPU.release()
    proceso.RAM.put(proceso.memoria)
    
#parámetros de la simulación
intervalo = 10
num_procesos = 25

#crear el entorno de la simulación
env = simpy.Environment()

#crear los recursos
RAM = simpy.Container(env, init = 100, capacity = 100)
CPU = simpy.Resource(env, capacity = 1)

#iniciar la llegada de procesos
env.process(llegada_proceso(env, RAM, CPU))

#ejecutar la simulación
env.run(until = 1000)
'''

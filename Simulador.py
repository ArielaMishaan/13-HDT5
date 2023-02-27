import itertools
import random
import simpy
import statistics
import matplotlib.pyplot as plt

RANDOM_SEED = 42
RAM_INICIAL = 100
INTERVALO1 = 10
INTERVALO2 = 5
INTERVALO3 = 1
TIEMPO_EJECUCION = 1
INSTRUCCIONES_POR_TIEMPO = 3
NUM_PROCESOS = [25, 50, 100, 150, 200]
SIM_TIME = 1000            # Simulation time in seconds

tiempos = []
tiempo_llegada = random.expovariate(1.0/INTERVALO)

def proceso(nombre, env, ram, cpu):
    
    #el proceso llega con un número aleatorio de instrucciones en el estado NEW
    tiempo_inicio = env.now
    
    cant_instrucciones = random.randint(1, 10)
    cant_memoria_requerida = random.randint(1, 10)
    
    print(nombre, ' llegando a la memoria RAM en ' , env.now, ' con ' , cant_instrucciones, ' instrucciones.')
    #print(nombre + ' llegando a la memoria RAM en ' + env.now + ' con '+ cant_instrucciones + ' instrucciones')

    with ram.get(cant_instrucciones):

    #ram.get(RAM_INICIAL) as req:
        
        start = env.now


        #pedir memoria para entrar en el estado de READY
        print('El proceso ', nombre, ' tiene ram')
        
        while cant_instrucciones > 0:
            
            with cpu.request() as req:
                
                #obtener la memoria requerida del cpu para entrar en el estado de RUNNING
                yield req
                yield env.timeout(TIEMPO_EJECUCION)
                
                cant_instrucciones -= INSTRUCCIONES_POR_TIEMPO
                waiting_ready = random.randint(1, 2)
                print('El proceso ', nombre, ' tiene cpu')
                
                #si el número al azar es 1, el proceso pasa a la cola de WAITING y hace operaciones de I/O
                if waiting_ready == 1:
                    
                    #luego del determinado tiempo, el proceso regresa al estado de READY y sigue con las instrucciones hasta terminar
                    yield env.timeout(2)

    print('El proceso ', nombre, ' dejó cpu')
        
    ram.put(cant_memoria_requerida)
    fin = env.now
            
    tiempo_total = fin - start
    tiempos.append(tiempo_total)
            
    print('El proceso ', nombre, ' terminó de ser ejecutado en ', tiempo_total, ' unidades de tiempo.\n')
    
def generador_procesos(env, ram, cpu, intervalo, cant_procesos):
    
    #Generar nuevos procesos que lleguen a RAM a pedir memoria
    for i in range (cant_procesos):
        
        yield env.timeout(random.expovariate(1.0/intervalo))
        env.process(proceso('Proceso %d' %i, env, ram, cpu))
        #tiempos.append(tiempo_total)
    
print("\n°°°°°°°°°°°°°°°°°°°° SIMULADOR MEMORIA RAM °°°°°°°°°°°°°°°°°°°° ")
random.seed(RANDOM_SEED)

#Correr la simulación para 25, 50, 100, 150 y 200 procesos (INTERVALO = 10)
tiempos_promedio1 = []
desviaciones_estandar1 = []

for i in NUM_PROCESOS:
    env = simpy.Environment()
    ram = simpy.Container(env, 100, init=100)
    cpu = simpy.Resource(env, 1)
    
    env.process(generador_procesos(env, ram, cpu, INTERVALO1, i))
    env.run()
    
    #cálculo tiempo promedio y desviación estándar
    print("\nTIEMPO PROMEDIO DE EJECUCIÓN DE LOS PROCESOS: ")
    tiempo_promedio = statistics.mean(tiempos)
    tiempos_promedio1.append(tiempo_promedio)
    print(tiempo_promedio)

    print("\nDESVIACIÓN ESTÁNDAR DEL TIEMPO DE EJECUCIÓN DE LOS PROCESOS: ")
    desviacion_estandar = statistics.stdev(tiempos)
    desviaciones_estandar1.append(desviacion_estandar)
    print(desviacion_estandar)
    
    #reiniciar lista de tiempos
    tiempos = []
    
    print("\n\nTIEMPOS PROMEDIO: ")
    print("-------------------------")
    for i in tiempos_promedio1:
        print(i)
        
    print("\n\nDESVIACIONES ESTÁNDAR: ")
    print("-------------------------")
    for i in desviaciones_estandar1:
        print(i)
        
#Graficar Número de procesos vs tiempo promedio
plt.plot(NUM_PROCESOS, tiempos_promedio1, "ro-")
plt.xlabel("Número de procesos")
plt.ylabel("Tiempo promedio")
plt.show()
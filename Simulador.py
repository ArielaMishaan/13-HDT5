import itertools
import random
import simpy
import statistics
import matplotlib.pyplot as plt

RANDOM_SEED = 42
RAM_INICIAL = 100
INTERVALO = 10
TIEMPO_EJECUCION = 1
INSTRUCCIONES_POR_TIEMPO = 3
NUM_PROCESOS = [25, 50, 100, 150, 200]
SIM_TIME = 1000            # Simulation time in seconds

tiempos = []
tiempos_promedio = []
desviaciones_estandar = []
tiempo_llegada = random.expovariate(1.0/INTERVALO)

def proceso(nombre, env, ram, cpu):
    
    #el proceso llega con un número aleatorio de instrucciones en el estado NEW
    tiempo_inicio = env.now
    
    cant_instrucciones = random.randint(1, 10)
    cant_memoria_requerida = random.randint(1, 10)
    
    print(nombre, ' llegando a la memoria RAM en ' , env.now, ' con ' , cant_instrucciones, ' instrucciones.')
    #print(nombre + ' llegando a la memoria RAM en ' + env.now + ' con '+ cant_instrucciones + ' instrucciones')
    
    with ram.request() as req:
    #ram.get(RAM_INICIAL) as req:
        
        start = env.now
                
        #pedir memoria para entrar en el estado de READY
        yield req
        
        while cant_instrucciones > 0:
            
            with cpu.get(cant_instrucciones) as req:
                
                #obtener la memoria requerida del cpu para entrar en el estado de RUNNING
                yield req
                yield env.timeout(TIEMPO_EJECUCION)
                
                cant_instrucciones -= INSTRUCCIONES_POR_TIEMPO
                waiting_ready = random.randint(1, 2)
                
                #si el número al azar es 1, el proceso pasa a la cola de WAITING y hace operaciones de I/O
                if waiting_ready == 1:
                    
                    #luego del determinado tiempo, el proceso regresa al estado de READY y sigue con las instrucciones hasta terminar
                    yield env.timeout(2)
        
    ram.put(cant_memoria_requerida)
    fin = env.now
            
    tiempo_total = start - fin
            
    print('El proceso ', nombre, ' terminó de ser ejecutado en ', tiempo_total, ' unidades de tiempo.')
    
def generador_procesos(env, ram, cpu):
    
    #Generar nuevos procesos que lleguen a RAM a pedir memoria
    for i in range (25):
        
        yield env.timeout(random.expovariate(1.0/INTERVALO))
        env.process(proceso('Proceso %d' %i, env, ram, cpu))
        #tiempos.append(tiempo_total)
    
print("\n°°°°°°°°°°°°°°°°°°°° SIMULADOR MEMORIA RAM °°°°°°°°°°°°°°°°°°°° ")
random.seed(RANDOM_SEED)

#crear el ambiente y comenzar los procesos
env = simpy.Environment()
ram = simpy.Resource(env, 1)
cpu = simpy.Container(env, 1, init = 1)
env.process(generador_procesos(env, ram, cpu))

#ejecutar
env.run()

#cálculo tiempo promedios
    
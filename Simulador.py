
 #Alina Carías (22539), Ignacio Méndez (22613), Ariela Mishaan (22052), Diego Soto (22737)
 #Algoritmos y Estructuras de Datos Sección 40
 #Hoja de Trabajo 5
 #27-02-2023
 


import itertools
import random
import simpy
import statistics
import matplotlib.pyplot as plt

RANDOM_SEED = 42
RAM_INICIAL = 100
INTERVALOS = [10, 5, 1]
TIEMPO_EJECUCION = 1
INSTRUCCIONES_POR_TIEMPO1 = 3
INSTRUCCIONES_POR_TIEMPO2 = 6
NUM_PROCESOS = [25, 50, 100, 150, 200]
SIM_TIME = 1000            # Simulation time in seconds

lista_listas_tiemposPromedio_Intervalos10 = []
lista_listas_tiemposPromedio_Intervalos5 = []
lista_listas_tiemposPromedio_Intervalos1 = []

intervalo_10_normal = []
intervalo_10_RAM_200 = []
intervalo_10_6_IPM = []
intervalo_10_2CPU = []

intervalo_5_normal = []
intervalo_5_RAM_200 = []
intervalo_5_6_IPM = []
intervalo_5_2CPU = []

intervalo_1_normal = []
intervalo_1_RAM_200 = []
intervalo_1_6_IPM = []
intervalo_1_2CPU = []

'''DEFINICIÓN DE LOS PROCESOS Y FUNCIONES '''

def proceso(nombre, env, ram, cpu, instrucciones_por_tiempo):
    
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
                
                cant_instrucciones -= instrucciones_por_tiempo
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
    
def generador_procesos(env, ram, cpu, intervalo, cant_procesos, instrucciones_por_tiempo):
    
    #Generar nuevos procesos que lleguen a RAM a pedir memoria
    for i in range (cant_procesos):
        
        yield env.timeout(random.expovariate(1.0/intervalo))
        env.process(proceso('Proceso %d' %i, env, ram, cpu, instrucciones_por_tiempo))
        #tiempos.append(tiempo_total)
        
        
''' EJECUCIÓN DEL PROGRAMA '''

continuar = True

while continuar == True:
    
    random.seed(RANDOM_SEED)

    #Menú
    print("\n°°°°°°°°°°°°°°°°°°°° SIMULADOR MEMORIA RAM °°°°°°°°°°°°°°°°°°°° ")
    print("\n1. Simular tiempo de ejecución con 25, 50, 100, 150 y 200 procesos y cambiar de intervalos.")
    print("2. Simular tiempos de ejecución, incrementando memoria RAM de 100 a 200.")
    print("3. Simular tiempos de ejecución con un procesador más rápido (6 instrucciones por unidad de tiempo en vez de 3)")
    print("4. Simular tiempos de ejecución con 2 procesadores.")
    print("5. Salir.")

    print("\n6. Ver graficado todo junto.")
    
    decision = input("\nEscoja una opción: ")
    
    if decision == "1": #Simular tiempos de ejecución cambiando de intervalos
        
        continuar2 = True
        while continuar2 == True:
            
            print("\n1. Simular tiempos de ejecución con intervalo = 10")
            print("2. Simular tiempos de ejecución con intervalo = 5")
            print("3. Simular tiempos de ejecución con intervalo = 1")
            print("4. Salir de esta sección")
            
            decision2 = input("\nEscoja una opción: ")
            
            if decision2 == "1": #intervalo = 10
                
                tiempos_promedio = []
                desviaciones_estandar = []
                tiempos = []

                for i in NUM_PROCESOS:
                    env = simpy.Environment()
                    ram = simpy.Container(env, 100, init=100)
                    cpu = simpy.Resource(env, 1)
                    
                    env.process(generador_procesos(env, ram, cpu, INTERVALOS[0], i, INSTRUCCIONES_POR_TIEMPO1))
                    env.run()
                    
                    #cálculo tiempo promedio y desviación estándar
                    print("\nTIEMPO PROMEDIO DE EJECUCIÓN DE LOS PROCESOS: ")
                    tiempo_promedio = statistics.mean(tiempos)
                    tiempos_promedio.append(tiempo_promedio)
                    print(tiempo_promedio)

                    print("\nDESVIACIÓN ESTÁNDAR DEL TIEMPO DE EJECUCIÓN DE LOS PROCESOS: ")
                    desviacion_estandar = statistics.stdev(tiempos)
                    desviaciones_estandar.append(desviacion_estandar)
                    print(desviacion_estandar)
                    
                    print("\n\nTIEMPOS PROMEDIO: ")
                    print("-------------------------")
                    for i in tiempos_promedio:
                        print(i)
                        
                    print("\n\nDESVIACIONES ESTÁNDAR: ")
                    print("-------------------------")
                    for i in desviaciones_estandar:
                        print(i)

                lista_listas_tiemposPromedio_Intervalos10.append(tiempos_promedio)
                intervalo_10_normal = tiempos_promedio       

                #Graficar Número de procesos vs tiempo promedio
                plt.plot(NUM_PROCESOS, tiempos_promedio, "ro-", color = "green")
                plt.xlabel("Número de procesos")
                plt.ylabel("Tiempo promedio")
                plt.suptitle("Tiempo promedio de ejecución vs Núm. procesos")
                plt.title("Intervalos de 10")
                plt.show()
                
            elif decision2 == "2": #intervalo = 5
                
                tiempos_promedio = []
                desviaciones_estandar = []
                tiempos = []

                for i in NUM_PROCESOS:
                    env = simpy.Environment()
                    ram = simpy.Container(env, 100, init=100)
                    cpu = simpy.Resource(env, 1)
                    
                    env.process(generador_procesos(env, ram, cpu, INTERVALOS[1], i, INSTRUCCIONES_POR_TIEMPO1))
                    env.run()
                    
                    #cálculo tiempo promedio y desviación estándar
                    print("\nTIEMPO PROMEDIO DE EJECUCIÓN DE LOS PROCESOS: ")
                    tiempo_promedio = statistics.mean(tiempos)
                    tiempos_promedio.append(tiempo_promedio)
                    print(tiempo_promedio)

                    print("\nDESVIACIÓN ESTÁNDAR DEL TIEMPO DE EJECUCIÓN DE LOS PROCESOS: ")
                    desviacion_estandar = statistics.stdev(tiempos)
                    desviaciones_estandar.append(desviacion_estandar)
                    print(desviacion_estandar)
                    
                    print("\n\nTIEMPOS PROMEDIO: ")
                    print("-------------------------")
                    for i in tiempos_promedio:
                        print(i)
                        
                    print("\n\nDESVIACIONES ESTÁNDAR: ")
                    print("-------------------------")
                    for i in desviaciones_estandar:
                        print(i)

                lista_listas_tiemposPromedio_Intervalos5.append(tiempos_promedio)
                intervalo_5_normal = tiempos_promedio               

                #Graficar Número de procesos vs tiempo promedio
                plt.plot(NUM_PROCESOS, tiempos_promedio, "ro-", color = "green")
                plt.xlabel("Número de procesos")
                plt.ylabel("Tiempo promedio")
                plt.suptitle("Tiempo promedio de ejecución vs Núm. procesos")
                plt.title("Intervalos de 5")
                plt.show()
                
            elif decision2 == "3": #intervalo = 1
                
                tiempos_promedio = []
                desviaciones_estandar = []
                tiempos = []

                for i in NUM_PROCESOS:
                    env = simpy.Environment()
                    ram = simpy.Container(env, 100, init=100)
                    cpu = simpy.Resource(env, 1)
                    
                    env.process(generador_procesos(env, ram, cpu, INTERVALOS[2], i, INSTRUCCIONES_POR_TIEMPO1))
                    env.run()
                    
                    #cálculo tiempo promedio y desviación estándar
                    print("\nTIEMPO PROMEDIO DE EJECUCIÓN DE LOS PROCESOS: ")
                    tiempo_promedio = statistics.mean(tiempos)
                    tiempos_promedio.append(tiempo_promedio)
                    print(tiempo_promedio)

                    print("\nDESVIACIÓN ESTÁNDAR DEL TIEMPO DE EJECUCIÓN DE LOS PROCESOS: ")
                    desviacion_estandar = statistics.stdev(tiempos)
                    desviaciones_estandar.append(desviacion_estandar)
                    print(desviacion_estandar)
                    
                    print("\n\nTIEMPOS PROMEDIO: ")
                    print("-------------------------")
                    for i in tiempos_promedio:
                        print(i)
                        
                    print("\n\nDESVIACIONES ESTÁNDAR: ")
                    print("-------------------------")
                    for i in desviaciones_estandar:
                        print(i)
                
                lista_listas_tiemposPromedio_Intervalos1.append(tiempos_promedio)     
                intervalo_1_normal = tiempos_promedio          

                #Graficar Número de procesos vs tiempo promedio
                plt.plot(NUM_PROCESOS, tiempos_promedio, "ro-", color = "green")
                plt.xlabel("Número de procesos")
                plt.ylabel("Tiempo promedio")
                plt.suptitle("Tiempo promedio de ejecución vs Núm. procesos")
                plt.title("Intervalos de 1")
                plt.show()
                
            elif decision2 == "4": #salir de esta sección
                
                continuar2 = False
                
            else:
                print("Escoja una opción válida.")
        
    elif decision == "2": #Simular tiempos de ejecución incrementando RAM a 200
        
        continuar3 = True
        while continuar3 == True:
            
            print("\nRAM de 200 en vez de 100")
            print("----------------------------------------")
            print("1. Simular tiempos de ejecución con intervalo = 10")
            print("2. Simular tiempos de ejecución con intervalo = 5")
            print("3. Simular tiempos de ejecución con intervalo = 1")
            print("4. Salir de esta sección")
            
            decision3 = input("\nEscoja una opción: ")
            
            if decision3 == "1": #intervalo = 10
                
                tiempos_promedio = []
                desviaciones_estandar = []
                tiempos = []

                for i in NUM_PROCESOS:
                    env = simpy.Environment()
                    ram = simpy.Container(env, 200, init=200)
                    cpu = simpy.Resource(env, 1)
                    
                    env.process(generador_procesos(env, ram, cpu, INTERVALOS[0], i, INSTRUCCIONES_POR_TIEMPO1))
                    env.run()
                    
                    #cálculo tiempo promedio y desviación estándar
                    print("\nTIEMPO PROMEDIO DE EJECUCIÓN DE LOS PROCESOS: ")
                    tiempo_promedio = statistics.mean(tiempos)
                    tiempos_promedio.append(tiempo_promedio)
                    print(tiempo_promedio)

                    print("\nDESVIACIÓN ESTÁNDAR DEL TIEMPO DE EJECUCIÓN DE LOS PROCESOS: ")
                    desviacion_estandar = statistics.stdev(tiempos)
                    desviaciones_estandar.append(desviacion_estandar)
                    print(desviacion_estandar)
                                        
                    print("\n\nTIEMPOS PROMEDIO: ")
                    print("-------------------------")
                    for i in tiempos_promedio:
                        print(i)
                        
                    print("\n\nDESVIACIONES ESTÁNDAR: ")
                    print("-------------------------")
                    for i in desviaciones_estandar:
                        print(i)
                
                lista_listas_tiemposPromedio_Intervalos10.append(tiempos_promedio)  
                intervalo_10_RAM_200 = tiempos_promedio     

                #Graficar Número de procesos vs tiempo promedio
                plt.plot(NUM_PROCESOS, tiempos_promedio, "ro-", color = "blue")
                plt.xlabel("Número de procesos")
                plt.ylabel("Tiempo promedio")
                plt.suptitle("Tiempo promedio de ejecución vs Núm. procesos")
                plt.title("Intervalos de 10 (RAM capacidad 200)")
                plt.show()
                
            elif decision3 == "2": #intervalo = 5
                
                tiempos_promedio = []
                desviaciones_estandar = []
                tiempos = []

                for i in NUM_PROCESOS:
                    env = simpy.Environment()
                    ram = simpy.Container(env, 200, init=200)
                    cpu = simpy.Resource(env, 1)
                    
                    env.process(generador_procesos(env, ram, cpu, INTERVALOS[1], i, INSTRUCCIONES_POR_TIEMPO1))
                    env.run()
                    
                    #cálculo tiempo promedio y desviación estándar
                    print("\nTIEMPO PROMEDIO DE EJECUCIÓN DE LOS PROCESOS: ")
                    tiempo_promedio = statistics.mean(tiempos)
                    tiempos_promedio.append(tiempo_promedio)
                    print(tiempo_promedio)

                    print("\nDESVIACIÓN ESTÁNDAR DEL TIEMPO DE EJECUCIÓN DE LOS PROCESOS: ")
                    desviacion_estandar = statistics.stdev(tiempos)
                    desviaciones_estandar.append(desviacion_estandar)
                    print(desviacion_estandar)
                                        
                    print("\n\nTIEMPOS PROMEDIO: ")
                    print("-------------------------")
                    for i in tiempos_promedio:
                        print(i)
                        
                    print("\n\nDESVIACIONES ESTÁNDAR: ")
                    print("-------------------------")
                    for i in desviaciones_estandar:
                        print(i)
                        
                lista_listas_tiemposPromedio_Intervalos5.append(tiempos_promedio)    
                intervalo_5_RAM_200 = tiempos_promedio  

                #Graficar Número de procesos vs tiempo promedio
                plt.plot(NUM_PROCESOS, tiempos_promedio, "ro-", color = "blue")
                plt.xlabel("Número de procesos")
                plt.ylabel("Tiempo promedio")
                plt.suptitle("Tiempo promedio de ejecución vs Núm. procesos")
                plt.title("Intervalos de 5 (RAM capacidad 200)")
                plt.show()
                                
            elif decision3 == "3": #intervalo = 1
                
                tiempos_promedio = []
                desviaciones_estandar = []
                tiempos = []

                for i in NUM_PROCESOS:
                    env = simpy.Environment()
                    ram = simpy.Container(env, 200, init=200)
                    cpu = simpy.Resource(env, 1)
                    
                    env.process(generador_procesos(env, ram, cpu, INTERVALOS[2], i, INSTRUCCIONES_POR_TIEMPO1))
                    env.run()
                    
                    #cálculo tiempo promedio y desviación estándar
                    print("\nTIEMPO PROMEDIO DE EJECUCIÓN DE LOS PROCESOS: ")
                    tiempo_promedio = statistics.mean(tiempos)
                    tiempos_promedio.append(tiempo_promedio)
                    print(tiempo_promedio)

                    print("\nDESVIACIÓN ESTÁNDAR DEL TIEMPO DE EJECUCIÓN DE LOS PROCESOS: ")
                    desviacion_estandar = statistics.stdev(tiempos)
                    desviaciones_estandar.append(desviacion_estandar)
                    print(desviacion_estandar)
                    
                    #reiniciar lista de tiempos
                    tiempos = []
                    
                    print("\n\nTIEMPOS PROMEDIO: ")
                    print("-------------------------")
                    for i in tiempos_promedio:
                        print(i)
                        
                    print("\n\nDESVIACIONES ESTÁNDAR: ")
                    print("-------------------------")
                    for i in desviaciones_estandar:
                        print(i)
                        
                lista_listas_tiemposPromedio_Intervalos1.append(tiempos_promedio) 
                intervalo_1_RAM_200 = tiempos_promedio      

                #Graficar Número de procesos vs tiempo promedio
                plt.plot(NUM_PROCESOS, tiempos_promedio, "ro-", color = "blue")
                plt.xlabel("Número de procesos")
                plt.ylabel("Tiempo promedio")
                plt.suptitle("Tiempo promedio de ejecución vs Núm. procesos")
                plt.title("Intervalos de 1 (RAM capacidad 200)")
                plt.show()
                
            elif decision3 == "4": #salir de esta sección
                
                continuar3 = False
                
            else:
                print("Escoja una opción válida.")
                
    elif decision == "3": #Simular tiempos de ejecución con procesador más rápido (6 instrucciones por unidad de tiempo) (intervalo = 10)
        
        continuar4 = True
        while continuar4 == True:

            print("\nCapacidad de 6 instrucciones por unidad de tiempo en vez de 3")
            print("----------------------------------------")
            print("\n1. Simular tiempos de ejecución con intervalo = 10")
            print("2. Simular tiempos de ejecución con intervalo = 5")
            print("3. Simular tiempos de ejecución con intervalo = 1")
            print("4. Salir de esta sección")
            
            decision4 = input("\nEscoja una opción: ")

            if decision4 == "1": #intervalo = 10
                
                tiempos_promedio = []
                desviaciones_estandar = []
                tiempos = []

                for i in NUM_PROCESOS:
                    env = simpy.Environment()
                    ram = simpy.Container(env, 100, init=100)
                    cpu = simpy.Resource(env, 1)
                    
                    env.process(generador_procesos(env, ram, cpu, INTERVALOS[0], i, INSTRUCCIONES_POR_TIEMPO2))
                    env.run()
                    
                    #cálculo tiempo promedio y desviación estándar
                    print("\nTIEMPO PROMEDIO DE EJECUCIÓN DE LOS PROCESOS: ")
                    tiempo_promedio = statistics.mean(tiempos)
                    tiempos_promedio.append(tiempo_promedio)
                    print(tiempo_promedio)

                    print("\nDESVIACIÓN ESTÁNDAR DEL TIEMPO DE EJECUCIÓN DE LOS PROCESOS: ")
                    desviacion_estandar = statistics.stdev(tiempos)
                    desviaciones_estandar.append(desviacion_estandar)
                    print(desviacion_estandar)
                    
                    print("\n\nTIEMPOS PROMEDIO: ")
                    print("-------------------------")
                    for i in tiempos_promedio:
                        print(i)
                        
                    print("\n\nDESVIACIONES ESTÁNDAR: ")
                    print("-------------------------")
                    for i in desviaciones_estandar:
                        print(i)
                        
                lista_listas_tiemposPromedio_Intervalos10.append(tiempos_promedio)  
                intervalo_10_6_IPM = tiempos_promedio     

                #Graficar Número de procesos vs tiempo promedio
                plt.plot(NUM_PROCESOS, tiempos_promedio, "ro-", color = "orange")
                plt.xlabel("Número de procesos")
                plt.ylabel("Tiempo promedio")
                plt.suptitle("Tiempo promedio de ejecución vs Núm. procesos")
                plt.title("Intervalos de 10 (6 instrucciones por unidad de tiempo)")
                plt.show()
                
            elif decision4 == "2": #intervalo = 5
                
                tiempos_promedio = []
                desviaciones_estandar = []
                tiempos = []

                for i in NUM_PROCESOS:
                    env = simpy.Environment()
                    ram = simpy.Container(env, 100, init=100)
                    cpu = simpy.Resource(env, 1)
                    
                    env.process(generador_procesos(env, ram, cpu, INTERVALOS[1], i, INSTRUCCIONES_POR_TIEMPO2))
                    env.run()
                    
                    #cálculo tiempo promedio y desviación estándar
                    print("\nTIEMPO PROMEDIO DE EJECUCIÓN DE LOS PROCESOS: ")
                    tiempo_promedio = statistics.mean(tiempos)
                    tiempos_promedio.append(tiempo_promedio)
                    print(tiempo_promedio)

                    print("\nDESVIACIÓN ESTÁNDAR DEL TIEMPO DE EJECUCIÓN DE LOS PROCESOS: ")
                    desviacion_estandar = statistics.stdev(tiempos)
                    desviaciones_estandar.append(desviacion_estandar)
                    print(desviacion_estandar)
                    
                    print("\n\nTIEMPOS PROMEDIO: ")
                    print("-------------------------")
                    for i in tiempos_promedio:
                        print(i)
                        
                    print("\n\nDESVIACIONES ESTÁNDAR: ")
                    print("-------------------------")
                    for i in desviaciones_estandar:
                        print(i)
                        
                lista_listas_tiemposPromedio_Intervalos5.append(tiempos_promedio) 
                intervalo_5_6_IPM = tiempos_promedio      

                #Graficar Número de procesos vs tiempo promedio
                plt.plot(NUM_PROCESOS, tiempos_promedio, "ro-", color = "orange")
                plt.xlabel("Número de procesos")
                plt.ylabel("Tiempo promedio")
                plt.suptitle("Tiempo promedio de ejecución vs Núm. procesos")
                plt.title("Intervalos de 5 (6 instrucciones por unidad de tiempo)")
                plt.show()
                
            elif decision4 == "3": #intervalo = 1
                
                tiempos_promedio = []
                desviaciones_estandar = []
                tiempos = []

                for i in NUM_PROCESOS:
                    env = simpy.Environment()
                    ram = simpy.Container(env, 100, init=100)
                    cpu = simpy.Resource(env, 1)
                    
                    env.process(generador_procesos(env, ram, cpu, INTERVALOS[2], i, INSTRUCCIONES_POR_TIEMPO2))
                    env.run()
                    
                    #cálculo tiempo promedio y desviación estándar
                    print("\nTIEMPO PROMEDIO DE EJECUCIÓN DE LOS PROCESOS: ")
                    tiempo_promedio = statistics.mean(tiempos)
                    tiempos_promedio.append(tiempo_promedio)
                    print(tiempo_promedio)

                    print("\nDESVIACIÓN ESTÁNDAR DEL TIEMPO DE EJECUCIÓN DE LOS PROCESOS: ")
                    desviacion_estandar = statistics.stdev(tiempos)
                    desviaciones_estandar.append(desviacion_estandar)
                    print(desviacion_estandar)
                    
                    print("\n\nTIEMPOS PROMEDIO: ")
                    print("-------------------------")
                    for i in tiempos_promedio:
                        print(i)
                        
                    print("\n\nDESVIACIONES ESTÁNDAR: ")
                    print("-------------------------")
                    for i in desviaciones_estandar:
                        print(i)
                        
                lista_listas_tiemposPromedio_Intervalos1.append(tiempos_promedio) 
                intervalo_1_6_IPM = tiempos_promedio      

                #Graficar Número de procesos vs tiempo promedio
                plt.plot(NUM_PROCESOS, tiempos_promedio, "ro-", color = "orange")
                plt.xlabel("Número de procesos")
                plt.ylabel("Tiempo promedio")
                plt.suptitle("Tiempo promedio de ejecución vs Núm. procesos")
                plt.title("Intervalos de 1 (6 instrucciones por unidad de tiempo)")
                plt.show()
                
            elif decision4 == "4": #salir de esta sección
                
                continuar4 = False
                
            else:
                print("Escoja una opción válida.")
                   
    elif decision == "4": #Simular tiempos de ejecución con 2 procesadores (intervalo = 10)
        
        continuar5 = True   
        while continuar5 == True:

            print("\n2 Procesadores en vez de 1")
            print("----------------------------------------")
            print("\n1. Simular tiempos de ejecución con intervalo = 10")
            print("2. Simular tiempos de ejecución con intervalo = 5")
            print("3. Simular tiempos de ejecución con intervalo = 1")
            print("4. Salir de esta sección")
            
            decision5 = input("\nEscoja una opción: ")
            
            if decision5 == "1": #intervalo = 10
                
                tiempos_promedio = []
                desviaciones_estandar = []
                tiempos = []

                for i in NUM_PROCESOS:
                    env = simpy.Environment()
                    ram = simpy.Container(env, 100, init=100)
                    cpu = simpy.Resource(env, 2)
                    
                    env.process(generador_procesos(env, ram, cpu, INTERVALOS[0], i, INSTRUCCIONES_POR_TIEMPO1))
                    env.run()
                    
                    #cálculo tiempo promedio y desviación estándar
                    print("\nTIEMPO PROMEDIO DE EJECUCIÓN DE LOS PROCESOS: ")
                    tiempo_promedio = statistics.mean(tiempos)
                    tiempos_promedio.append(tiempo_promedio)
                    print(tiempo_promedio)

                    print("\nDESVIACIÓN ESTÁNDAR DEL TIEMPO DE EJECUCIÓN DE LOS PROCESOS: ")
                    desviacion_estandar = statistics.stdev(tiempos)
                    desviaciones_estandar.append(desviacion_estandar)
                    print(desviacion_estandar)
                    
                    print("\n\nTIEMPOS PROMEDIO: ")
                    print("-------------------------")
                    for i in tiempos_promedio:
                        print(i)
                        
                    print("\n\nDESVIACIONES ESTÁNDAR: ")
                    print("-------------------------")
                    for i in desviaciones_estandar:
                        print(i)
                        
                lista_listas_tiemposPromedio_Intervalos10.append(tiempos_promedio)  
                intervalo_10_2CPU = tiempos_promedio     

                #Graficar Número de procesos vs tiempo promedio
                plt.plot(NUM_PROCESOS, tiempos_promedio, "ro-", color = "purple")
                plt.xlabel("Número de procesos")
                plt.ylabel("Tiempo promedio")
                plt.suptitle("Tiempo promedio de ejecución vs Núm. procesos")
                plt.title("Intervalos de 10 (2 procesadores)")
                plt.show()
                
            elif decision5 == "2": #intervalo = 5
                
                tiempos_promedio = []
                desviaciones_estandar = []
                tiempos = []

                for i in NUM_PROCESOS:
                    env = simpy.Environment()
                    ram = simpy.Container(env, 100, init=100)
                    cpu = simpy.Resource(env, 2)
                    
                    env.process(generador_procesos(env, ram, cpu, INTERVALOS[1], i, INSTRUCCIONES_POR_TIEMPO1))
                    env.run()
                    
                    #cálculo tiempo promedio y desviación estándar
                    print("\nTIEMPO PROMEDIO DE EJECUCIÓN DE LOS PROCESOS: ")
                    tiempo_promedio = statistics.mean(tiempos)
                    tiempos_promedio.append(tiempo_promedio)
                    print(tiempo_promedio)

                    print("\nDESVIACIÓN ESTÁNDAR DEL TIEMPO DE EJECUCIÓN DE LOS PROCESOS: ")
                    desviacion_estandar = statistics.stdev(tiempos)
                    desviaciones_estandar.append(desviacion_estandar)
                    print(desviacion_estandar)
                    
                    print("\n\nTIEMPOS PROMEDIO: ")
                    print("-------------------------")
                    for i in tiempos_promedio:
                        print(i)
                        
                    print("\n\nDESVIACIONES ESTÁNDAR: ")
                    print("-------------------------")
                    for i in desviaciones_estandar:
                        print(i)
                        
                lista_listas_tiemposPromedio_Intervalos5.append(tiempos_promedio) 
                intervalo_5_2CPU = tiempos_promedio      

                #Graficar Número de procesos vs tiempo promedio
                plt.plot(NUM_PROCESOS, tiempos_promedio, "ro-", color = "purple")
                plt.xlabel("Número de procesos")
                plt.ylabel("Tiempo promedio")
                plt.suptitle("Tiempo promedio de ejecución vs Núm. procesos")
                plt.title("Intervalos de 5 (2 procesadores)")
                plt.show()
                
            elif decision5 == "3": #intervalo = 1
                
                tiempos_promedio = []
                desviaciones_estandar = []
                tiempos = []

                for i in NUM_PROCESOS:
                    env = simpy.Environment()
                    ram = simpy.Container(env, 100, init=100)
                    cpu = simpy.Resource(env, 2)
                    
                    env.process(generador_procesos(env, ram, cpu, INTERVALOS[2], i, INSTRUCCIONES_POR_TIEMPO1))
                    env.run()
                    
                    #cálculo tiempo promedio y desviación estándar
                    print("\nTIEMPO PROMEDIO DE EJECUCIÓN DE LOS PROCESOS: ")
                    tiempo_promedio = statistics.mean(tiempos)
                    tiempos_promedio.append(tiempo_promedio)
                    print(tiempo_promedio)

                    print("\nDESVIACIÓN ESTÁNDAR DEL TIEMPO DE EJECUCIÓN DE LOS PROCESOS: ")
                    desviacion_estandar = statistics.stdev(tiempos)
                    desviaciones_estandar.append(desviacion_estandar)
                    print(desviacion_estandar)
                    
                    print("\n\nTIEMPOS PROMEDIO: ")
                    print("-------------------------")
                    for i in tiempos_promedio:
                        print(i)
                        
                    print("\n\nDESVIACIONES ESTÁNDAR: ")
                    print("-------------------------")
                    for i in desviaciones_estandar:
                        print(i)
                        
                lista_listas_tiemposPromedio_Intervalos1.append(tiempos_promedio) 
                intervalo_1_2CPU = tiempos_promedio      

                #Graficar Número de procesos vs tiempo promedio
                plt.plot(NUM_PROCESOS, tiempos_promedio, "ro-", color = "purple")
                plt.xlabel("Número de procesos")
                plt.ylabel("Tiempo promedio")
                plt.suptitle("Tiempo promedio de ejecución vs Núm. procesos")
                plt.title("Intervalos de 1 (2 procesadores)")
                plt.show()
                
            elif decision5 == "4": #salir de esta sección
                
                continuar5 = False
                
            else:
                print("Escoja una opción válida.")
        
    elif decision == "5": #Salir
        continuar = False

    elif decision == "6": #graficar todo junto

        continuar6 = True   
        while continuar6 == True:

            print("\nGráficas")
            print("----------------------------------------")
            print("\n1. Gráficas: ntervalo = 10")
            print("2. Gráficas: intervalo = 5")
            print("3. Gráficas: intervalo = 1")
            print("4. Salir de esta sección")
            decision6 = input("\nEscoja una opción: ")

            if decision6 == "1": #intervalo = 10

                if len(intervalo_10_2CPU) > 0 and len(intervalo_10_normal) > 0 and len(intervalo_10_6_IPM)>0 and len(intervalo_10_RAM_200)>0:

                    #Graficar Número de procesos vs tiempo promedio
                    plt.plot(NUM_PROCESOS, intervalo_10_normal, "ro-", color = "orange", label = "Normal")
                    plt.plot(NUM_PROCESOS, intervalo_10_2CPU, "ro-", color = "blue", label = "2 procesadores")
                    plt.plot(NUM_PROCESOS, intervalo_10_6_IPM, "ro-", color = "green", label = "6 instrucciones por u.t.")
                    plt.plot(NUM_PROCESOS, intervalo_10_RAM_200, "ro-", color = "purple", label = "RAM capacidad 200")

                    plt.xlabel("Número de procesos")
                    plt.ylabel("Tiempo promedio")
                    plt.legend()
                    plt.suptitle("Tiempo promedio de ejecución vs Núm. procesos")
                    plt.title("Intervalos de 10")
                    plt.show()

                else:
                    print("\nNo hay suficientes datos para graficar.")
                
            elif decision6 == "2": #intervalo = 5
                
                if len(intervalo_5_2CPU) > 0 and len(intervalo_5_normal) > 0 and len(intervalo_5_6_IPM)>0 and len(intervalo_5_RAM_200)>0:
                    
                    #Graficar Número de procesos vs tiempo promedio
                    plt.plot(NUM_PROCESOS, intervalo_5_normal, "ro-", color = "orange", label = "Normal")
                    plt.plot(NUM_PROCESOS, intervalo_5_2CPU, "ro-", color = "blue", label = "2 procesadores")
                    plt.plot(NUM_PROCESOS, intervalo_5_6_IPM, "ro-", color = "green", label = "6 instrucciones por u.t.")
                    plt.plot(NUM_PROCESOS, intervalo_5_RAM_200, "ro-", color = "purple", label = "RAM capacidad 200")

                    plt.xlabel("Número de procesos")
                    plt.ylabel("Tiempo promedio")
                    plt.legend()
                    plt.suptitle("Tiempo promedio de ejecución vs Núm. procesos")
                    plt.title("Intervalos de 5")
                    plt.show()
                
                else:
                    print("\nNo hay suficientes datos para graficar.")
                
            elif decision6 == "3": #intervalo = 1

                if len(intervalo_1_2CPU) > 0 and len(intervalo_1_normal) > 0 and len(intervalo_1_6_IPM)>0 and len(intervalo_1_RAM_200)>0:
                
                    #Graficar Número de procesos vs tiempo promedio
                    plt.plot(NUM_PROCESOS, intervalo_1_normal, "ro-", color = "orange", label = "Normal")
                    plt.plot(NUM_PROCESOS, intervalo_1_2CPU, "ro-", color = "blue", label = "2 procesadores")
                    plt.plot(NUM_PROCESOS, intervalo_1_6_IPM, "ro-", color = "green", label = "6 instrucciones por u.t.")
                    plt.plot(NUM_PROCESOS, intervalo_1_RAM_200, "ro-", color = "purple", label = "RAM capacidad 200")

                    plt.xlabel("Número de procesos")
                    plt.ylabel("Tiempo promedio")
                    plt.legend()
                    plt.suptitle("Tiempo promedio de ejecución vs Núm. procesos")
                    plt.title("Intervalos de 1")
                    plt.show()
                
                else:
                    print("\nNo hay suficientes datos para graficar.")

            elif decision6 == "4": #salir de esta sección
                
                continuar6 = False
                
            else:
                print("Escoja una opción válida.")
            
        
    else: 
        print("Escoja una opción válida.")     
        


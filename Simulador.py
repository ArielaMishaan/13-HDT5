import statistics
import matplotlib.pyplot as plt
import random
import simpy

RANDOM_SEED = 42
INTERVALOS = [10, 5, 1]
INSTRUCCIONES_POR_TIEMPO = [3, 4, 5, 6]
NUM_PROCESOS = [25, 50, 100, 150, 200]

class Proceso:

    def __init__ (self, name, env, RAM, cpu_vel):        
        self.env = env
        self.name = name
        self.RAM = RAM
        self.cpu_vel = cpu_vel
        self.memoria = random.randint(1, 10)
        self.tiempo_espera = 0
        self.tiempo_proceso = 0
        self.tiempo_llegada = env.now
        self.cpu_time = random.expovariate(1.0/10)
        
    def ejecutar(self, cpu):

        with cpu.request() as req:
            yield req
            while self.memoria > 0:
                yield self.env.timeout(1/self.cpu_vel)
                self.memoria -= 3
            if self.memoria <= 0:
                if random.random() <= 0.5:
                    self.tiempo_espera -= self.env.now
                    self.env.process(self.io())
                else:
                    self.tiempo_proceso = self.env.now - self.tiempo_llegada

    def io(self):
        with io_request.request() as req:
            yield req
            self.tiempo_espera += self.env.now
            yield self.env.timeout(random.randint(1, 2))
            self.tiempo_espera -= self.env.now
            self.env.process(self.ejecutar(cpu))

def llegada(env, RAM, cpu, io_request):
    i = 0
    while True:
        i += 1
        p = Process(env, f'Process {i}', ram, random.choice(INSTRUCCIONES_POR_TIEMPO))
        env.process(run_process(env, p, cpu, ram, io_request))
        t = random.expovariate(1.0 / INTERVALOS)
        yield env.timeout(t)

def proceso_ejecucion(env, proceso, cpu, ram, io_request):
    with ram.get(process.memoria_req) as req:
        yield req
        yield env.process(process.ejecutar(cpu))
        ram.put(process.memoria_req)

def simular_ejecucion(num_procesos, intervalo, cpu_vel):
    #semilla aleatoria
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    cpu = simpy.Resource(env, capacidad = 1)
    ram = simpy.Container(env, capacidad = 100, init = 100)
    io_request = simpy.Resource(env, capacidad = 1)
    env.process(llegada(env, RAM, cpu, io_request))
    env.ejecutar(until = num_procesos * intervalo)
    tiempos_proceso = [p.tiempo_proceso for p in env.procesos if isinstance(p, Process)]
    tiempo_proceso_promedio = statistics.mean(tiempos_proceso)
    tiempo_proceso_std = statistics.stdev(tiempos_proceso)
    return tiempo_proceso_promedio, tiempo_proceso_std

#Parte A
tiempos_promedio_a = []
tiempos_promedio_std = []
for num_procesos in NUM_PROCESOS:
    tiempo_promedio, tiempo_std = simular_ejecucion(num_procesos, INTERVALOS[0], INSTRUCCIONES_POR_TIEMPO)
    tiempos_promedio_a.append(tiempo_promedio)
    tiempos_promedio_std.append(tiempo_std)
plt.plot(NUM_PROCESOS, tiempos_promedio_std)
plt.xlabel('Número de procesos')
plt.ylabel('Tiempo de proceso promedio')
plt.show()

#Parte B
tiempos_promedio_b
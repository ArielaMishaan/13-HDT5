import itertools
import random
import simpy

env = simpy.Environment()

RANDOM_SEED = 10
RAM_SIZE = 100
TAMANIO_RECURSO_CPU = 3                                    #tiene que ser variable
RAPIDEZ_CPU = 1                                            #CPU realiza 1 proceso en 1 unidad de tiempo
LLEGADA_PROCESOS = random.expovariate(1.0 / 10)            #llegada de procesos sigue una distribución exponencial con con intervalo 10
SIM_TIME = 1000                                            # Simulation time in seconds
CANT_MEMORIA_PROCESO = [1, 10]
INSTRUCCIONES_PROCESO = [1, 10]

def proceso(nombre, env, ram, cpu):
    '''
    Llega un proceso a RAM para realizarse. Pide de primero la asignación de RAM.
    Luego espera la atención del CPU. Si el CPU tiene otro proceso, entonces el nuevo
    tiene que esperar a que el CPU termine. 
    '''
    
    cant_instrucciones_proceso = random.randint(*INSTRUCCIONES_PROCESO) 
    print("%s llegando a la memoria RAM en la unidad de tiempo %.1f" % (nombre, env.now))
    
    with ram.request() as req:
        start = env.now
        
        #pedir un espacio en la RAM
        yield req
        
        #Obtener la atención del cpu por el tiempo necesario
        #????
        
        #Tiempo que tarda cada instrucción
        yield env.timeout(cant_instrucciones_proceso)
        
        print("%s terminó de ser atendido por la RAM en %.1f segundos" % (nombre, env.now - start))
        
def control_ram(env, cpu):
    '''
    Periódicamente se chequea el la cantidad de espacios disponibles del cpu y se llama al
    RAM si se acaba el espacio
    '''
    
    while True:
        if cpu.level < 1:
        

'''

def gas_station_control(env, fuel_pump):
    while True:
        if fuel_pump.level / fuel_pump.capacity * 100 < THRESHOLD:
            # We need to call the tank truck now!
            print('Calling tank truck at %d' % env.now)
            # Wait for the tank truck to arrive and refuel the station
            yield env.process(tank_truck(env, fuel_pump))

        yield env.timeout(10)  # Check every 10 seconds


def tank_truck(env, fuel_pump):
    """Arrives at the gas station after a certain delay and refuels it."""
    yield env.timeout(TANK_TRUCK_TIME)
    print('Tank truck arriving at time %d' % env.now)
    ammount = fuel_pump.capacity - fuel_pump.level
    print('Tank truck refuelling %.1f liters.' % ammount)
    yield fuel_pump.put(ammount)


def car_generator(env, gas_station, fuel_pump):
    """Generate new cars that arrive at the gas station."""
    for i in itertools.count():
        yield env.timeout(random.randint(*T_INTER))
        env.process(car('Car %d' % i, env, gas_station, fuel_pump))


# Setup and start the simulation
print('Gas Station refuelling')
random.seed(RANDOM_SEED)

# Create environment and start processes
env = simpy.Environment()
gas_station = simpy.Resource(env, 2)
fuel_pump = simpy.Container(env, GAS_STATION_SIZE, init=GAS_STATION_SIZE)
env.process(gas_station_control(env, fuel_pump))
env.process(car_generator(env, gas_station, fuel_pump))

# Execute!
env.run(until=SIM_TIME)

'''
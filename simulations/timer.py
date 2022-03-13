from time import time


class Timer:
    def __init__(self, title):
        self.title = title
    def __enter__(self):
        self.start = time()
    def __exit__(self, type, value, traceback):
        self.end = time()
        print(f"###### {self.title}: {self.end - self.start} ######")


if __name__ == "__main__":
    from simulation import Simulation, VectorizedSimulation, BatchSimulation
    from config import update_config
    
    update_config(max_number_of_scenarios=10000)

    with Timer("Simulation"):
        sim = Simulation().get_prices()

    with Timer("VectorizedSimulation"):
        sim = VectorizedSimulation().get_prices()

    with Timer("BatchSimulation"):
        sim = BatchSimulation().get_prices()

#    print("++++++++++++++++++++++++++++++++++++++++++++++++")
#
#    sim=Simulation()
#    with Timer("Simulation"):
#        sim.get_prices()
#
#    sim = VectorizedSimulation()
#    with Timer("VectorizedSimulation"):
#        sim.get_prices()
#
#    sim = BatchSimulation()
#    with Timer("BatchSimulation"):
#        sim.get_prices()

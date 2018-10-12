# Project: Herd Immunity
# Name: Thomas J. Lee

import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus

class Simulation(object):
    # * Main class that will run the herd immunity simulation program.  Expects initialization
    # * parameters passed as command line arguments when file is run.

    # * Simulates the spread of a virus through a given population.  The percentage of the
    # * population that are vaccinated, the size of the population, and the amount of initially
    # * infected people in a population are all variables that can be set when the program is run.

    simulation = Simulation(1000, 0.5, 'AIDS', 0.5)

    def __init__(self, population_size, vacc_percentage, initial_infected=1,virus_name, mortality_rate, repro_rate):
        self.population_size = population_size
        self.population = []

        self.total_infected = 0
        self.current_infected = 0
        self.initial_infected = initial_infected

        self.next_person_id = 0
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            virus_name, population_size, vacc_percentage, initial_infected)

        self.newly_infected = []

        # * Creating Virus object
        self.virus = Virus(virus_name, mortality_rate, repro_rate)

        # * Create a Logger object and bind it to self.logger.  
        self.logger = Logger(self.file_name)

        # * Setting a survive_infection attribute 
        self.survive_infection = person.did_survive_infection(self.virus.mortality_rate)

        # * Setting is_alive from Person class to self
        self.person_is_alive = person.is_alive
        


    def _create_population(self, initial_infected, population_size):
        # * Call this method to populate the "population". 
        # * This method will return an array of Person objects in the population.

        population = []
        infected_count = 0
        while len(population) != population_size:
            if infected_count !=  initial_infected:
                # * Creating a infected_person object with initialised virus object and appending it 
                # * to the population.

                infected_person = Person(self.next_person_id, False, self.virus)
                self.next_person_id += 1 
                population.append(infected_person)
                infected_count += 1
                
            else:
                # * For every new non-infected person, generate a random number between 0 & 1. 
                # * If this number is smaller than vacc_percentage, this person should be instantiated
                # * as a vaccinated one. Else, this person is unvaccinated.

                survival_rate = randint(0,1)
                if survival_rate < vacc_percentage:
                    not_infected_person = Person(self.next_person_id, True)
                    self.next_person_id += 1
                else:
                    not_infected_person = Person(self.next_person_id, False)
                    self.next_person_id += 1
                population.append(not_infected_person)
                
        return population

    def _simulation_should_continue(self):
        # * While the simulation continues, it should return True (False if it doesn't). 
        # * The simulation will end only if:
        # *     - The entire population is dead.
        # *     - There are no more infected people.
        infected_counter = 0
        dead_counter = 0
        simulation_status = True

        for person_obj in self.population:
            if person_obj.infected is not None:
                infected_counter += 1
            if person_obj.is_alive == False:
                dead_counter += 1
      
        while simulation_status:
            for person_obj in self.population:
                if dead_counter == len(self.population) or infected_counter == 0:
                    simulation_status = False
        return simulation_status

    def run(self):
        # * This method will run the simulation until everyone is dead or the virus no 
        # * longer exists.
        # * use the _simulation_should_continue() helper method to know whether or not 
        # * we should continue the simulation and run 1 more time_step.
        # * This method will keep track of the number of time steps that have passed using
        # * the time_step_counter variable. 

        population = self.population
        create_population = self._create_population(self.initial_infected, self.population_size)
        population = create_population

        time_step_counter = 0
        should_continue = self._simulation_should_continue()

        while should_continue:
            # Run simulation and increment time_step_counter.
            self.time_step()
            time_step_counter += 1
            self.logger.log_time_step(time_step_counter)
            should_continue = self._simulation_should_continue()

        print('The simulation has ended after {time_step_counter} turns.'.format(time_step_counter))

    def time_step(self):

        interaction_counter = 1

        for person_obj in self.population:
            # Person must have and infected and be alive.
            if person_obj.infected is not None and person_obj.is_alive == True:
                while interaction_counter <= 100:
                    random_person = random.choice(self.population)
                    # Random person cannot interact with dead people or himself.
                    if random_person.is_alive == False or person_obj._id == random_person._id:
                        random_person = random.choice(self.population)
                    else:
                        self.interaction(person_obj, random_person)
                        interaction_counter += 1

    def interaction(self, person, random_person):
        # * This method will be called any time two living people are selected for an 
        # * interaction. 

        assert person.is_alive == True
        assert random_person.is_alive == True

        # * Cases that need to be covered:
            # * random_person is vaccinated:
            # *    nothing happens to random person.
            # * random_person is already infected:
            # *    nothing happens to random person.
            # * random_person is healthy, but unvaccinated:
            # *    generate a random number between 0 and 1.  If that number is smaller
            # *    than basic_repro_num, random_person's ID should be appended to
            # *    Simulation object's newly_infected array, so that their .infected
            # *    attribute can be changed to True at the end of the time step.

        if random_person.is_vaccinated: 
            self.logger.log_interaction(person, random_person, False, True, False)
        if random_person.infection is not None:
            self.logger.log_interaction(person, random_person, False, False, True)
        else:
            survival_rate =  randint(0,1)
            if survival_num < self.basic_repro_num:
                self.newly_infected.append(person._id)
                self.logger.log_interaction(person, random_person, False, False, False)
    
    def try_and_kill_person(self, person_obj):
        person_obj.did_survive_infection(self.virus.mortality_rate)

    def _infect_newly_infected(self):
        # * This method should be called at the end of
        # * every time step.  This method should iterate through the list stored in
        # * self.newly_infected.
        # * For every person id in self.newly_infected:
        # *  - Find the Person object in self.population that has this corresponding ID.
        # *  - Set this Person's .infected attribute to True.
        person = ''
        for id in self.newly_infected:
            for person_obj in self.population:
                if person_obj._id == id:
                    person.infected = self.virus
                    person = person_obj
        try_and_kill_person(person)
        self.newly_infected = []


if __name__ == "__main__":
    params = sys.argv[1:]
    population_size = int(params[0])
    vacc_percentage = float(params[1])
    virus_name = str(params[2])
    mortality_rate = float(params[3])
    basic_repro_num = float(params[4])
    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1
    simulation = Simulation(population_size, vacc_percentage, virus_name, mortality_rate,
                            basic_repro_num, initial_infected)
    simulation.run()

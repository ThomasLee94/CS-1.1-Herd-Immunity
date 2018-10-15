# Project: Herd Immunity
# Name: Thomas J. Lee

import random, sys
from person import Person
from logger import Logger
from virus import Virus
random.seed(42)

class Simulation(object):
    # * Main class that will run the herd immunity simulation program.  Expects initialization
    # * parameters passed as command line arguments when file is run.

    # * Simulates the spread of a virus through a given population.  The percentage of the
    # * population that are vaccinated, the size of the population, and the amount of initially
    # * infected people in a population are all variables that can be set when the program is run.

    # simulation = Simulation(1000, 0.5, 'AIDS', 0.5)

    def __init__(self, population_size, vacc_percentage,virus_name, mortality_rate, repro_rate, initial_infected=1, dead=0):
        self.population_size = population_size

        self.current_infected = 0
        self.initial_infected = initial_infected
        self.total_infected = self.initial_infected
        self.dead = dead

        self.next_person_id = 0
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            virus_name, population_size, vacc_percentage, initial_infected)

        self.newly_infected = []

        # * Creating Virus object
        self.virus = Virus(virus_name, mortality_rate, repro_rate)

        # * Create a Logger object and bind it to self.logger.  
        self.logger = Logger(self.file_name)

        self.basic_repro_num = repro_rate

        self.population = self._create_population(self.initial_infected, self.population_size)


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
                population.append(infected_person)
                infected_count += 1
                
            else:
                # * For every new non-infected person, generate a random number between 0 & 1. 
                # * If this number is smaller than vacc_percentage, this person should be instantiated
                # * as a vaccinated one. Else, this person is unvaccinated.

                survival_rate = random.uniform(0,1)
                if survival_rate < vacc_percentage:
                    not_infected_person = Person(self.next_person_id, True)
                else:
                    not_infected_person = Person(self.next_person_id, False)
                
                population.append(not_infected_person)
            
            self.next_person_id += 1 
        print("INFECTED COUNT IN CREATE POPULATION: {}".format(infected_count))
        return population

    def _simulation_should_continue(self):
        # * While the simulation continues, it should return True (False if it doesn't). 
        # * The simulation will end only if:
        # *     - The entire population is dead.
        # *     - There are no more infected people.

        simulation_status = True

        for person_obj in self.population:
            if person_obj.infected is not None:
                if not person_obj.did_survive_infection():
                    print('HE DEAD CUZ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1')
                    self.dead+= 1

            # if person_obj.infected is not None and person_obj.is_alive:
            #     self.current_infected += 1

        if self.dead == len(self.population):
            simulation_status = False
        if self.total_infected == 0:
            simulation_status = False
        
        print("Total population: {}".format(len(self.population)))
        print("Total Infected: {}".format(self.total_infected))
        print("Total dead people: {}".format(self.dead))
        print('_________________________________________')

        if simulation_status:
            print("SIMULATION STATUS IS TRUE")
        else:
            print("SIMULATION STATUS IS FALSE")

        return simulation_status

   

    def run(self):
        # * This method will run the simulation until everyone is dead or the virus no 
        # * longer exists.
        # * use the _simulation_should_continue() helper method to know whether or not 
        # * we should continue the simulation and run 1 more time_step.
        # * This method will keep track of the number of time steps that have passed using
        # * the time_step_counter variable. 

        print("run function is running DUDE")

        time_step_counter = 0
        should_continue = self._simulation_should_continue()

        while should_continue:
            # Run simulation and increment time_step_counter.
            self.time_step()
            print("i can run the time_step function DUDE")
            time_step_counter += 1
            self.logger.log_time_step(time_step_counter)
            should_continue = self._simulation_should_continue()

        print('The simulation has ended after {} turns.'.format(time_step_counter))

    def time_step(self):
        # - For each infected person in the population:
        #        - Repeat for 100 total interactions:
        #             - Grab a random person from the population.
        #           - If the person is dead, continue and grab another new
        #                 person from the population. Since we don't interact
        #                 with dead people, this does not count as an interaction.
        #           - Else:
        #               - Call simulation.interaction(person, random_person)
        #               - Increment interaction counter by 1.

        print("time_step function is running DUDE")

        interaction_counter = 1

        encounters = []

        for person_obj in self.population:
            # print("WHY THE FUCK IS MY PERSON NOT INFECTED")
            # * If person is alive and not infected
            print(person_obj.is_alive)
            print(person_obj.infected)
            print('!!!!!!!!!!!!!8888888888888888888888888888!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            if person_obj.infected and person_obj.is_alive:
                # * Condition for 100 interactions
                print('BOBA IS THE BEST')
                while interaction_counter <= 100:
                    # * Picking random person
                    print("****IM IN THE WHILE LOOP****")
                    random_person = random.choice(self.population)
                    # * If random person is not the same as person_obj, random peron is alive and random person is not infected
                    if random_person._id != person_obj._id and random_person.is_alive and random_person.infected == None:
                        print('PEOPLE INTERACTING')
                        self.interaction(person_obj, random_person)
                        encounters.append(random_person)
                        interaction_counter += 1
                    else:
                        random_person = random.choice(self.population)

        self._infect_newly_infected()
                    
    def interaction(self, person_obj, random_person):
        # * This method will be called any time two living people are selected for an 
        # * interaction. 

        assert person_obj.is_alive == True
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
            self.logger.log_interaction(person_obj, random_person, False, True, False)
        if random_person.infected is not None:
            self.logger.log_interaction(person_obj, random_person, False, False, True)
        if random_person.infected is None:
            survival_rate =  random.uniform(0,1)
            if survival_rate < self.basic_repro_num:
                self.newly_infected.append(random_person._id)
                self.logger.log_interaction(person_obj, random_person, False, False, False)

    def _infect_newly_infected(self):
        # * This method should be called at the end of
        # * every time step.  This method should iterate through the list stored in
        # * self.newly_infected.
        # * For every person id in self.newly_infected:
        # *  - Find the Person object in self.population that has this corresponding ID.
        # *  - Set this Person's .infected attribute to True.
        
        for id in self.newly_infected:
            for person_obj in self.population:
                if person_obj._id == id:
                    person_obj.infected = self.virus
                    self.initial_infected += 1
        self.newly_infected = []


if __name__ == "__main__":
    params = sys.argv[1:]
    pop_size = int(params[0])
    vacc_percentage = float(params[1])
    virus_name = str(params[2])
    mortality_rate = float(params[3])
    basic_repro_num = float(params[4])
    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1
    simulation = Simulation(pop_size, vacc_percentage, virus_name, mortality_rate,
                            basic_repro_num, initial_infected)
    simulation.run()


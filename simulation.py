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
        self.next_person_id = 0
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            virus_name, population_size, vacc_percentage, initial_infected)
        self.newly_infected = []

        # * Creating Virus object
        self.virus = Virus(virus_name, mortality_rate, repro_rate)

        # * Create a Logger object and bind it to self.logger.  You should use this
        # * logger object to log all events of any importance during the simulation.  Don't forget
        # * to call these logger methods in the corresponding parts of the simulation!
        self.logger = None

        # This attribute will be used to keep track of all the people that catch
        # the infection during a given time step. We'll store each newly infected
        # person's .ID attribute in here.  At the end of each time step, we'll call
        # self._infect_newly_infected() and then reset .newly_infected back to an empty
        # list.
        self.newly_infected = []
        # TODO: Call self._create_population() and pass in the correct parameters.
        # Store the array that this method will return in the self.population attribute.

    def _create_population(self, initial_infected, pop_size):
        # * Call this method to populate the "population". 
        # * This method will return an array of Person objects in the population.

        population = []
        infected_count = 0
        while len(population) != pop_size:
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
                # ! Whether vaccinated or unvaccinated, I will need to increment self.next_person_id 
                # ! by 1 as each Person object's id has to be unique.

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
        
        for person_obj in self.population:
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
        # ! Use the logger's log_time_step() method at the end of each step and pass in the 
        # ! time_step_counter variable!

        time_step_counter = 0
        should_continue = self._simulation_should_continue()

        while should_continue:

        # TODO: for every iteration of this loop, call self.time_step() to compute another
        # round of this simulation.  At the end of each iteration of this loop, remember
        # to rebind should_continue to another call of self._simulation_should_continue()!
            pass
        print('The simulation has ended after {time_step_counter} turns.'.format(time_step_counter))

    def time_step(self):
        # * This method contains the logic for computing one time step in the simulation.
        # * This includes:
        # *     For each infected person in the population:
        # *        1. Repeat interactions 100 times:
        # *             - Grab a random person from the population. 
        # *        2. IF the person is dead, continue and grab a new person (no interaction 
        # *           between dead people).
        # *        3. ELSE:
        # *             - Call simulation.interaction(person, random_person). 
        # *             - Increment interaction counter by 1.

        for person_obj in self.population:
            if person_obj.infected:


    def interaction(self, person, random_person):
        # * This method will be called any time two living people are selected for an 
        # * interaction. 
        # ! Only living people should be passed into this method.

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
        # ! Remember to call self.logger.log_interaction() during this method!

        if random_person.is_vaccinated:
            self.logger.log_interaction(person, random_person, False, True, False)
        if random_person.infection is not None:
            self.logger.log_interaction(person, random_person, False, False, True)
        else:
            survival_rate =  randint(0,1)
            if survival_num < self.basic_repro_num:
                self.newly_infected.append(person._id)
                self.logger.log_interaction(person, random_person, False, False, False)

    def _infect_newly_infected(self):
        # * This method should be called at the end of
        # * every time step.  This method should iterate through the list stored in
        # * self.newly_infected.
        # * For every person id in self.newly_infected:
        # *  - Find the Person object in self.population that has this corresponding ID.
        # *  - Set this Person's .infected attribute to True.
        # ! Once you have iterated through the entire list of self.newly_infected, remember
        # ! to reset self.newly_infected back to an empty list!

        for id in self.newly_infected:
            for person in self.population:
                if person._id == id:
                    person.infected = self.virus
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

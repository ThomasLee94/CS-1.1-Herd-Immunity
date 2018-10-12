# Project: Herd Immunity
# Name: Thomas J. Lee

import random
from virus import Virus

class Person(object):

    def __init__(self, _id, is_vaccinated, infected=None):
        # * If a person is infected for the first round of simulation, the object
        # * should create a Virus object for self.infection. Otherwise, self.infection
        # * should be set to None.
      
        # * _id, a unique ID assigned to each person.

        # * is_vaccinated: Bool.  Determines whether the person object is vaccinated against
        # * the disease in the simulation.

        # * is_alive: Bool. All person objects begin alive (value set to true).  Changed
        # *  to false if person object dies from an infection.

        # ! infection:  None/Virus object.  Set to None for people that are not infected.
        # ! If a person is infected, will instead be set to the virus object the person
        # ! is infected with.

        self._id = _id
        self.is_vaccinated = is_vaccinated
        self.is_alive = True
        self.infected = infected


    def did_survive_infection(self):
        # * for resolve_infection.  If person dies, set is_alive to False and return False.
        # * If person lives, set is_vaccinated = True, infected = None, return True. 

        survival_rate = random.randint(0,1)
        
        if survival_rate < self.infected.mortality_rate:
            self.is_alive = False
            return False
        else:
            self.is_vaccinated = True
            self.infected = None
            return True
        

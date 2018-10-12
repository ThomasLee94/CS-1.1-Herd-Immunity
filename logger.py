# Project: Herd Immunity
# Name: Thomas J. Lee

class Logger(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.meta_data = open(file_name, "w")

    def write_metadata(self, population_size, vacc_percentage, virus_name, mortality_rate,
                       basic_repro_num):
        # * The simulation class should use this method 
        # * immediately upon creation, to log the specific parameters of the simulation
        # * as the first line of the file.  This line of metadata should be tab-delimited
        # * (each item separated by a '\t' character).
        # * Since this is the first method called, it will create the text file
        # * that we will store all logs in.  Be sure to use 'w' mode when you open the file.
        # * For all other methods, we'll want to use the 'a' mode to append our new log to the end,
        # * since 'w' overwrites the file.
       
        self.meta_data.write("Population size:{} \t Vaccination Percentage:{} \t Virus name:{} \t Mortality Rate:{} \t Basic reproduction number:{}\n"
            .format(population_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num))

    def log_interaction(self, person1, person2, did_infect=None,
                        person2_vacc=None, person2_sick=None):
        # * The Simulation object should use this method to
        # * log every interaction a sick individual has during each time step.  
        # * person1 is the infected person, person2 is the person being chosen for interaction.

        if did_infect is not None:
            self.meta_data.write("{} has infected {}\n".format(person1._id, person2._id))
        else:
            if person2_sick is not None:
                self.meta_data.write("{} is already infected\n".format(person2._id))
            if person2_vacc is not None:
                self.meta_data.write("{} is vaccinated\n".format(person2._id))
            else:
                self.meta_data.write("{} fails to infect {}\n".format(person1._id, person2._id))


    def log_infection_survival(self, person, did_die_from_infection):
        # * The Simulation object should use this method to log
        # * the results of every call of a Person object's .resolve_infection() method.
        # * If the person survives, did_die_from_infection should be False.  Otherwise,
        # * did_die_from_infection should be True.  See the documentation for more details
        # * on the format of the log.
       
        if did_die_from_infection:
            self.meta_data.write("{} died from infection\n".format(person._id))
        if did_die_from_infection is None:
            self.meta_data.write("{} did not get infected\n".format(person._id))
        else:
            self.meta_data.write("{} survived from infection\n".format(person._id))


    def log_time_step(self, time_step_number):
        # * This method should log when a time step ends, and a
        # * new one begins.  See the documentation for more information on the format of the log.
        # * NOTE: Stretch challenge opportunity! Modify this method so that at the end of each time
        # * step, it also logs a summary of what happened in that time step, including the number of
        # * people infected, the number of people dead, etc.  You may want to create a helper class
        # * to compute these statistics for you, as a Logger's job is just to write logs!
       
        self.meta_data.write("Time step has ended at count {}".format(time_step_number))
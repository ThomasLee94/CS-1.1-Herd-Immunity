class Virus(object):

# NOTE # *Properties and Attributes of the virus used in the Simulation

    __init__(self, virus_name, mortality_rate, repro_rate):
        self.virus_name = virus_name
        self.mortality_rate = mortality_rate
        self.basic_repro_num = basic_repro_num
    
    def test_virus_instantiation():
        # *Check to make 
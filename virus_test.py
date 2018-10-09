import pytest
import io
import sys
import virus

def test_virus_instantiation():
        # * Check to make the virus instantiator is working 
        virus =  Virus("HIV", 0.8, 0.3)
        assert virus.name == "HIV"
        assert virus.mortality_rate == 0.8
        assert virus.basic_repro_num
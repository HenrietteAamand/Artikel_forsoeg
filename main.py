
from filereader import *
from extract_phases import *

fr = filereader_class( "C:/Users/hah/Documents/Artikel_forsoeg/Data/")

timelimits_list = fr.read_data('timelimits')
eph = Extract_phases_class(timelimits_list)

for n in range(51):
    filename = "Testperson_" + str(n+1)
    data_list = fr.read_data(filename)
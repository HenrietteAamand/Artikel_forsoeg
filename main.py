
from filereader import *
from sort_data import *

#fr = filereader_class( "C:/Users/hah/Documents/Artikel_forsoeg/Data/")
fr = filereader_class("C:/Users/Bruger/Documents/GitHub/Praktik/Artikel_forsoeg/Data/")
sd = sort_data_class()

timelimits_list = fr.read_data('timelimits')
brugbare =[3,4,5]
gennemkoerselsesgang = 0
all_datasets = {}
for testperson_nr in brugbare:
    filename = "my_log_filer/Testperson_" + str(testperson_nr)
    data_list = fr.read_data(filename)
    temp_data_dict = sd.sort(timelimits_list = timelimits_list, data_list=data_list, testperson_nr= testperson_nr, gennemloeb= gennemkoerselsesgang)
    all_datasets[testperson_nr] = temp_data_dict.copy()
    gennemkoerselsesgang +=1

#Nu skulle data gerne være indlæst


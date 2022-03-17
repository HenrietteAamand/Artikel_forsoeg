
from pandas import test
from filereader import *
from sort_data import *
from process_results import *
from plotter import *

#fr = filereader_class( "C:/Users/hah/Documents/Artikel_forsoeg/Data/")
fr = filereader_class("C:/Users/Bruger/Documents/GitHub/Praktik/Artikel_forsoeg/Data/")
sd = sort_data_class()
results = results_class()
plotter = plotter_class()

timelimits_list = fr.read_data('timelimits_full_2')#therest')
brugbare =[1,3,4,5,6,7,8,9,10,11,12,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,35,36,37,38]#,40,41,42,43,44,45,46,47,48,49,50,51,52]
gennemkoerselsesgang = 0
all_datasets = {}
for testperson_nr in brugbare:
    filename = "my_log_filer/Testperson_" + str(testperson_nr)
    data_list = fr.read_data(filename)
    temp_data_dict = sd.sort(timelimits_list = timelimits_list, data_list=data_list, testperson_nr= testperson_nr, gennemloeb= gennemkoerselsesgang)
    all_datasets[testperson_nr] = temp_data_dict.copy()
    gennemkoerselsesgang +=1

#Nu skulle data gerne være indlæst

for testperson_key in all_datasets:
    # bestem index, mean + std for hver fase + velocity (linReg)
    current_dataset = all_datasets[testperson_key]
    dict_mean_std = {}
    dict_index = {}
    for key in current_dataset:
        if('tid' in key):
            pass
        else:
            tidsliste_key = key + '_tid'
            indexes = results.process_results(hr_list=current_dataset[key] , tider_list = current_dataset[tidsliste_key],testperson_nr=testperson_key, intervention=key)
            dict_index[key] = indexes
            list_mean_std = results.get_mean_and_std_list()
            dict_mean_std[key] = list_mean_std
    
    # Plot de 4 hr kurver afhængigt af tiden med indtegnet velocity og stabiliseringstidspunkt/index
    velocity_list_lin_reg = results.get_coefs()
    plotter.plot_limit_HRM_pro(current_dataset, testperson_key, show_bool=False, index_list=dict_index,dict_mean_std=dict_mean_std, hastighed_lin_reg=velocity_list_lin_reg)    

    # Tegn de gaussiske fordelinger med histogrammer og fordelingskurver
    results.plot_hist_and_gaussian(dict_hr_data=current_dataset,dict_mean_std=dict_mean_std,testperson_nr = testperson_key)

# gem resultaterne i en passende liste/dictionary så de senere kan gemmes i en fil. 
res = results.Get_results_as_list()   
fr.save_results(res, 'results.csv')

import json
import pyhrv.frequency_domain as fd
import pyhrv.time_domain as td
import pyhrv.tools as tools
import matplotlib.pyplot as plt
"""
RMSSD: Kan godt laves på shortterm. Udtryk for parasympatisk aktivitet
pNN50: krav om 2 minutters længde. Usikkert hvad denne viser
HF: min 1 minut. Parasympatisk tone
LF: 2 minutter. 
LF/HF: Ratioen mellem LF og HF. 

"""

class HRV_class:
    def __init__(self) -> None:
        pass

    def hrv_extract(self, dict_all_obs = [], dict_usefull_dataseta = {}):
        all_hrv_data = {}
        for dataset in dict_usefull_dataseta:
            # printer RR:
            for fase in json.loads(dataset['faser']):
                string_rr = "RR_" + dataset['sensor'] + "_" + str(fase)
                string_time = "RRtime_" + dataset['sensor'] + "_" + str(fase)
                testpersonnummer = int(dataset['testperson'])
                rr_list = dict_all_obs[testpersonnummer][string_rr]
                time_list = dict_all_obs[testpersonnummer][string_time]
                string_hrv = dataset['sensor'] + "_Testperson_" + dataset['testperson'] + '_Fase_' + str(fase)
                all_hrv_data[string_hrv] = self.two_minutes(rr_list,time_list)
                #self.understand_nni(rr_list, time_list)
            print("done testperson " + dataset['testperson'])
        return all_hrv_data

    def two_minutes(self, rr_list = [], time_list = []):
        sec = 120
        
        index_15 = 0
        index_counter = 0
        cumulative_time = 0
        hrv_list = []
        n = 0
        temp_rr_list = []
        total_time = 0
        while n < len(rr_list):
            temp_rr_list.append(rr_list[n])
            cumulative_time += rr_list[n]/1000
            index_counter +=1
            if(cumulative_time <= 15):
                index_15 = n
            if(cumulative_time >= sec):
                total_time = time_list[n]
                returned = fd.frequency_domain(temp_rr_list, show=False)
                dict_results = {}
                dict_results['lf_hf'] = returned['fft_ratio'] #'lomb_', 'fft_', 'ar'
                dict_results['abs'] = returned['fft_abs']
                dict_results['rel'] = returned['fft_rel']
                dict_results['total'] = returned['fft_total']
                dict_results['time'] = total_time
                sdnn = td.sdnn(temp_rr_list)
                dict_results['sdnn'] = sdnn[0]

                hrv_list.append(dict_results)
                n = index_15-1
                temp_rr_list = []
                cumulative_time = 0
            n+=1
            
        return hrv_list

    def understand_nni(self, rr_list = [], rpeaks = []):
        nni = tools.nn_intervals(rpeaks)

        plt.plot(nni, label = 'nni')
        plt.plot(rr_list, label = 'rr_list')
        plt.legend()
        plt.show()

        
import matplotlib.pyplot as plt
import numpy as np
from statistics import mode
from stabelisation import*
import json
from sklearn.linear_model import LinearRegression


class plotter_class():
    def __init__(self) -> None:
        self.fase_variable = 0
        self.testperson = 1
        self.velocities = []
        self.path = 'C:/Users/Bruger/Documents/GitHub/Praktik/Forsoeg_sammenligningsscript/Forsoeg_sammenligningsscript/Figurer/'
        self.path = 'C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/Figurer/'
        pass

    def plot_rr_subplot(self, Dict_all_data: dict, Dict_accel: dict, counter: int, show_bool = True, tidsforskydning = []):
        """Metoden plotter de givne RR-værdier

        Args:
            maxrefdes (list, optional): Liste med RR-værdier for maxrefdes. Defaults to [].
            hrm_pro (list, optional): Liste med RR-værdier for HRM-Pro. Defaults to [].
            forerunner (list, optional): Liste med RR-værdier for Forerunner 45. Defaults to [].
            empatica (list, optional): Liste med RR værdier for Empatica. Defaults to [].
            fasenummer (int, optional): Fasenummer er nummeret på fasen, og Bruges til en titel. Defaults to 0.
            testpersonnummer (int, optional): Testpersonnummer er nummeret på testpersonen, hvis data der plottes. Defaults to 0.
            show_bool (bool, optional): Styrer om plottet vises eller ej. Defaults to True.
        """

        # DU ER VED AT TIDSFORSKYDE!!!

        min_max = []
        list_timeaxes = []
        fs_maxrefdes = 25/5
        time_corrected_dict = {}
        fs_empatica = 32/8
        for fasenummer in range(4):
            delta_tid_maxrefdes = 1/fs_maxrefdes
            delta_tid_empatica = 1/fs_empatica
            signal_maxrefdes103 = Dict_accel[counter]['Accel_Maxrefdes103_' + str(fasenummer) + '_X']
            signal_empatica = Dict_accel[counter]['Accel_Empatica_' + str(fasenummer) + '_X']
            
            # længde af signal i tid
            tid_accel_max = len(signal_maxrefdes103)/fs_maxrefdes
            tid_accel_empatica = len(signal_empatica)/fs_empatica

            # Laver tidsakse til de forskellige signaler så de kan plottes i samme figur
            tidsakse_maxrefdes = np.arange(0,tid_accel_max, delta_tid_maxrefdes)
            tidsakse_empatica = np.arange(0,tid_accel_empatica, delta_tid_empatica)
            # for time in range(len(tidsakse_empatica)-1):
            #     tidsakse_empatica[time] = tidsakse_empatica[time]+float(tidsforskydning[counter-1]['empatica_' + str(fasenummer)])

            dict_tidsakse = {}
            dict_tidsakse["Max"] = tidsakse_maxrefdes
            dict_tidsakse["Empatica"] = tidsakse_empatica
            list_timeaxes.append(dict_tidsakse)


            time_emp = []
            time_hrm = []
            time_corrected_dict[fasenummer] = {}
            if(len(tidsforskydning) > 0):
                for time in Dict_all_data[counter]['RRtime_Empatica_' + str(fasenummer)]:
                    time_emp.append(time+float(tidsforskydning[counter-1]['empatica_' + str(fasenummer)]))
                for time in Dict_all_data[counter]['RRtime_Hrmpro_' + str(fasenummer)]:
                    time_hrm.append(time+float(tidsforskydning[counter-1]['hrmpo_' + str(fasenummer)]))
                time_corrected_dict[fasenummer]['empatica'] = time_emp
                time_corrected_dict[fasenummer]['hrmpro'] = time_hrm
            else:
                time_corrected_dict[fasenummer]['empatica'] = Dict_all_data[counter]['RRtime_Empatica_' + str(fasenummer)] 
                time_corrected_dict[fasenummer]['hrmpro'] = Dict_all_data[counter]['RRtime_Hrmpro_' + str(fasenummer)]
            


            # Bestemmer max omg minimumværdier til RR-værdi y-akse
            middel = mode(Dict_all_data[counter]['RR_Hrmpro_' + str(fasenummer)])
            minimum = middel*0.6
            maximum = middel*1.4
            min_max.append(minimum)
            min_max.append(maximum)
        y_lim_low = min(min_max)
        y_lim_high = max(min_max)
        if(counter == 4):
            y_lim_low = 300
            y_lim_high = 1200




        fig, axs = plt.subplots(4,2, figsize = (20,15), gridspec_kw={'height_ratios': [5, 2,5,2]})
        fig.suptitle("RR værdier for testperson " + str(counter) + " efter endt stresstest - Forerunner er pillet ud")
        list_koordinates_rr = [(0,0), (0,1), (2,0), (2,1)]
        list_koordinates_accel = [(1,0), (1,1), (3,0), (3,1)]
        for n in range(len(list_koordinates_rr)):
            axs[list_koordinates_rr[n]].plot(Dict_all_data[counter]['RRtime_Maxrefdes103_' + str(n)],Dict_all_data[counter]['RR_Maxrefdes103_' + str(n)], label = 'MAXREFDES103')
            axs[list_koordinates_rr[n]].plot(time_corrected_dict[n]['empatica'],Dict_all_data[counter]['RR_Empatica_' + str(n)], label = 'empatica')
            axs[list_koordinates_rr[n]].plot(time_corrected_dict[n]['hrmpro'], Dict_all_data[counter]['RR_Hrmpro_' + str(n)], label = 'HRM-Pro', color = 'g')
            #axs[list_koordinates[n]].plot(Dict_all_data[counter]['RR_Forerunner_' + str(n)], label = 'Forerunner 45')
            axs[list_koordinates_rr[n]].set_xlabel('Tid [s]')
            axs[list_koordinates_rr[n]].set_ylabel('RR-værdier [ms]')
            axs[list_koordinates_rr[n]].legend(loc = 'upper right')
            axs[list_koordinates_rr[n]].set_title('Fase ' + str(n))
            axs[list_koordinates_rr[n]].set_ylim([y_lim_low, y_lim_high])
            #Accelerometerdata
            axs[list_koordinates_accel[n]].plot(list_timeaxes[n]['Empatica'],Dict_accel[counter]['Accel_Empatica_' + str(n) + '_X'], label = 'X emp', color = 'darkgoldenrod')
            axs[list_koordinates_accel[n]].plot(list_timeaxes[n]['Empatica'],Dict_accel[counter]['Accel_Empatica_' + str(n) + '_Y'], label = 'Y emp', color = 'gold')
            axs[list_koordinates_accel[n]].plot(list_timeaxes[n]['Empatica'],Dict_accel[counter]['Accel_Empatica_' + str(n) + '_Z'], label = 'Z emp', color = 'tan')
            axs[list_koordinates_accel[n]].plot(list_timeaxes[n]['Max'],Dict_accel[counter]['Accel_Maxrefdes103_' + str(n) + '_X'], label = 'X max', color = 'indigo')
            axs[list_koordinates_accel[n]].plot(list_timeaxes[n]['Max'],Dict_accel[counter]['Accel_Maxrefdes103_' + str(n) + '_Y'], label = 'Y max', color = 'blueviolet')
            axs[list_koordinates_accel[n]].plot(list_timeaxes[n]['Max'],Dict_accel[counter]['Accel_Maxrefdes103_' + str(n) + '_Z'], label = 'Z max', color = 'mediumpurple')
            axs[list_koordinates_accel[n]].set_xlabel('Tid [s]')
            axs[list_koordinates_accel[n]].set_ylabel('accel [g]')
            axs[list_koordinates_accel[n]].legend(loc = 'upper right')
      
                
        fig.set_tight_layout('tight')
        #fig.set_size_inches(20,30)
        fig.subplots_adjust(left=0.05, bottom=0.08, right=0.97, top=0.92, wspace=None, hspace=None)
        path = 'C:/Users/Bruger/Documents/GitHub/Praktik/Forsoeg_sammenligningsscript/Forsoeg_sammenligningsscript/Figurer/RR/'
        path = 'C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/Figurer/RR/'
        title = 'Testperson ' + str(counter)
        fig.savefig(path + title, dpi = 300)
        if show_bool == True:
            plt.show()    

    def plot_hr_subplot(self, Dict_all_data: dict, counter: int, show_bool = True):
        """Plotter alle faser for en given testperson i det samme subplot. Dermed bliver der en figur på 2x2 med fase 0 - 3

        Args:
            Dict_all_data (dict): dictionarie med data fra samtlige testpersoner og samtlige faser
            counter (int): nummeret på den testperson der ønskes plottet hr data for
            show_bool (bool, optional): Styrer om plottet vises eller ej. 
        """
        list_timeaxes = []
        fs_maxrefdes = 25
        fs_empatica = 1
        fs_garmin = 4
        
        i = 0
        while i < 4:
            maxrefdes = Dict_all_data[counter]['Hr_Maxrefdes103_' + str(i)]
            hrm_pro = Dict_all_data[counter]['Hr_Hrmpro_' + str(i)]
            empatica = Dict_all_data[counter]['Hr_Empatica_' + str(i)]
            forerunner = Dict_all_data[counter]['Hr_Forerunner_' + str(i)]

            # Deltatider
            delta_tid_maxrefdes = 1/fs_maxrefdes
            delta_tid_garmin = 1/fs_garmin
            delta_tid_empatica = 1/fs_empatica

            # længde af signal i tid
            tid_maxrefdes = len(maxrefdes)/fs_maxrefdes
            tid_empatica = len(empatica)/fs_empatica
            tid_hrmpro = len(hrm_pro)/fs_garmin
            tid_forerunner = len(forerunner)/fs_garmin

            # Laver tidsakse til de forskellige signaler så de kan plottes i samme figur
            tidsakse_maxrefdes = np.arange(0,tid_maxrefdes,delta_tid_maxrefdes)
            tidsakse_empatica = np.arange(0,tid_empatica, delta_tid_empatica)
            tidsakse_hrmpro = np.arange(0,tid_hrmpro, delta_tid_garmin)
            tidsakse_forerunner = np.arange(0,tid_forerunner, delta_tid_garmin)

            dict_tidsakse = {}
            dict_tidsakse["Maxrefdes103"] = tidsakse_maxrefdes
            dict_tidsakse["Hrmpro"] = tidsakse_hrmpro
            dict_tidsakse["Empatica"] = tidsakse_empatica
            dict_tidsakse["Forerunner"] = tidsakse_forerunner

            list_timeaxes.append(dict_tidsakse)
            i += 1

        fig, axs = plt.subplots(2,2)
        fig.suptitle("Hr for testperson " + str(counter) + " efter endt stresstest")
        
        list_koordinates = [(0,0), (0,1), (1,0), (1,1)]


        for n in range(len(list_koordinates)):
            axs[list_koordinates[n]].plot(list_timeaxes[n]["Maxrefdes103"], Dict_all_data[counter]['Hr_Maxrefdes103_' + str(n)], label = 'MAXREFDES103')
            axs[list_koordinates[n]].plot(list_timeaxes[n]["Empatica"], Dict_all_data[counter]['Hr_Empatica_' + str(n)], label = 'empatica')
            axs[list_koordinates[n]].plot(list_timeaxes[n]["Hrmpro"],  Dict_all_data[counter]['Hr_Hrmpro_' + str(n)], label = 'HRM-Pro')
            axs[list_koordinates[n]].plot(list_timeaxes[n]["Forerunner"], Dict_all_data[counter]['Hr_Forerunner_' + str(n)], label = 'Forerunner 45')
            axs[list_koordinates[n]].set_xlabel('Tid [sekunder]')
            axs[list_koordinates[n]].set_ylabel('HR [BPM]')
            axs[list_koordinates[n]].legend(loc = 'upper right')
            axs[list_koordinates[n]].set_title('Fase ' + str(n))


        fig.set_size_inches(20,10)
        fig.subplots_adjust(left=0.03, bottom=0.08, right=0.97, top=0.92, wspace=None, hspace=None)
        path = 'C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/Figurer/HR/Alle_sensorer/'
        title = 'Testperson ' + str(counter)
        fig.savefig(path + " " + title) #, dpi = 200)
        if show_bool == True:
            plt.show()    

    def plot_limit_HRM_pro(self, Dict_one_testperson: dict, testperson_nr: int, show_bool = True, index_list = [], dict_mean_std = {}, fase_intervention_list = [], hastighed_lin_reg = {}, hastighed_two_points = []):
        """ Her plottes hr data udelukkende for HRM-pro. Figurerne bruges i selve forsøget. I figuren er der:
             1) Det midlede hr signal
             2) Et stem der viser stabiliseringstidspunktet
             3) En linje der viser hastigheden alt efter metode
             4) Tre horisontale linje med hhv stabiliseringsniveau +/- std

        Args:
            Dict_all_data (dict): Dictionarie med data fra samtlige testpersoner og samtlige faser
            counter (int): nummeret på den testperson der ønskes plottet hr data for
            show_bool (bool, optional): Styrer om plottet vises eller ej. Default er True.
            index_list (list, optional): Listen indeholder ved hvilket index i hr_listen stabiliseringstidspunktet er fundet for fase 1-3. Defaults er [].
            list_mean_std (list, optional): Liste med et dictionary. Listen har 3 pladser svarende til fase 1-3 og hver dictionary har 4 pladser hhv mean_low, mean_high, std_low og std_high. Defaults er [].
            fase_intervention_list (list, optional): liste med sammenhæng mellem testperson, fase og intervention. Defaults er [].
            hastighed_lin_reg (list, optional): Liste med de hastigheder der er beregnet via den lineære regression. Defaults er [].
            hastighed_two_points (list, optional): Liste med de hastigheder der er beregnet via en two point metode. Defaults er [].
        """

        dict_timeaxes = {}
        dict_indexes_time = {}
        fs = 4
        i = 0
        N = 51
        max_and_min_values = []
        dict_hastighed = {} 
        intervention_list = []
        dict_avg = {}
       
        for key in Dict_one_testperson:
            if('tid' in key):
                pass
            else:
                # Tilføj det filtrerede signal til en liste/dictionary, med tilknyttet intervention
                # Beregn y-værdier for den lineære regression:
                intervention_list.append(key)
                # filtrer signalet + lav tidsakse på -2*N længde af originalsignalet
                fs = 4            
                # Antal filterkoefficienter
                N = fs*10+1
                # Finder det filtrerede signal
                signal_avg = self.__get_filtered_signal(Dict_one_testperson[key], N)
                dict_avg[key] = signal_avg

                dict_tid = {}
                time_key = key+'_tid'
                time_gmm = Dict_one_testperson[time_key][index_list[key]['gmm']]
                dict_tid['gmm'] = time_gmm
                dict_indexes_time[key] = dict_tid


                # Laver tidsakse til de forskellige signaler så de kan plottes i samme figur
                dict_tidsakse = {}
                dict_tidsakse["Signal"] = Dict_one_testperson[key+'_tid']
                dict_tidsakse["Avg"] = Dict_one_testperson[key+'_tid'][:len(Dict_one_testperson[key+'_tid'])-N*2] #Fjerner de første 41 tider og de sidste 41 tider.
                dict_timeaxes[key] = dict_tidsakse
                max_and_min_values.append(max(signal_avg))
                max_and_min_values.append(min(signal_avg))
                
                list_regression = []
                a = hastighed_lin_reg[key]['coef']
                b = hastighed_lin_reg[key]['intercept']
                # Laver den rette linje
                for tid in dict_tidsakse["Avg"]:
                    list_regression.append((a*(tid)+b))
                dict_hastighed[key] = list_regression


        # Ændrer skriftstørrelsen, så plotsne bliver mere læsbare i artiklen
        SMALL_SIZE = 12
        MEDIUM_SIZE = 12 #16
        MEDIUM_BIG_SIZE = 14 #20
        BIGGER_SIZE = 16 #22

        plt.rc('font', size=MEDIUM_SIZE)         # controls default text sizes
        plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
        plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('legend', fontsize=MEDIUM_BIG_SIZE)   # legend fontsize
        plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

        fig, axs = plt.subplots(2,2)
        fig.suptitle("Hr, testperson " + str(testperson_nr) + " after finishing the stresstest", fontweight='bold')
        list_koordinates = [(0,0), (0,1), (1,0), (1,1)]

        y_lim_low = min(max_and_min_values)-5
        y_lim_high = max(max_and_min_values)+5
        for n in range(len(list_koordinates)):
            #axs[list_koordinates[n]].plot(list_timeaxes[n]["Signal"],  Dict_all_data[counter][signal_name + str(n)][N:len(Dict_all_data[counter][signal_name + str(n)])-N], label = 'Raw Hr data', color = 'g', linewidth = 0.8)
            axs[list_koordinates[n]].plot(dict_timeaxes[intervention_list[n]]["Avg"],  dict_avg[intervention_list[n]], label = 'Averaged Hr data', color = 'g', linewidth = 2.5)
            mean = dict_mean_std[intervention_list[n]][0]["mean_low"]
            axs[list_koordinates[n]].axhline(y=mean, color='b', linestyle='-', label = 'Mean of low cluster = ' + str(round(mean,2)), linewidth = 1.6)
            axs[list_koordinates[n]].axhline(y=mean + dict_mean_std[intervention_list[n]][0]["std_low"], color='k', linestyle='--', linewidth = 1, label = 'Mean of low cluster +/- 1*std ')
            axs[list_koordinates[n]].axhline(y=mean - dict_mean_std[intervention_list[n]][0]["std_low"], color='k', linestyle='--', linewidth = 1)
            axs[list_koordinates[n]].plot(dict_timeaxes[intervention_list[n]]["Avg"], dict_hastighed[intervention_list[n]], color = 'darkgoldenrod', label = 'Stabelization velocity = ' + str(hastighed_lin_reg[intervention_list[n]]['coef']) + ' bpm/s', linewidth = 2)   
            markerline_mean, stemlines_mean, baseline = axs[list_koordinates[n]].stem(dict_indexes_time[intervention_list[n]]['gmm'],y_lim_high-10,'b', markerfmt='o', label = 'Stabilization time = ' + str(dict_indexes_time[intervention_list[n]]['gmm']) + " sec", basefmt=" ")
    
            plt.setp(markerline_mean, 'color', plt.getp( stemlines_mean,'color'))
            axs[list_koordinates[n]].set_ylim([y_lim_low, y_lim_high])
            axs[list_koordinates[n]].set_xlabel('Time [seconds]')
            axs[list_koordinates[n]].set_ylabel('HR [bpm]')
            axs[list_koordinates[n]].legend(loc = 'upper right', facecolor="white")
            axs[list_koordinates[n]].set_facecolor('whitesmoke')
            axs[list_koordinates[n]].grid(color = 'lightgrey')
            axs[list_koordinates[n]].set_title(intervention_list[n], fontsize = MEDIUM_BIG_SIZE, fontweight='bold')
            self.fase_variable += 1

        fig.set_size_inches(20,10)
        fig.set_tight_layout('tight')
        fig.subplots_adjust(left=0.05, bottom=0.08, right=0.97, top=0.92, wspace=None, hspace=None)
        #path = 'C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/Figurer/HR/gmm/'
        path ='C:/Users/Bruger/Documents/GitHub/Praktik/Artikel_forsoeg/Figurer/heart_rate/'
        title = 'Testperson ' + str(testperson_nr)
        fig.savefig(path + " " + title, dpi = 500)
        self.testperson+= 1
        if show_bool == True:
            plt.show()    

    def plot_HRV(self, dict_hrv_data: dict, dict_usefull_data = dict, show_bool = True):
        
        plt.close('all')
        # vlf: 0, lf: 1, hf: 2
        l = 0
        list_reorganized_hrv_results = []

        for dataset in dict_usefull_data:
            sensor = dataset['sensor']
            testperson = dataset['testperson']
            for fase in json.loads(dataset['faser']):
                time = []
                lf = []
                hf = []
                lf_hf = []
                sdnn = []

                dict_reorganized_fase_results = {}
                key = sensor + "_Testperson_" + testperson + '_Fase_' + str(fase)
                for result in dict_hrv_data[key]:
                    time.append(result['time'])
                    lf.append(result['abs'][1]) #'abs' kan erstattes af 'rel' hvorved man får de relatve powers frem for absolutte
                    hf.append(result['abs'][2])
                    lf_hf.append(result['lf_hf'])
                    sdnn.append(result['sdnn'])
                dict_reorganized_fase_results['time'] = time
                dict_reorganized_fase_results['lf'] = lf
                dict_reorganized_fase_results['hf'] = hf
                dict_reorganized_fase_results['lf_hf'] = lf_hf
                dict_reorganized_fase_results['sdnn'] = sdnn
                dict_reorganized_fase_results['lf_linreg'] = self.lin_reg(time,lf)
                dict_reorganized_fase_results['hf_linreg'] = self.lin_reg(time,hf)
                dict_reorganized_fase_results['lf_hf_linreg'] = self.lin_reg(time,lf_hf)
                dict_reorganized_fase_results['sdnn_linreg'] = self.lin_reg(time,sdnn)
                list_reorganized_hrv_results.append(dict_reorganized_fase_results)
                l+= 1

        SMALL_SIZE = 6
        MEDIUM_SIZE = 6 #18
        MEDIUM_BIG_SIZE = 10 #22
        BIGGER_SIZE = 14

        plt.rc('font', size=MEDIUM_SIZE)         # controls default text sizes
        plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
        plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('legend', fontsize=MEDIUM_SIZE)   # legend fontsize
        plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
        hrv_params = ['lf', 'hf', 'lf_hf','sdnn']
        rows = 8
        columns = len(hrv_params)
        fig, axs = plt.subplots(rows,columns)
        fig.suptitle("HRV-parameters", fontweight='bold')

        list_koordinates = []
        for row in range(rows):
            for column in range(columns):
                koordinates = (row,column)
                list_koordinates.append(koordinates)
        n = 0
        axes_index = 0
        for n in range(len(list_reorganized_hrv_results)):
            for i in range(len(hrv_params)):
                axs[list_koordinates[axes_index]].scatter(list_reorganized_hrv_results[n]['time'], list_reorganized_hrv_results[n][hrv_params[i]], s = 7)
                string = hrv_params[i]+'_linreg'
                axs[list_koordinates[axes_index]].plot(list_reorganized_hrv_results[n][string]['time'], list_reorganized_hrv_results[n][string]['hrv'], 'g', label = list_reorganized_hrv_results[n][string]['model'] )
                y_low = min(list_reorganized_hrv_results[n][hrv_params[i]])
                y_low = y_low - 0.5*y_low
                y_max = max(list_reorganized_hrv_results[n][hrv_params[i]])
                y_max = y_max + 0.3*y_max
                axs[list_koordinates[axes_index]].set_ylim(y_low,y_max)
                axs[list_koordinates[axes_index]].set_xlabel('time')
                axs[list_koordinates[axes_index]].set_ylabel('Abs power [ms^2]')
                #axs[list_koordinates[n]].legend(loc = 'upper right', facecolor="white")
                axs[list_koordinates[axes_index]].set_facecolor('whitesmoke')
                axs[list_koordinates[axes_index]].grid(color = 'lightgrey')
                axs[list_koordinates[axes_index]].legend(loc = 'upper right', facecolor="white")
                axes_index+=1
        for index in range(len(hrv_params)):
            axs[list_koordinates[index]].set_title(hrv_params[index], fontsize = MEDIUM_BIG_SIZE, fontweight='bold')
        # axs[list_koordinates[1]].set_title('HF', fontsize = MEDIUM_BIG_SIZE, fontweight='bold')
        # axs[list_koordinates[2]].set_title('LF/HF', fontsize = MEDIUM_BIG_SIZE, fontweight='bold')

        fig.set_size_inches(columns*2, rows*2)
        fig.set_tight_layout('tight')
        fig.subplots_adjust(left=0.05, bottom=0.08, right=0.97, top=0.92, wspace=None, hspace=None)
        path = self.path + '/hrv/'
        title = 'HRV'
        fig.savefig(path + " " + title, dpi = 500)
        if show_bool == True:
            plt.show()    
        
    def lin_reg(self, time: list, signal: list):
        X = np.array(time).reshape(-1,1)
        y = np.array(signal).reshape(-1,1)
        reg = LinearRegression(copy_X=True).fit(X, y)
        reg.score(X, y)
        coef = reg.coef_
        time_hrv = [time[0], time[len(time)-1]]
        hrv = []
        for n in range(2):
            coordinate_y = round(coef[0][0],3)*time_hrv[n]+round(reg.intercept_[0],3)
            hrv.append(coordinate_y)
        model = 'y = '+ str(round(coef[0][0],3)) + 'x'
        if(round(reg.intercept_[0])!=0):
            model = model + ' + ' + str(round(reg.intercept_[0]))
        dict_reg = {'time': time_hrv, 'hrv': hrv, 'model': model }
        return dict_reg      

    def get_velocities(self):
        return self.velocities

    def __get_filtered_signal(self, raw_signal: list, average_value: int):
        """filtrerer signalet med et mooving average filter. Der bruges numpy.convolve metoden medmode='same'. 

        Args:
            raw_signal (list): listet med hr signalet før filtrtering
            average_value (int): antallet af filterkoefficienter. Angives det til et lige tal korrigeres med +1

        Returns:
            list : Der returneres en liste med det midlede signal på længden n = (len(raw_signaal) - 2xN) svarende til de data, hvor filter og signal overlapper 100%
        """
        N = average_value
        if(N%2 == 0):
            N+=1
        hr_avg = np.convolve(raw_signal, np.ones(N)/N, mode='same')
        hr_return = hr_avg[N:len(hr_avg)-N]
        return hr_return

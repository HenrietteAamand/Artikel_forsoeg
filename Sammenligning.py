import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import statsmodels.api as sm
from scipy.stats import norm
import pylab
class sammenligning_class():
    """ OBS! Klassen er delvist forældet. Den har tidligere været brugt til at forsøge at sammenligne sensorerne, men har ikke været brugt længe. Derfor er filstierne m.v. forkerte.
        Flere ting virker altså ikke, og derfor skal der rettes nogle ting inden man direkte kan bruge klassen igen
    """
    def __init__(self) -> None:
        pass

    def __Downsample_maxrefdes(self, list_maxrefdes_data : list):
        i = 0
        do_7 = 0
        downsampled_maxrefdes_data = []
        while i+7 < len(list_maxrefdes_data):
            range_number = 6
            if(do_7 == 6):
                range_number = 7
                do_7 = -1
            mean = 0
            for n in range(range_number):
                mean += list_maxrefdes_data[i+n]*1/range_number
            do_7 +=1
            downsampled_maxrefdes_data.append(mean)
            i+=range_number
        #print("length before: " + str(len(list_maxrefdes_data)) + " Lengt_after: " + str(len(downsampled_maxrefdes_data)))
        return downsampled_maxrefdes_data

    def __upsample_empatica(self, list_empatica_data : list):
        upsampled_empatica_data = []
        for hr in list_empatica_data:
            for n in range(4):
                upsampled_empatica_data.append(hr)

        #print("length before: " + str(len(list_empatica_data)) + " Lengt_after: " + str(len(upsampled_empatica_data)))
        return upsampled_empatica_data
    
    def plot_differences(self, Dict_all_obs, counter):
        list_timeaxes = []
        list_differneces = []
        fs= 4
        diff_maxrefdes = []
        diff_empatica = []
        diff_forerunner = []
        i = 0
        while i < 4:
            maxrefdes_raw = Dict_all_obs[counter]['Hr_Maxrefdes103_' + str(i)]
            hrm_pro = Dict_all_obs[counter]['Hr_Hrmpro_' + str(i)]
            empatica_raw = Dict_all_obs[counter]['Hr_Empatica_' + str(i)]
            forerunner = Dict_all_obs[counter]['Hr_Forerunner_' + str(i)]

            maxrefdes = self.__Downsample_maxrefdes(maxrefdes_raw)
            empatica = self.__upsample_empatica(empatica_raw)
            print("Length og HRM-pro: " + str(len(hrm_pro)))
            # maxrefdes = self.krydskorellation(hrm_pro, maxrefdes, i, counter, "Maxrefdes103")
            # empatica = self.krydskorellation(hrm_pro, empatica, i, counter, "Empatica")
            # forerunner = self.krydskorellation(hrm_pro, forerunner, i, counter, "Forerunner")

            diff_maxrefdes = []
            diff_empatica = []
            diff_forerunner = []
            for n in range(len(hrm_pro)):
                if(n< len(maxrefdes)):
                    diff_maxrefdes.append(maxrefdes[n] - hrm_pro[n])
                if(n<len(empatica)):
                    diff_empatica.append(empatica[n] - hrm_pro[n])
                if(n<len(forerunner)):
                    diff_forerunner.append(forerunner[n] - hrm_pro[n]) 

            dict_differences = {}
            dict_differences["Maxrefdes103"] = diff_maxrefdes
            dict_differences["Empatica"] = diff_empatica
            dict_differences["Forerunner"] = diff_forerunner
            list_differneces.append(dict_differences)

             # Deltatider
            delta_tid = 1/fs

            # længde af signal i tid
            tid_diff_maxrefdes = len(diff_maxrefdes)/fs
            tid_diff_empatica = len(diff_empatica)/fs
            tid_diff_forerunner = len(diff_forerunner)/fs

            # Laver tidsakse til de forskellige signaler så de kan plottes i samme figur
            tidsakse_maxrefdes = np.arange(0,tid_diff_maxrefdes,delta_tid)
            tidsakse_empatica = np.arange(0,tid_diff_empatica, delta_tid)
            tidsakse_forerunner = np.arange(0,tid_diff_forerunner, delta_tid)

            dict_tidsakse = {}
            dict_tidsakse["Maxrefdes103"] = list(tidsakse_maxrefdes)
            dict_tidsakse["Empatica"] = list(tidsakse_empatica)
            dict_tidsakse["Forerunner"] = list(tidsakse_forerunner)

            list_timeaxes.append(dict_tidsakse)
            i += 1

        fig, axs = plt.subplots(2,2)
        list_koordinates = [(0,0), (0,1), (1,0), (1,1)]
    
        fig.suptitle("Differens mellem sensorer for testperson " + str(counter) + "efter endt stresstest")
        
        for n in range(len(list_koordinates)):
            axs[list_koordinates[n]].plot(list_timeaxes[n]["Maxrefdes103"], list_differneces[n]["Maxrefdes103"], label = 'MAXREFDES103 - HRM-Pro')
            axs[list_koordinates[n]].plot(list_timeaxes[n]["Empatica"], list_differneces[n]["Empatica"], label = 'Empatica - HRM-Pro')
            axs[list_koordinates[n]].plot(0,0)
            axs[list_koordinates[n]].axhline(y=0, color = 'g', linestyle='-', linewidth = 0.5)
            axs[list_koordinates[n]].plot(list_timeaxes[n]["Forerunner"], list_differneces[n]["Forerunner"], label = 'Forerunner 45 - HRM-Pro')
            axs[list_koordinates[n]].set_xlabel('Tid [sekunder]')
            axs[list_koordinates[n]].set_ylabel('Absolut forskel ')
            axs[list_koordinates[n]].legend(loc = 'upper right')
            axs[list_koordinates[n]].set_title('Fase ' + str(n))
        fig.tight_layout()

        fig.set_size_inches(20,10)
        fig.subplots_adjust(left=0.03, bottom=0.08, right=0.97, top=0.92, wspace=None, hspace=None)
        #path = 'C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/Figurer/Differens/Med_krydskorellation/'
        path = 'C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/Figurer/Differens/Uden_krydskorellation/'
        title = 'Testperson ' + str(counter) + " - Uden krydskorellation"
        fig.savefig(path + " " + title) #, dpi = 200)
        #plt.show()

    def plot_normal_distribution(self, Dict_all_obs, counter, type='hist'):
        """ For at man må bruge Bland-Altman plot skal man undersøge at differensserne er normalfordelt. Dette kan gøres med denne klasse

        Args:
            Dict_all_obs (dict): Dictionarie med data fra samtlige testpersoner og samtlige faser
            counter (int): nummeret på den testperson der ønskes plottet hr data for
            type (str, optional): Vælger hvordan man vil tjekke normalfordelingen. Defaultt er 'hist', alternativet er 'QQ'
        """
        list_timeaxes = []
        list_differneces = []
        fs= 4
        diff_maxrefdes = []
        diff_empatica = []
        diff_forerunner = []
        i = 0
        while i < 4:
            maxrefdes_raw = Dict_all_obs[counter]['Hr_Maxrefdes103_' + str(i)]
            hrm_pro = Dict_all_obs[counter]['Hr_Hrmpro_' + str(i)]
            empatica_raw = Dict_all_obs[counter]['Hr_Empatica_' + str(i)]
            forerunner = Dict_all_obs[counter]['Hr_Forerunner_' + str(i)]

            maxrefdes = self.__Downsample_maxrefdes(maxrefdes_raw)
            empatica = self.__upsample_empatica(empatica_raw)
            print("Length og HRM-pro: " + str(len(hrm_pro)))
            # maxrefdes = self.krydskorellation(hrm_pro, maxrefdes, i, counter, "Maxrefdes103")
            # empatica = self.krydskorellation(hrm_pro, empatica, i, counter, "Empatica")
            # forerunner = self.krydskorellation(hrm_pro, forerunner, i, counter, "Forerunner")

            diff_maxrefdes = []
            diff_empatica = []
            diff_forerunner = []
            for n in range(len(hrm_pro)):
                if(n< len(maxrefdes)):
                    diff_maxrefdes.append(maxrefdes[n] - hrm_pro[n])
                if(n<len(empatica)):
                    diff_empatica.append(empatica[n] - hrm_pro[n])
                if(n<len(forerunner)):
                    diff_forerunner.append(forerunner[n] - hrm_pro[n]) 

            dict_differences = {}
            dict_differences["Maxrefdes103"] = diff_maxrefdes
            dict_differences["Empatica"] = diff_empatica
            dict_differences["Forerunner"] = diff_forerunner
            list_differneces.append(dict_differences)
            i += 1
        if(type == 'hist'):
            for n in range(4):
                fig, axs = plt.subplots(2,2,figsize = [20,10])
                list_koordinates = [(0,0), (0,1), (1,0), (1,1)]
                fig.suptitle("Differens mellem sensorer for testperson " + str(counter) + "efter endt stresstest")

                axs[list_koordinates[0]].hist(list_differneces[n]["Maxrefdes103"], 20, label = 'MAXREFDES103 - HRM-Pro', facecolor = 'blue', alpha = 0.7)
                axs[list_koordinates[0]].set_title('MAXREFDES')
                axs[list_koordinates[1]].hist(list_differneces[n]["Empatica"], 20, label = 'Empatica - HRM-Pro', facecolor = 'orange', alpha = 0.7)
                axs[list_koordinates[1]].set_title('Empatica')
                axs[list_koordinates[2]].hist(list_differneces[n]["Forerunner"], 20, label = 'Forerunner 45 - HRM-Pro', facecolor = 'red', alpha = 0.7)
                axs[list_koordinates[2]].set_title('Forerunner')
                fig.tight_layout()

                fig.subplots_adjust(left=0.03, bottom=0.08, right=0.97, top=0.92, wspace=None, hspace=None)
                #path = 'C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/Figurer/Differens/Med_krydskorellation/'
                path = 'C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/Figurer/Histogrammer/'
                title = 'Testperson ' + str(counter) + " - Histogram over differenserne"
                #fig.savefig(path + " " + title) #, dpi = 200)
                #plt.show()
        elif type == 'QQ':
            for n in range(4):
                self.__QQ_plot(list_differneces[n]["Maxrefdes103"])
                self.__QQ_plot(list_differneces[n]["Empatica"])
                self.__QQ_plot(list_differneces[n]["Forerunner"])
   
    def __QQ_plot(self, list_differences: list):
        list_differences = norm.rvs(size=1000)
        sm.qqplot(list_differences, line='45')
        pylab.show()

    def krydskorellation(self, HRM_pro: list, det_andet_signal: list, fase: int = 0, testperson: int = 0, sensor: str = ''):
        """ Kan bruges til at bestemme krydskorellationen mellem 2 signaler. Krydskorellationen laves op imod HRM-pro

        Args:
            HRM_pro (list): liste med HRM-pro data. Det er ikke afgørende, så det kunne lige så godt tests op mod eks epatica el.lign
            det_andet_signal (list): signalet der skal krydskorelleres med HRM-Pro
            fase (int, optional): Defaults to 0.
            testperson (int, optional): Defaults to 0.
            sensor (str, optional): Defaults to ''.

        Returns:
            list: Der returneres et signal der er forskudt svarende til det fundne lag.
        """
        if(len(det_andet_signal) == 0 or len(HRM_pro) == 0):
            #rint("Testperson " + str(testperson) + " fase " + str(fase) + " Sensor " + str(sensor) + " havde ingen data" )
            return det_andet_signal
        
        corr = sig.correlate(HRM_pro, (det_andet_signal),mode="valid",method="direct") / len(HRM_pro)
        lags = sig.correlation_lags(len(HRM_pro), len(det_andet_signal),mode="valid")
        corr /= np.max(corr)
        lag = lags[np.argmax(corr)]

    
        # fig,axs = plt.subplots()
        # # Plot of corrLag
        # axs.plot(lags/4,abs(corr))
        # # axs.set_xlim(-100,100)
        # axs.set_title("Korrelationsresultat for sensor " + sensor + " fase " + str(fase) + " Testperson " + str(testperson))
        # axs.set_xlabel("Lag [ms]")
        # plt.show()
        if(lag > 0):
            for n in range(lag):
                det_andet_signal.insert(0,det_andet_signal[0])
        elif( lag < 0):
            for n in range(lag):
                det_andet_signal.pop(0)
        return det_andet_signal

    def plot_corellation(self, Dict_all_obs, counter):
        """Plotter korellationen mellem alle signalerne. Jo bedre denne er, des mere ligner linjen en ret linje gennem 0,0

        Args:
            Dict_all_obs (dict): Dictionarie med data fra samtlige testpersoner og samtlige faser
            counter (int): nummeret på den testperson der ønskes at lavet corellation på
        """
        list_differneces = []
        fs= 4 #Default for Garmin
        diff_maxrefdes = []
        diff_empatica = []
        diff_forerunner = []
        i = 0
        while i < 4:
            maxrefdes_raw = Dict_all_obs[counter]['Hr_Maxrefdes103_' + str(i)]
            hrm_pro = Dict_all_obs[counter]['Hr_Hrmpro_' + str(i)]
            empatica_raw = Dict_all_obs[counter]['Hr_Empatica_' + str(i)]
            forerunner = Dict_all_obs[counter]['Hr_Forerunner_' + str(i)]

            maxrefdes = self.__Downsample_maxrefdes(maxrefdes_raw)
            empatica = self.__upsample_empatica(empatica_raw)
            print("Length og HRM-pro: " + str(len(hrm_pro)))
            maxrefdes = self.krydskorellation(hrm_pro, maxrefdes, i, counter, "Maxrefdes103")
            empatica = self.krydskorellation(hrm_pro, empatica, i, counter, "Empatica")
            forerunner = self.krydskorellation(hrm_pro, forerunner, i, counter, "Forerunner")

            diff_maxrefdes = []
            diff_empatica = []
            diff_forerunner = []
            for n in range(len(hrm_pro)):
                if(n< len(maxrefdes)):
                    diff_maxrefdes.append(maxrefdes[n])
                if(n<len(empatica)):
                    diff_empatica.append(empatica[n])
                if(n<len(forerunner)):
                    diff_forerunner.append(forerunner[n]) 

            dict_data = {}
            dict_data["Maxrefdes103"] = diff_maxrefdes
            dict_data["Empatica"] = diff_empatica
            dict_data["Forerunner"] = diff_forerunner
            dict_data["Hrm_pro"] = hrm_pro
            list_differneces.append(dict_data)

            i += 1

        fig, axs = plt.subplots(2,2)
        list_koordinates = [(0,0), (0,1), (1,0), (1,1)]
    
        fig.suptitle("Korellationsplot mellem sensorer for testperson " + str(counter) + " efter endt stresstest")
        
        for n in range(len(list_koordinates)):
            if(n !=0):
                #axs[list_koordinates[n]].plot(list_differneces[n]["Hrm_pro"],list_differneces[n]["Hrm_pro"])
                # axs[list_koordinates[n]].plot(list_differneces[n]["Hrm_pro"][:len(list_differneces[n]["Maxrefdes103"])], list_differneces[n]["Maxrefdes103"], 'o',label = 'MAXREFDES103 - HRM-Pro', linewidth = 0.5)
                # axs[list_koordinates[n]].plot(list_differneces[n]["Hrm_pro"][:len(list_differneces[n]["Empatica"])], list_differneces[n]["Empatica"], 'x',label = 'Empatica - HRM-Pro', linewidth = 0.5)
                # axs[list_koordinates[n]].plot(list_differneces[n]["Hrm_pro"][:len(list_differneces[n]["Forerunner"])], list_differneces[n]["Forerunner"], 'v', label = 'Forerunner 45 - HRM-Pro', linewidth = 0.5)
                # # axs[list_koordinates[n]].plot(list_differneces[n]["Hrm_pro"][:360], list_differneces[n]["Maxrefdes103"][:360], 'o',label = 'MAXREFDES103 - HRM-Pro', linewidth = 0.5)
                # # axs[list_koordinates[n]].plot(list_differneces[n]["Hrm_pro"][:360], list_differneces[n]["Empatica"][:360], 'x',label = 'Empatica - HRM-Pro', linewidth = 0.5)
                # # axs[list_koordinates[n]].plot(list_differneces[n]["Hrm_pro"][:360], list_differneces[n]["Forerunner"][:360], 'v', label = 'Forerunner 45 - HRM-Pro', linewidth = 0.5)
                axs[list_koordinates[n]].plot(list_differneces[n]["Hrm_pro"][360:len(list_differneces[n]["Maxrefdes103"])], list_differneces[n]["Maxrefdes103"][360:], 'o',label = 'MAXREFDES103 - HRM-Pro', linewidth = 0.5)
                axs[list_koordinates[n]].plot(list_differneces[n]["Hrm_pro"][360:len(list_differneces[n]["Empatica"])], list_differneces[n]["Empatica"][360:], 'x',label = 'Empatica - HRM-Pro', linewidth = 0.5)
                axs[list_koordinates[n]].plot(list_differneces[n]["Hrm_pro"][360:],list_differneces[n]["Hrm_pro"][360:])
                axs[list_koordinates[n]].plot(list_differneces[n]["Hrm_pro"][360:len(list_differneces[n]["Forerunner"])], list_differneces[n]["Forerunner"][360:], 'v', label = 'Forerunner 45 - HRM-Pro', linewidth = 0.5)
                axs[list_koordinates[n]].set_xlabel('Tid [sekunder]')
                axs[list_koordinates[n]].set_ylabel('Absolut forskel ')
                axs[list_koordinates[n]].legend(loc = 'upper right')
                axs[list_koordinates[n]].set_title('Fase ' + str(n))
        fig.tight_layout()

        fig.set_size_inches(20,10)
        fig.subplots_adjust(left=0.03, bottom=0.08, right=0.97, top=0.92, wspace=None, hspace=None)
        # path = 'C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/Figurer/Differens/Med_krydskorellation/'
        path = 'C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/Figurer/Differens/Uden_krydskorellation/'
        title = 'Testperson ' + str(counter) + " - Uden krydskorellation"
        fig.savefig(path + " " + title) #, dpi = 200)
        #plt.show()
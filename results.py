from stabelisation import stabelisation_class
from scipy.stats import norm
import scipy
import numpy as np
from sklearn.linear_model import LinearRegression

from stabelisation import *
class results_class():
    def __init__(self, fase_intervention_testperson_sammenhaeng) -> None:
        self.intervention = fase_intervention_testperson_sammenhaeng
        self.list_dict_results = []
        self.stabel = stabelisation_class()
        self.id_2_dot_0 = 1
        self.testperson = 1
        self.list_velocity = []
        
    

    def process_results(self, Dict_all_data: dict, counter: int):
        """Metoden styrer hvordan hr processeres, så der findes en stabiliseringshastighed og niveau. 

        Args:
            Dict_all_data (dict): dictionarie med data fra samtlige testpersoner og samtlige faser
            counter (int): Nummeret på den testperson der behandles

        Returns:
            (list): Der returneres en liste der indeholder 3 indexer svarende til stabiliseringstidspunktet for det midlede hr signal for alle tre faser
        """
        testperson_nr = counter
        i = 1
        fs = 0
        list_hr_avg = []
        self.list_mean_std = [] # Bruges til at tegne histogrammet med fordelingerne indtegnet
        index_list = []         # Gemmer de indexer, der er fundet som stabiliseringstidspunktet. 
        self.coef_list = []     # Gemmer hældningskoefficienten sat skæringen med y-aksen
        self.list_velocity = []

        # Dette gøres 4 gange svarende til de 4 faser. Ved baseline ønskes der ikke at gøre noge. 
        while i < 4: #denne tæller faser, jeg skal ikke forholde mig til antal personer
            if (i == 0):
                pass
            else:
                if(testperson_nr == 1): # hvis vi er i gang med testperson 1, svarende til at vi bruger maxrefdes data
                    signal_original = Dict_all_data[testperson_nr]['Hr_Maxrefdes103_' + str(i)]
                    signal_name="Hr_Maxrefdes103_"
                    fs = 25
                else: #Alle de andre gange bruger vi HRM-Pro
                    signal_original = Dict_all_data[testperson_nr]['Hr_Hrmpro_' + str(i)]
                    signal_name = "Hr_Hrmpro_"
                    fs = 4

                # Bestemmer ved hvilket index signalet er stabilt med gmm-metoden
                N = fs*10
                signal_original = Dict_all_data[testperson_nr][signal_name + str(i)]
                hr_avg = self.__get_filtered_signal(signal_original, N)
                list_hr_avg.append(hr_avg)
                index_gmm = self.stabel.gmm(hr_avg)
                index_soren = self.stabel.soren(signal_original, N)
                dict_index = {}
                dict_index['soren'] = index_soren
                dict_index['gmm'] = index_gmm
                index_list.append(dict_index)
                delta_tid_garmin = 1/fs

                # Gemmer resultaterne af gmm()
                std_low, std_high = self.stabel.get_stds()
                mean_low, mean_high = self.stabel.get_means()
                dict_mean_std = {}
                dict_mean_std["std_low"] = std_low
                dict_mean_std["std_high"] = std_high
                dict_mean_std["mean_low"] = mean_low
                dict_mean_std["mean_high"] = mean_high
                two_point_high_mean = hr_avg[0] # self.mean_high_data(hr_avg, index_gmm) #mean_high # Der er 3 forskellige forslag til hvordan man beregner hastigheden.  
                # dict_mean_std["mean_high"] = two_point_high_mean #Dette bruges hvis man vil plotte med en anden metode end gmm. Så skal denne linje ændres til det 'max' datapunkt som man ønsker den rette linje skal plottes efter. 
                self.list_mean_std.append(dict_mean_std)
                
                # gemmer de resultater der skal laves statistik af, så de senere kan gemmes i en fil
                tid1 = index_gmm*delta_tid_garmin
                maximum_hr = max(hr_avg)
                hastighed = self.two_point_velocity(two_point_high_mean,mean_low, tid1) # Der er to metoder til at finde hastigheden, her bruges 'two point'
                hastighed = self.linear_regression(hr_avg,fs, index_gmm)[0][0]     # Der er to metoder til at finde hastigheden, her bruges lineær regression, og det er den vi har brugt til at bestemme hastigheden i pilotforsøget
                # hastighed = (mean_low-maximum_hr)/(tid1)
                stabiliseringsniveau, denhoje = self.stabel.get_means()
                
                # Jeg vil gerne gemme hvilken intervention der hører til dette datasæt. Derfor skal jeg ind i interventionslisten og finde den intervention, hvor fasenumrene og testpersonnummmeret matcher
                n=0
                while(n < 3):
                    index2 = testperson_nr*3+n-3 # Jeg trækker 3 fra, fordi jeg hver gang ganger med 3, og dermed lander 1 person for langt fremme
                    fasenummer = self.intervention[index2]['fase']
                    if(fasenummer == str(i)):
                        intervention = self.intervention[index2]['intervention']
                        break
                    n+=1
                dict_results = {}
                dict_results['ID 2.0'] = self.id_2_dot_0
                dict_results['ID 1.0'] = testperson_nr
                dict_results['Mean'] = stabiliseringsniveau
                dict_results['Condition'] = intervention
                dict_results['Time'] = tid1
                dict_results['Max'] = maximum_hr
                dict_results['Velocity (bpm/s)'] = hastighed

                self.list_dict_results.append(dict_results)
                i+=1

        self.id_2_dot_0 += 1
        self.plot_hist_and_gaussian(list_hr_data=list_hr_avg, list_mean_std = self.list_mean_std, counter=testperson_nr)
        return index_list
        

    def __get_filtered_signal(self, raw_signal, average_value):        
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

    def Get_results_as_list(self):
        """Når data skal behandles i R-studioi var det ønsket, at alle resultaterne kom ud i rækkefælgen: stilhed, statisk, dynamisk. Denne metode ændrer på rækkefølgen af resultaterne, så dette er tilfældet

        Returns:
            (list): liste med resultater for stabiliseringshastighed, niveau, tid mm, men nu i korrigeret rækkefølge. 
        """
        new_returnlist = []
        raekkefoelge = ['Silent', 'Static', 'Dynamic']
        i = 0
        while( i < len(self.list_dict_results)):
            for n in range(3):
                for j in range(3):
                    condition = self.list_dict_results[i+j]['Condition'] 
                    raekkefoelge_index = raekkefoelge[n]
                    if(condition == raekkefoelge_index):
                        new_returnlist.append(self.list_dict_results[i+j])
                        break

            i +=3


        return new_returnlist

    def Empty_result_dict(self):
        """Tømmer resultatlisten. Skulle bruges på et tidligere tidspunkt, hvor databehandlingen blev lavet flere gange uden programmet sluttede. Bruges ikke mere
        """
        self.list_dict_results.clear()

    def plot_hist_and_gaussian(self, list_hr_data, list_mean_std, counter = 0):
        """Plotter et histogram med fordelingerne der er fundet med gmm metoden

        Args:
            list_hr_data (list): Liste med de rå hr data
            list_mean_std ([type]): liste med længden 3. På hver plads er et dictionary, der indeholder mean og std for begge fordelinger
            counter (int, optional): testpeson nummer. Bruges ikke. Defaults to 0
        """
        SMALL_SIZE = 12
        MEDIUM_SIZE = 18
        BIGGER_SIZE = 24

        plt.rc('font', size=MEDIUM_SIZE)         # controls default text sizes
        plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
        plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('legend', fontsize=MEDIUM_SIZE)   # legend fontsize
        plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title        
        fig, axs = plt.subplots(2,2)
        fig.suptitle("Hr, testperson " + str(self.testperson) + " after finishing the stresstest", fontweight = 'bold') 
        list_koordinates = [(0,1), (1,0), (1,1), (0,0)]


        for n in range(len(list_koordinates)-1):
            bins = int(round(max(list_hr_data[n])-min(list_hr_data[n])))
            std_low = round(list_mean_std[n]["std_low"],2)
            std_high = round(list_mean_std[n]["std_high"],2)
            mean_low = round(list_mean_std[n]["mean_low"],2)
            mean_high = round(list_mean_std[n]["mean_high"],2)
            x_low = np.linspace(mean_low - 3* std_low, mean_low + 3*std_low, 100)
            x_high = np.linspace(mean_high - 3* std_high, mean_high + 3*std_high, 100)
            axs[list_koordinates[n]].plot(x_low, scipy.stats.norm.pdf(x_low, mean_low, std_low), label = 'Mean = ' + str(mean_low) + ' std = ' + str(std_low))
            axs[list_koordinates[n]].plot(x_high, scipy.stats.norm.pdf(x_high, mean_high, std_high), label = 'Mean = ' + str(mean_high) + ' std = ' + str(std_high))
            axs[list_koordinates[n]].hist(list_hr_data[n], bins, facecolor = 'green', alpha= 0.5, density=True)
            axs[list_koordinates[n]].set_xlabel('HR [Bpm]')
            axs[list_koordinates[n]].set_ylabel('Density of heart rate')
            axs[list_koordinates[n]].set_title('Phase ' + str(n+1), fontsize = MEDIUM_SIZE, fontweight = 'bold')
            axs[list_koordinates[n]].legend(loc = 'upper right', facecolor="white")
            axs[list_koordinates[n]].set_facecolor('whitesmoke')
            axs[list_koordinates[n]].grid(color = 'lightgrey')

        axs[list_koordinates[3]].set_facecolor('whitesmoke')
        axs[list_koordinates[3]].grid(color = 'lightgrey')


        fig.set_size_inches(20,10)
        fig.set_tight_layout('tight')
        fig.subplots_adjust(left=0.05, bottom=0.08, right=0.97, top=0.92, wspace=None, hspace=None)
        path = 'C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/Figurer/HR/Histogrammer/'
        title = 'Gaussian distributions, Testperson ' + str(self.testperson)
        fig.savefig(path + " " + title) #, dpi = 200)
        self.testperson+=1

    def get_mean_and_std_list(self):
        """Standard getmetode, der returnerer resultaterne for gmm metoden

        Returns:
            (list<dict>):liste med længden 3. På hver plads er et dictionary, der indeholder mean og std for begge fordelinger
        """
        # std_low = round(self.list_mean_std[n]["std_low"],2)
        # mean_low = round(self.list_mean_std[n]["mean_low"],2)
        return self.list_mean_std

    def __get_time(self, signal_avg, fs):
        """Bruges til at lave lineær regression. Her er krævet en tidsakse frem for bare indexer.

        Args:
            signal_avg (list<float>): det midlede hr signal
            fs (int): samelfrekvens for den brugte sensor

        Returns:
            8list): liste med tidsakse for hr_avg
        """
        delta_tid = 1/fs
        tid_avg = len(signal_avg)/fs
        tidsakse_avg = np.arange(0,tid_avg, delta_tid)
        return tidsakse_avg

    def linear_regression(self, signal_avg = [], fs = 4, index = 0):
        """Udfører lineær regression på den første del af signalet fra t = 0 til t = stabiliseringstid

        Args:
            signal_avg (list, optional):  det midlede hr signal. Default er [].
            fs (int, optional): samelfrekvens for den brugte sensor. Default er 4.
            index (int, optional): indexet hvor der er registreret stabiliseringsniveau. Default er 0.

        Returns:
            returnerer et arraylignende objekt med hældningen.
        """
        y = signal_avg[:index] # Vil kun lave lineær regression på data indtil det index hvor vi har fundet stabiliseringstiden
        X = self.__get_time(y, fs).reshape(-1,1)
        y = y.reshape(-1,1)
        reg = LinearRegression(copy_X=True).fit(X, y)
        reg.score(X, y)
        coef = reg.coef_
        dict_coefficients = {}
        dict_coefficients['coef'] = round(coef[0][0],3)
        dict_coefficients['intercept'] = round(reg.intercept_[0],3)
        self.coef_list.append(dict_coefficients)
        return coef

    def mean_high_data(self, hr_avg : list, index : int):
        """Beregner middelværdien af data fra t=0 til det givne index

        Args:
            hr_avg (list):  det midlede hr signal
            index (int): Det index hvor der er registreret stabiliseringsniveau

        Returns:
            (int): gennemsnittet af hr_avg i intervallet 0 < t <= index)
        """
        mean_high = sum(hr_avg[0:index-1])/index
        return mean_high
    
    def two_point_velocity(self, hr_begin : float, hr_mean:float, stabilization_time : float):
        """Beregner hældningen af den rette linje der går igennem de to punkter: 1) [0, hr_begin] 2) [stibilization_time, hr_mean]. Denne metode beregner altså hastigheden ved brug af two point velocity

        Args:
            hr_begin (float): den hr-værdi der skal bruges i punktet [0, hr_begin]. Det kan være den første hr,værdi, middelværdien af den første del af signalet eller den høje middelværdi fra GMM metoden
            hr_mean (float): stabiliseringsniveauet
            stabilization_time (float): Den tid det tog, før hr var stabil efter endt strestest.

        Returns:
            (float) : den beregnede hældning, svarende til hastigheden
        """
        self.list_velocity.append(round((hr_mean-hr_begin)/stabilization_time,2))
        return self.list_velocity[len(self.list_velocity)-1]

    def get_coefs(self):
        """Der returneres en liste med dictionary, der indeholder hældningen og skæringen for den libeære regression. Listen har længden 3 svarende til hælding og skæring for fase 1-3

        Returns:
            (list): Returnerer den ovenfr beskrevne liste. 
        """
        return self.coef_list

    def get_velocity_two_point(self):
        return self.list_velocity

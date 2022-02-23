import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import numpy as np
from sklearn.mixture import GaussianMixture as GMM
import math
class stabelisation_class():
    def __init__(self) -> None:
        pass
        
    def dispertion(self, signal, width = 20 , fs = 4):
        """Metoden bruger dispertion til at vurdere hvornår signalet er stabilt. Disperstion bruges i tidsdomænet. 

        Args:
            signal (list<float>): Denne liste indeholder signalet, der ønskes at finde stabiliseringsindexet på
            width (int, optional): Bredden af vinduet angivet i sekunder. Defaults to 20.
            fs (int, optional): Samplefrekvens for signalet. Default er 4, svarende til samplefrekvensen for HRM-Pro og Forerunner.

        Returns:
            index (int): Der returneres et index svarende til den midterste værdi når vinduet har en højde mindre end 10 BPM. De 10 BPM er fundet på baggrund af tidligere testmålinger
        """
        index = 0
        width_index = width*fs
        final_heights_list = []
        for i in range(len(signal)-width_index):
            window_content = []
            for n in range(width_index):
                window_content.append(signal[i+n])
            height = max(window_content) - min(window_content)
            final_heights_list.append(height)
        maximum = max(final_heights_list)
        reached_maximum = False
        n=0
        for height in final_heights_list:
            if(reached_maximum == True and height <=10):
                index = n
                break
            elif(height == maximum):
                reached_maximum=True
            n+=1

        # plt.plot(final_heights_list)
        # plt.show()
        return index

    def gmm(self, signal: list, counter = 0):
        # init_1, init_2 = self.__initial_parameters(signal)
        # means = np.array([[init_1+20],[init_2+20]])
        # gmm = GMM(n_components=2, means_init=means)
        gmm = GMM(n_components=2)
        
        reshaped = signal.reshape(-1,1)
        results = gmm.fit(reshaped)
        #print(str(counter) + " Low mean: " + str(min(results.means_)) + " High mean " + str(max(results.means_)))
        reached_maximum = False
        maximum = max(signal)

        self.std_low = math.sqrt(min(results.covariances_))
        self.std_high = math.sqrt(max(results.covariances_))
        self.mean_low = min(results.means_)[0]
        self.mean_high = max(results.means_)[0]

        limit = min(results.means_) + self.std_low*0
        n=0
        index = len(signal)-1
        for hr in signal:
            if(reached_maximum == True and hr <= limit):
                index = n
                break
            elif(hr == maximum):
                reached_maximum=True
            n+=1
            
        return index

    def __initial_parameters(self,signal):
        hr_list = self.__remove_X_percentages(signal,0)
        minimum = min(hr_list)
        maximum = max(hr_list)
        split = minimum + int(round((maximum-minimum)/2))
        high = []
        low = []
        for hr in hr_list:
            if(hr <= split):
                low.append(hr)
            else:
                high.append(hr)
        mean_low = sum(low)/len(low)
        mean_high = sum(high)/(len(high))

        return mean_low, mean_high

    def get_means(self):
        return self.mean_low, self.mean_high

    def get_stds(self):
        return self.std_low, self.std_high


    def soren(self, signal2, N, do_soren = False):
        if(do_soren == True):
            signal = self.__remove_X_percentages(signal2, 10)
            middle = self.__get_limit(signal)
            faktor_under = 1 # Denne faktor ganges under, for at gøre std mindre. 
            faktor_over = 1.5
            
            # Splitter signal i 2 ud fra den midterste hr værdi
            hr_low = []
            hr_high = []
            for hr in signal:
                if(hr >= middle):
                    hr_high.append(hr)
                else:
                    hr_low.append(hr)

            # Beregner middelværdi og std for de lave værdier i det nu splittede signal
            self.mean_low = round(np.mean(hr_low))
            self.std_low = np.std(hr_low)
            self.mean_high = round(np.mean(hr_high))
            self.std_high = np.std(hr_high)

            # Laver midling af hele signalet (Mooving average)
            hr_avg = self.__get_filtered_signal(signal, N)

            #Forlænger det midlede signal med data, til det er lige så langt som hr signalet
            # devider = int(round((len(signal)-len(hr_avg))/2))
            # forlaeng_high = [signal[0]]*(devider)
            # forlaeng_low = [mean]*(devider)
            # hr_avg = forlaeng_high + hr_avg.tolist() + forlaeng_low

            found_mean = False
            found_under = False
            found_over = False
            i = 0

            CI_mean = 0
            CI_std_under = 0
            CI_std_over = 0 

            #Bestemmer hvornår signalet første gange rammer hhv mean, mean-std*faktor_under og mean+std*self.faktor_over 
            for hr in hr_avg: #for hr in signal:
                if(round(hr) == self.mean_low and found_mean == False):
                    found_mean = True
                    found_under = False
                    CI_mean = i
                elif(round(hr) == round(self.mean_low-(self.std_low*faktor_under)) and found_under == False and found_mean == True):
                    found_under = True
                    break
                i+=1
            
            return CI_mean
        else:
            return 0

    def __remove_X_percentages(self,signal, percentage_to_remove):
        list_to_sort = signal.copy()
        if(percentage_to_remove != 0):
            list_to_sort.sort()
            length_of_list = len(list_to_sort)
            amount_to_remove = int(round((length_of_list/100)*percentage_to_remove))
            from_end = length_of_list-amount_to_remove
            list_to_sort = list_to_sort[amount_to_remove-1:from_end] # Fjerne de laveste og højeste 10 %
            # list_to_sort = list_to_sort[0:from_end] # Fjerner kun de højeste 10 %
        return list_to_sort

    def __get_filtered_signal(self, raw_signal, average_value):
        N = average_value
        if(N%2 == 0):
            N+=1
        hr_avg = np.convolve(raw_signal, np.ones(N)/N, mode='same')
        hr_return = hr_avg[N:len(hr_avg)-N]
        return hr_return

    def __get_limit(self, hr_list):
        max_val = max(hr_list)
        min_val = min(hr_list)

        middle = min_val + round((max_val-min_val)/2)

        return middle
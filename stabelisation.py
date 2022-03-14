import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import numpy as np
from sklearn.mixture import GaussianMixture as GMM
import math
class stabelisation_class():
    def __init__(self) -> None:
        pass
    
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

    def get_means(self):
        return round(self.mean_low,2), round(self.mean_high,2)

    def get_stds(self):
        return self.std_low, self.std_high
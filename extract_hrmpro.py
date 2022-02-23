

from IExtract import IExtract
from filereader import filereader_class
from tidskorrigering import tidskorrigering_class
from Calculate_RR_class import *


class extract_hrmpro_class(IExtract):
    def __init__(self, filereader: filereader_class, tidskorrigering: tidskorrigering_class, calculate_RR: Caculate_rr_class) -> None:
        self.filereader = filereader
        self.tidkorr = tidskorrigering
        self.rr_calculator = Caculate_rr_class()
        self.read_from_file = True
        self.lines_splitted = []

    def extract_new(self, testpersonnummer : int, timelim_begin: int, timelim_end : int, fase: int):
        """Metoden udtrækker HR og RR. Det er også via denne metode der tidskorrigeres, så tidsintervallerne kan sammenlignes på tværs af sensorer
            RR-værdierne virker dog til at være presset sammen, som om der mangler en værdi. Dette kan skyldes, at nogle gange fejler en pakke (82286937 : Rx fail)

        Args:
            testpersonnummer (int): nummeret på den testperson man er ved at udtrække data fra. Bruges i filereader
            timelim_begin (int): Tidspunktet hvorfra der skal gemmes data. Dette er det første tidspunkt i Maxrefdes103 data grundet forsøgets opsætning.
            timelim_end (int): Tidspunktet, hvor man ikke længere skal bruge data
        """
        if(self.read_from_file):
            self.lines_from_file = self.filereader.read_HRMpro(testpersonnummer)
            self.read_from_file = False
        self.lines_splitted = self.tidkorr.garmin(self.lines_from_file, timelim_begin, timelim_end)
        self.hr_list = []
        oldtogglebit = 0
        self.list_of_rr_and_time = []
        # I den hexadecimale streng udtrækkes hver byte og gemmes i et dictionary sammen med den udregnede tid
        #self.New_list_with_logged_values_as_dictionay = []
        t = 0
        results_dict = {}
        FirstTime=True
        self.rr_calculator.set_first_time()
        for sensordata in self.lines_splitted:
            dictionary_with_hex ={} 
            if len(sensordata) == 3:
                if 'Rx' in sensordata[1]:
                    temporary_List = sensordata[2][1:-2].split('][')
                    if(temporary_List[0][2] == '0'):
                        self.hr_list.append('3C')
                    else: #(temporary_List[0][2] == '4'):    
                        self.hr_list.append(temporary_List[7])
                    newTogglebit = int(temporary_List[6],16)
                    if(oldtogglebit != newTogglebit): #Yderligere gemmes kun data, når der har været et nyt 'heart-beat-event svarende til at hr_count er blevet en større
                        dictionary_with_hex["b0"] = temporary_List[0][1:]
                        dictionary_with_hex["b1"] = temporary_List[1]
                        dictionary_with_hex["b2"] = temporary_List[2]
                        dictionary_with_hex["b3"] = temporary_List[3]
                        dictionary_with_hex["LSB"] = temporary_List[4]
                        dictionary_with_hex["MSB"] = temporary_List[5]
                        dictionary_with_hex["hr_count"] = temporary_List[6]
                        dictionary_with_hex["hr"] = temporary_List[7]
                        dictionary_with_hex["time"] = sensordata[0]
                        number_of_repeat = 1
                        if(oldtogglebit != newTogglebit-1 and newTogglebit != 0 and FirstTime == False):
                            number_of_repeat = newTogglebit-oldtogglebit
                            # for n in range(number_of_repeat):
                            #     self.list_of_rr_and_time.append(results_dict)
                        results_dict = self.rr_calculator.rr_4_new(dictionary_with_hex)
                        # if(number_of_repeat> 2):
                        #     results_dict['rr'] = results_dict['rr']/number_of_repeat
                        #     print( "Testperson: " + str(testpersonnummer) + " Fase " + str(fase) + " RR: " + str(results_dict['rr']) + " Antal gange: " + str(number_of_repeat) + ", t = " + str(t))
                        #     for n in range(number_of_repeat):
                        #         self.list_of_rr_and_time.append(results_dict)
                        #         t+=1
                        # else:
                        #     t+=1
                        #     self.list_of_rr_and_time.append(results_dict)
                        self.list_of_rr_and_time.append(results_dict)
                    oldtogglebit = newTogglebit
                    FirstTime = False
            elif 'Rx' in sensordata[1] and len(self.hr_list) > 0: #hvis data er på formen 8795535 : RX fail
                self.hr_list.append(self.hr_list[len(self.hr_list)-1])
        #Bruger data page 4 til at omregne til RR-værdier
        #self.list_of_rr_and_time = self.rr_calculator.rr_4(self.New_list_with_logged_values_as_dictionay)
        return self.list_of_rr_and_time

    def extract(self, testpersonnummer : int, timelim_begin: int, timelim_end : int):
        """Metoden udtrækker HR og RR. Det er også via denne metode der tidskorrigeres, så tidsintervallerne kan sammenlignes på tværs af sensorer
            RR-værdierne virker dog til at være presset sammen, som om der mangler en værdi. Dette kan skyldes, at nogle gange fejler en pakke (82286937 : Rx fail)

        Args:
            testpersonnummer (int): nummeret på den testperson man er ved at udtrække data fra. Bruges i filereader
            timelim_begin (int): Tidspunktet hvorfra der skal gemmes data. Dette er det første tidspunkt i Maxrefdes103 data grundet forsøgets opsætning.
            timelim_end (int): Tidspunktet, hvor man ikke længere skal bruge data
        """
        if(self.read_from_file):
            self.lines_from_file = self.filereader.read_HRMpro(testpersonnummer)
            self.read_from_file = False
        self.lines_splitted = self.tidkorr.garmin(self.lines_from_file, timelim_begin, timelim_end)
        self.hr_list = []
        oldtogglebit = 0
        # I den hexadecimale streng udtrækkes hver byte og gemmes i et dictionary sammen med den udregnede tid
        self.New_list_with_logged_values_as_dictionay = []
        for sensordata in self.lines_splitted:
            dictionary_with_hex ={} 
            if len(sensordata) == 3:
                if 'Rx' in sensordata[1]:
                    temporary_List = sensordata[2][1:-2].split('][')
                    if(temporary_List[0][2] == '0'):
                        self.hr_list.append('3C')
                    else: #(temporary_List[0][2] == '4'):    
                        self.hr_list.append(temporary_List[7])
                    newTogglebit = int(temporary_List[6],16)
                    # if(oldtogglebit != newTogglebit-1):
                    #     self.hr_list.append(temporary_List[7]) 
                    if(oldtogglebit != newTogglebit): #Yderligere gemmes kun data, når der har været et nyt 'heart-beat-event svarende til at hr_count er blevet en større
                        dictionary_with_hex["b0"] = temporary_List[0]
                        dictionary_with_hex["b1"] = temporary_List[1]
                        dictionary_with_hex["b2"] = temporary_List[2]
                        dictionary_with_hex["b3"] = temporary_List[3]
                        dictionary_with_hex["LSB"] = temporary_List[4]
                        dictionary_with_hex["MSB"] = temporary_List[5]
                        dictionary_with_hex["hr_count"] = temporary_List[6]
                        dictionary_with_hex["hr"] = temporary_List[7]
                        dictionary_with_hex["time"] = sensordata[0]
                        if(oldtogglebit != newTogglebit-1):
                            self.New_list_with_logged_values_as_dictionay.append(dictionary_with_hex)
                            self.hr_list.append(temporary_List[7])   
                        self.New_list_with_logged_values_as_dictionay.append(dictionary_with_hex)
                    oldtogglebit = int(temporary_List[6],16)
            elif 'Rx' in sensordata[1] and len(self.hr_list) > 0: #hvis data er på formen 8795535 : RX fail
                self.hr_list.append(self.hr_list[len(self.hr_list)-1])
        
        #Bruger data page 4 til at omregne til RR-værdier
        self.list_of_rr_and_time = self.rr_calculator.rr_4(self.New_list_with_logged_values_as_dictionay)
        return self.list_of_rr_and_time

    def get_rr(self):
        """ Metoden returnerer en liste med rr-værdier.

        Returns:
            List<float>: Rr returneres som en liste med floats
        """
        # Modificerer rr-værdierne ved at udtrække rr værdier uden tiden.
        rr = []
        if len(self.list_of_rr_and_time) > 0:
            for dict in self.list_of_rr_and_time:
                rr.append(dict['rr'])
        else:
            #print("please extract rr data with the extract_rr_values-method before getting the rr-values in a separate list")
            pass
        return rr

    def get_time_rr(self):
        time = []
        first_time = self.list_of_rr_and_time[0]['time']
        if len(self.list_of_rr_and_time) > 0:
            for dict in self.list_of_rr_and_time:
                time.append((dict['time']-first_time)/1000)
        else:
            #print("please extract rr data with the extract_rr_values-method before getting the rr-values in a separate list")
            pass
        return time

    
    def get_hr(self):
        """ Metoden returnerer en liste med Hr-værdier.

        Returns:
            List<float>: Hr returneres som en liste med floats
        """
        hr_list = []
        for hr in self.hr_list: #self.New_list_with_logged_values_as_dictionay:
            hr_list.append(int(hr,16))
        return(hr_list)

    def set_read_from_file_bool(self, value : bool):
        """ Denne bool bruges til at fortælle extract_empatic metoden, at nu skal der indlæses data fra en ny testperson. 
            Dette er implementeret for at data kun indlæses en gang pr. testperson, og ikke 3 gange svarende til de 3 faser
        
        Args:
            value (bool): True hvis vi skal i gang med en ny testperson, False hvis vi er i gang med samme testperson, men bare fase 2 og 3
        """
        self.read_from_file = value


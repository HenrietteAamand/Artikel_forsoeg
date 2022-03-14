class Caculate_rr_class:
    def __init__(self) -> None:
        self.first_time = True
        self.old_time = 0
        self.old_time_str = ''
    def rr_0(self, Values_in_Hex_List): 
        """Metode til at udtrække RR fra SimulANT+ datapage 0. Bruges eksempelvis ved Garmin Foreunner 45, og i tilfælde af, at datapage 4 ikke er tilstede. 

        Args:
            Values_in_Hex_List (list<string>): Indputparameteren er en liste med alle de værdier der ønskes at beregnes RR og HR på

        Returns:
            List<Dict>: Der returneres en liste med et dictionary med 2 keys, nemlig 'time' og 'rr'
        """
        old_time = 0
        new_time = 0
        first_time = True
        listOfRR = []
        rollover = False
        for dict in Values_in_Hex_List:
            if(dict['b0'][2] == '0'):
                dict_rr_and_temp = {}
                temperaryString = dict['MSB'] + dict['LSB']            
                if first_time == True:
                    old_time = int(temperaryString,16) #HeartBeatEventTime (message 1: byte 4|5)
                    first_time = False
                else:
                    new_time = int(temperaryString,16) #HeartBeatEventTime (message 2: byte 4|5)
                    rr = ((new_time-old_time)*1000)/1024
                    # Tjekker og Korrigerer for et evt. rollover
                    if(old_time > new_time):
                        new_time += 65535
                        rollover = True
                    rr = ((new_time-old_time)*1000)/1024
                    if(rollover == True): 
                        new_time -= 65535
                        rollover = False
                    old_time = new_time
                    # Opretter liste med dictionaries med hhv tiden og rr-værdien til dette tidspunkt
                    # rr tilføjes kun hvis der er beregnet en ny værdi
                    if(rr != 0.0):
                        dict_rr_and_temp['time'] = dict['time']
                        dict_rr_and_temp['rr'] = rr
                        listOfRR.append(dict_rr_and_temp)
        return listOfRR

    def rr_4(self, Values_in_Hex_List): #Brug 4, fordi det giver altid de rigtige data modsat datapage 0. 
        """Metode til at udtrække RR fra SimulANT+ datapage 4 Bruges eksempelvis vi Garmin HRM-pro.

        Args:
            Values_in_Hex_List (list<string>): Indputparameteren er en liste med alle de værdier der ønskes at beregnes RR og HR på

        Returns:
            List<Dict>: Der returneres en liste med et dictionary med 2 keys, nemlig 'time' og 'rr'
        """
        # Defnerer tomme variabler til senere brug
        old_time = 0
        new_time = 0
        listOfRR = []
        oldrr = 0
        rollover = False
        first_time = True
        multiplikator = 0.961
        i =1
        old_toggle = ''
        for dict in Values_in_Hex_List:
            dict_rr_and_temp = {}
            if(dict['b0'][2] == '4'):
                old_time_str =  dict['b3'] + dict['b2']#PreviousHeartBeatEventTime (byte 2|3) OBS! Det skal vende med b3 først og b2 efter
                old_time = int(old_time_str,16)
                new_time_str = dict['MSB'] + dict['LSB']#HeartBeatEventTime (byte 4|5)
                new_time = int(new_time_str,16)
                # Tjekker og Korrigerer for et evt. rollover
                if(old_time > new_time): # and dict['b0'][2] == '4'):
                    new_time += 65535
                    rollover = True
                rr = ((new_time-old_time)*1000)/1024
                if(rollover == True): 
                    new_time -= 65535
                    rollover = False
                
                # Opretter liste med dictionaries med hhv tiden og rr-værdien til dette tidspunkt
                # rr tilføjes kun hvis der er beregnet en ny værdi
                if (oldrr != rr): # and dict['b0'][2] == '4'):
                    dict_rr_and_temp['time'] = dict['time']
                    dict_rr_and_temp['rr'] = rr*multiplikator
                    listOfRR.append(dict_rr_and_temp)
                oldrr = rr
            # elif(dict['b0'][2] == '0'): #Hvis vi er disconnected fra HRM-pro, så skal vi bruge forerunner protokollen
            #     toggel= dict['hr_count']
            #     #print("old toggle: " + old_toggle + ", new toggle: " + toggel)
            #     if(toggel != old_toggle):
            #         dict_rr_and_temp['time'] = dict['time']
            #         dict_rr_and_temp['rr'] = 1000
            #         listOfRR.append(dict_rr_and_temp)
            #     old_toggle = toggel                        

            i += 1
        return listOfRR

    def rr_4_new(self, dict_values_in_hex): #Brug 4, fordi det giver altid de rigtige data modsat datapage 0. 
        """Metode til at udtrække RR fra SimulANT+ datapage 4 Bruges eksempelvis vi Garmin HRM-pro.

        Args:
            Values_in_Hex_List (list<string>): Indputparameteren er en liste med alle de værdier der ønskes at beregnes RR og HR på

        Returns:
            List<Dict>: Der returneres en liste med et dictionary med 2 keys, nemlig 'time' og 'rr'
        """
        # Defnerer tomme variabler til senere brug
        rollover = False
        multiplikator = 1#0.961
        dict_rr_and_temp = {}
        new_time_str = dict_values_in_hex['MSB'] + dict_values_in_hex['LSB']#HeartBeatEventTime (byte 4|5)
        new_time = int(new_time_str,16)
        if(dict_values_in_hex['b0'][1] == '4'):
            self.first_time = False
            self.old_time_str =  dict_values_in_hex['b3'] + dict_values_in_hex['b2']#PreviousHeartBeatEventTime (byte 2|3) OBS! Det skal vende med b3 først og b2 efter
            self.old_time = int(self.old_time_str,16)
        else:
            if(self.first_time):
                self.old_time_str = dict_values_in_hex['MSB'] + dict_values_in_hex['LSB'] # HeartBeatEventTime (byte 4|5)
        # Tjekker og Korrigerer for et evt. rollover
        if(self.old_time > new_time): # and dict['b0'][2] == '4'):
            new_time += 65535
            rollover = True
        if (self.first_time):
            dict_rr_and_temp['time'] = dict_values_in_hex['time']
            dict_rr_and_temp['rr'] = 600 #Jeg sætter vare noget random ind på plads
            self.first_time = False
        else:
            rr = ((new_time-self.old_time)*1000)/1024
            dict_rr_and_temp['time'] = dict_values_in_hex['time']
            dict_rr_and_temp['rr'] = rr*multiplikator
            if(rr > 2000):
                rr = rr
            
        
        if(rollover == True): 
            new_time -= 65535
            rollover = False
            
        self.old_time = new_time

        return dict_rr_and_temp

    def set_first_time(self):
        self.first_time = True
        self.old_time = 0

import datetime, time
from typing import List
class tidskorrigering_class:
    def garmin(self, list_of_data1: list, timelim_begin: int, timelim_end: int):
        """Ud fra en liste med data, hvor der også skal indgå tidsværdier, tidskorrigeres ud fra de givbne grænseværdier

        Args:
            list_of_data (list<string>): Listen ideholder alle dataværdier som strings på formen: "81809671 : Rx: [04][00][EC][6F][DC][74][A4][38] [description]"
            timelim_begin (int): Grænseværdien for den første måling der skal medtages, inklusiv denne værdi
            timelim_end (int): Grænseværdien for den sidste måling der skal medtages, inklusiv denne værdi

        Returns:
            list<array[]>: Der returneres en liste, der udelukkende indeholder værdier inden for det angivne tidsinterval, begge grænseværdier inklusiv. Listen indeholder arrays på formen [1636471068000, ' Rx', ' [04][00][6E][A2][14][A5][B6][5B]\n']. Her er sensorcpunt altså korrigeret til en tidsværdi med dags dato
        """
        list_of_data = list_of_data1.copy()
        list_splitted_data = []
        timecorrected_list = []
        i = -3
        for line in list_of_data:
            if(i >= 0):
                list_splitted_data.append(line.split(':'))
                list_splitted_data[i][0] = self.__get_timestamp_garmin(float(list_splitted_data[i][0])) #Ændrer sensorcountet til et unix timestamp
                if(list_splitted_data[i][0] >= timelim_begin and list_splitted_data[i][0] <= timelim_end):
                    timecorrected_list.append(list_splitted_data[i])
            i += 1
        return timecorrected_list


    def empatica(self, data_list : list, timelim_begin: int, timelim_end : int, datatype : str):
        """Ud fra en liste med data, hvor der også skal indgå tidsværdier, tidskorrigeres ud fra de givne grænseværdier

        Args:
            data_list (list<Dict>): Listen ideholder alle dataværdier som et dictionary med 2 keys, hvoraf den ene skal være 'time', mens den sidste specificers gennem parametren 'datatype'
            timelim_begin (int): Grænseværdien for den første måling der skal medtages, inklusiv denne værdi
            timelim_end (int): Grænseværdien for den sidste måling der skal medtages, inklusiv denne værdi
            datatype (str): Specificere den sidste key, eks 'rr' eller 'hr'

        Returns:
            list<float>: Der returneres en liste med floats, der udelukkende indeholder værdier inden for det angivne tidsinterval, begge grænseværdier inklusiv. Listen indeholder de data der er specificeret via datatype parametren
        """
        return_list = []
        return_list_time = []
        first_time = 0
        for data in data_list:
            if(data['time'] >= timelim_begin and data['time'] <= timelim_end):
                if(first_time == 0):
                    first_time = float(data['time'])
                return_list.append(data[datatype])
                return_list_time.append((float(data['time']-first_time))/1000)
            if(data['time'] > timelim_end):
                break
        return return_list, return_list_time

    def __get_timestamp_garmin(self, current_count: int):
        """Metoden ændre garmins sensorcount til et UNIX timestamp med dags dato. Klokkeslettet beregnes ud fra Et kendt unix timestamp til et specifikt sensorcount, og dette specificeres gennem initierings metoden

        Args:
            current_count (int): Current count er det sensorcount der findes i logfilen som det første tal, eks 81809671 i logentrien "81809671 : Rx: [04][00][EC][6F][DC][74][A4][38] [description]"

        Returns:
            int : Der returneres et UNIX timestamp med dags dato som dato.
        """
        current_absolute_time = self.birthtime_sensor+current_count
        # tid_forkert_dato = str(datetime.datetime.now().date().strftime("%d/%m/%y")) + " " + str(datetime.datetime.fromtimestamp(current_absolute_time/1000).strftime('%H:%M:%S.%f'))
        # my_datetime = datetime.datetime.strptime(tid_forkert_dato, '%d/%m/%y %H:%M:%S.%f')
        # #absolute_time = int((time.mktime(my_datetime.timetuple())*1000))
        # absolute_time = datetime.datetime.timestamp(my_datetime)*1000
        # return absolute_time
        return current_absolute_time

    def set_birthtime_sensor(self, absolute_time: int, sensorcount_at_absolute_time : int):
        """Bruges til at sætte birthcount, så når der indlæses data fra en ny sensor der skal tidskorrigeres, så skal birthcount justeres

        Args:
            absolute_time (int): Unix timestamp til det sensorcount
            sensorcount_at_absolute_time (int): Sensorcount til det tilhørende Unix timestamp
        """
        self.birthtime_sensor = int(absolute_time)-int(sensorcount_at_absolute_time)
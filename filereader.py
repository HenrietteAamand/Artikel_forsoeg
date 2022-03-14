import csv, os.path, json

class filereader_class:
    def __init__(self, path, filename = "") -> None:
        self.path = path
        self.filename = filename

    def read_data(self, filename: str):
        full_path = self.path + filename + ".csv"
        file =  open(full_path, mode='r', newline='')
        lines_from_logfile = list(csv.reader(file)) 
        file.close()
        return lines_from_logfile

    def save_results(self, list_to_save: list, filename : str):
        """Når der er beregnet stabiliseringstider, hastigheder m.v. så gemmes disse via denne metode. Data er blevet brugt i R-tudio til de statistiske beregninger. 

        Args:
            list_to_save (list): En liste med dictionaries der indeholder de data der ønskes gemt.   
            filename (str): Filnavnet på de resultater der skal gemmes
        """
        keys = list_to_save[0].keys()
        #output_file = open('C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/Data/' + filename, 'w+', newline='')
        output_file = open("C:/Users/Bruger/Documents/GitHub/Praktik/Artikel_forsoeg/Data/" + filename, 'w+', newline='')
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_to_save)
    # def read_HRMpro(self, testpersonnummer: int):
    #     """Metoden læser data fra den logfil, der genereres når man bruger SimulANT+ til at læse data der sendes fra en Garmin(R) ANT+ sensor. 
    #        Der indlæses en liste, hvor hver plads i listen indeholder en linje fra logfilen på formen '81809171 : Rx: [04][00][88][6B][EC][6F][A3][39]', svarende til datapage 4
    #        Der er ikke en fælles read_metode for garmin, da filnavnene og dermed filstien er forskellig.

    #     Args:
    #         testpersonnummer (int): nummer på testpersonnumer fra forøget. Bruges til at åbne den rigtige fil tilhørende den rigtige person. 

    #     Returns:
    #         lines_from_logfile (list<string>): Returnerer en liste med strings svarende til hver linje i logfilen
    #     """
    #     hrmpro_path = self.path + "/Testperson_" + str(testpersonnummer) + "/SimulANT+ Logs - HRM-Pro/"
    #     filename = "Heart Rate Display ANT Messages.txt"
    #     fullpath = hrmpro_path + filename
    #     file = open(fullpath, 'r')
    #     lines_From_Logfile = file.readlines()
    #     return lines_From_Logfile

    # def read_forerunner(self, testpersonnummer: int):
    #     """Metoden læser data fra den logfil, der genereres når man bruger SimulANT+ til at læse data der sendes fra en Garmin(R) ANT+ sensor. 
    #        Der indlæses en liste, hvor hver plads i listen indeholder en linjje fra logfilen på formen '81722734 : Rx: [00][FF][FF][FF][86][02][9F][38]'

    #     Args:
    #         testpersonnummer (int): nummer på testpersonnumer fra forøget. Bruges til at åbne den rigtige fil tilhørende den rigtige person. 

    #     Returns:
    #         lines_from_logfile (list<string>): Returnerer en liste med strings svarende til hver linje i logfilen
    #     """
    #     forerunner_path = self.path + "/Testperson_" + str(testpersonnummer) + "/SimulANT+ Logs - forerunner/"
    #     filename = "Heart Rate Display ANT Messages.txt"
    #     fullpath = forerunner_path + filename
    #     file = open(fullpath, 'r')
    #     lines_From_Logfile = file.readlines()
    #     return lines_From_Logfile

    # def read_empatica(self, testpersonnummer: int,datatype: str):
    #     """Metoden indlæser data fra den ønskede empatica logfil.

    #     Args:
    #         testpersonnummer (int): Nummeret på testpersonen
    #         datatype (str): Initialerne for det data der skal indlæses. Muligheder: ACC, BVP, EDA, HR, IBI, tags og TEMP

    #     Returns:
    #         lines_from_logfile (list<string>): Returnerer en liste med strings svarende til hver linje i logfilen
    #     """
    #     empatica_path = self.path + "/Testperson_" + str(testpersonnummer) + "/Empatica/" + datatype + ".csv"
    #     file =  open(empatica_path, mode='r', newline='')
    #     lines_from_logfile = list(csv.reader(file)) 
    #     file.close()
    #     return lines_from_logfile
    
    # def read_maxrefdes_Raa_observationer(self, testpersonnummer: int, fasenummer: int):
    #     """Metoden læser data ind fra de rå onservationer, hvor der kan udtrækkes både RR, hr, timestamps m.v. Data indlæses som en .csv fil, og indlses inds i et dictionary

    #     Args:
    #         testpersonnummer (int): nummer på testpersonnumer fra forøget. Bruges til at åbne den rigtige fil tilhørende den rigtige person. 
    #         fasenummer (int): nummer på fasen, der bruges til at åbne den rigtige fil

    #     Returns:
    #         list<Dict>: Der returneres en liste med dictionaries. Der er følgende entries i dictionariet: timestmp,smpleCnt,grnCnt,led2,led3,grn2Cnt,irCnt,redCnt,accelX,accelY,accelZ,hr,rr,rrsecure,spo2. Timestamp angives som et klokkeslet uden dato 
    #     """
    #     i = 0
    #     faser = ["Baseline","Stilhed", "Statisk", "Dynamisk"]

    #     for i in range(len(faser)):
    #         maxrefdes_path = self.path + "/Raaobservationer/Testperson_" + str(testpersonnummer) + "_Fase_" + str(fasenummer) + "_" + faser[i] + "_observationer.csv"
    #         if(os.path.exists(maxrefdes_path)):
    #             i = 3
    #             csv_file_original =  open(maxrefdes_path, mode='r')
    #             #print(maxrefdes_path)
    #             lines_as_dict = csv.DictReader(csv_file_original, delimiter = ',')
    #             lines_as_dict = list(lines_as_dict)
    #             csv_file_original.close()
    #             return lines_as_dict


    # def read_dict_to_list(self, rest_of_path : str):
    #     """Metoden indlæser en .csv fil som en liste med dictionaries. det bruges i programmet til to .csv filer:
    #        Der er lavet en .csv fil der indeholder sammenhængen mellem et rent faktisk Unix epoch timestamp, og sensorcount på SimulANT+ displayet. 
    #        Denne fil indlæses her, så Garmin sensorerne kan få et reelt timestamp der kan sammenlignes med Maxrefdes tidsgrænser 
    #        Derudover indlæses en .csv fil, der indeholder information om hvilken intervention der var i hvilken fase. Denne information bruges primært til at plotte figurerne og til at gemme stabiliseringshastighed og niveau relativt til en intervention.

    #     Returns:
    #         lines_as_dict: (list<string>): Dette er en liste med dictionary der indeholder information om sensorcount og absolute count. En linje er på formen '{'Testperson_nr': '1', 'Absolute_count': '1635761570409', 'Sensor_count': '63780218'}
    #     """
    #     path = self.path + rest_of_path #"/sensorcount.csv"
    #     csv_file_original =  open(path, mode='r')
    #     lines_as_dict = csv.DictReader(csv_file_original, delimiter = ';')
    #     lines_as_dict = list(lines_as_dict)
    #     csv_file_original.close()
    #     return lines_as_dict     

     

    # def save_hr_data(self, data, filename: str):
    #     """Når alle HR data er indlæst, tidskorrigere og inddelt i faser, så gemmes de i en stor .csv fil, så næste gang programmet køres
    #     Dermed behøver man ikke indlæse samtlige data og tidskorrigere på ny. Dette tidsoptimerer processen, når data skal sammenlignes, og man dermed kører et program mange gange 

    #     Args:
    #         data (Dict<dict<key, list<float>>): Dette er et dictionary, med alt informationen pr testperson.  
    #                                             En linje er på formen DATA_SENSOR_FASENR, eksempelvis: Hr_maxrefdes_3
    #                                             Udsnit: {1: {'Hr_Maxrefdes103_0': [...], 'RR_Maxrefdes103_0': [...], 'Hr_Hrmpro_0': [...], 'RR_Hrmpro_0': [...], 'Hr_Forerunner_0': [...], 'RR_Forerunner_0': [...], 'Hr_Empatica_0': [...], 'RR_Empatica_0': [...], 'Hr_Maxrefdes103_1': [...], ...}}

    #     """
    #     full_path = self.path + filename
    #     data_file = open(full_path, 'w+', newline='') 
    #     csv_writer = csv.writer(data_file, delimiter=';')
    #     string = json.dumps(data[1], default=lambda o: o.__dict__, sort_keys=False, indent=4)
    #     json_obj = json.loads(string)
    #     header = json_obj.keys()
    #     csv_writer.writerow(header)
        
    #     # Gemmer data som JSON objekter
    #     i=1
    #     while i <= len(data):
    #         string = json.dumps(data[i], default=lambda o: o.__dict__, sort_keys=False, indent=4)
    #         json_obj = json.loads(string)
    #         csv_writer.writerow(json_obj.values())
    #         i+=1
    #     data_file.close()
        
    # def read_hr_data(self, filename : str):
        # """I stedet for at indlæse data gennem samtlige af de originale datafiler, så kan data i stedet indlæses med denne metode, forudsat data på et tidspunkt er blev gemt med metoden 'save_hr_data' 

        # Returns:
        #     dict_data (dict<dict<key,value>>): Der returneres et dictionary magen til det dictionary der er blevet oprettet, efter alle data er tidskorrigeret m.v. (se forklaring på format i save_hr())
        # """
        # full_path = self.path + filename #'C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/' + filename
        # csv_file_original =  open(full_path, mode='r')
        # lines_as_dict = csv.DictReader(csv_file_original, delimiter = ';')
        # i = 1
        # dict_data = {}
        # for line in lines_as_dict:
        #     dict_data[i] = line
        #     i+=1
        # csv_file_original.close()
        # i = 1
        # for key in dict_data:
        #     for dataset_key in  dict_data[key]:
        #         string = dict_data[key][dataset_key]
        #         dict_data[key][dataset_key] = json.loads(string)
        #     i+=1
        # return dict_data




        

    
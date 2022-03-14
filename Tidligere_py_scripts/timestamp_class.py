import csv
import datetime, time

class timestamp_class():
    def __init__(self) -> None:
        pass

    def get_dict_with_timestamps(self, filepath : str, filename: str):
        full_path = filepath+filename
        file =  open(full_path, mode='r', newline='')
        lines_from_logfile = list(csv.reader(file)) 
        file.close()

        list_with_dict = []
        list_keywords = lines_from_logfile[0][0].split(';')
        firsttime = True
        for line in lines_from_logfile :
            if(firsttime == False):
                temp_dict = {}
                list_data = line[0].split(';')
                temp_dict[list_keywords[0]] = int(list_data[0])
                temp_dict[list_keywords[1]] = int(list_data[1])
                temp_dict[list_keywords[2]] = int(list_data[2])
                temp_dict[list_keywords[3]] = int(list_data[3])
                list_with_dict.append(temp_dict)
            else:
                firsttime = False

        return list_with_dict

    def correct_timestamp(self, timestamp : str):
        last_datetime = datetime.datetime.strptime(timestamp, '%d/%m/%y %H:%M:%S.%f')
        absolute_time = int("{:.0f}".format(time.mktime(last_datetime.timetuple())*1000))
        return absolute_time

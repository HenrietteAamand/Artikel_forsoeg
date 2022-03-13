class sort_data_class:
    def __init__(self) -> None:
        pass

    def sort(self, timelimits_list = [], data_list = [], testperson_nr = 0, gennemloeb = 0):
        testperson_dict = {}
        testperson_dict['Reference'] = []
        testperson_dict['Statisk'] = []
        testperson_dict['Dynamisk_2'] = []
        testperson_dict['Dynamisk_10'] = []
        for n in range(4):
            where = gennemloeb*4 +(1 + n)
            temporary_timelist = timelimits_list[where][0].split(';')
            begin = int(temporary_timelist[3])
            end = int(temporary_timelist[4])
            phase = temporary_timelist[2]
            first_time = True
            hr = []
            tider = []
            for datapoint in data_list:
                if(first_time == True or datapoint == []):
                    first_time = False
                else:
                    # 0: timelimit, 2:hr
                    if(float(datapoint[0]) >= begin and float(datapoint[0]) <= end):
                        hr.append(int(datapoint[2]))
                        tider.append(float(datapoint[0])-begin)
                    elif(float(datapoint[0]) > end):
                        break
            testperson_dict[phase] = hr
            time_name = phase + '_tid'
            testperson_dict[time_name] = tider
        return testperson_dict

    
            



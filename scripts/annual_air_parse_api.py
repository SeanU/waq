import sys
import csv

input_file = '/Users/ankittharwani/Junk/annual_all_2016.csv'

for line in csv.reader(open(input_file, 'rb'), quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL):
    if ("State" not in line[0]):
        cont_id = int(line[3])
        if (cont_id in (42101,42401,42602,44201,81102,88101,88502)):
            metric = line[11]
            if (metric == "Observed Values" or metric == "Obseved hourly values" or metric == "Daily maximum of 8-hour running average"):
                value = float(line[27])
                status=""
                if(cont_id == 44201):
                    # Ozone
                    if (value > 0.164):
                        status = "red"
                    elif (value > 0 and value < 0.164):
                        status = "amber"

                elif(cont_id == 42401):
                    # SO2
                    if (value > 185):
                        status = "red"
                    elif (value > 35 and value <= 185):
                        status = "amber"
                    elif (value < 35):
                        status = "green"

                elif(cont_id == 42101):
                    # CO
                    if (value > 12.4):
                        status = "red"
                    elif (value > 4.4 and value <= 12.4):
                        status = "amber"
                    elif (value < 4.4):
                        status = "green"

                elif(cont_id == 42602):
                    # NO2
                    if (value > 360):
                        status = "red"
                    elif (value > 53 and value <= 360):
                        status = "amber"
                    elif (value < 53):
                        status = "green"

                elif(cont_id == 88101 or cont_id == 88502):
                    # PM2.5
                    if (value > 55.4):
                        status = "red"
                    elif (value > 12 and value <= 55.4):
                        status = "amber"
                    elif (value < 12):
                        status = "green"

                elif(cont_id == 81102):
                    # PM10
                    if (value > 253):
                        status = "red"
                    elif (value > 54 and value <= 253):
                        status = "amber"
                    elif (value < 54):
                        status = "green"

                print('\t'.join((line[1],
                                 line[49],
                                 str(int(line[0])),
                                 line[50],
                                 "Air",
                                 line[54],
                                 "00:00:00",
                                 "Gases",
                                 line[8],
                                 line[27],
                                 status,
                                 "1",
                                 line[3],
                                 line[5],
                                 line[6])))

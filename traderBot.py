# importing the requests library
import requests
import coinbase
from datetime import datetime, date, time, timedelta
import csv
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM

import pandas as pd


# api-endpoint
URL = "https://api.pro.coinbase.com/products/BTC-USD/candles"
# defining a params dict for the parameters to be sent to the API


def yearsago(years, from_date=None):
    if from_date is None:
        from_date = datetime.now()
    try:
        return from_date.replace(year=from_date.year - years)
    except ValueError:
        # Must be 2/29!
        assert from_date.month == 2 and from_date.day == 29 # can be removed
        return from_date.replace(month=2, day=28, year=from_date.year-years)

def years_to_timedelta(begin, end):
    # if begin <= datetime(month=2, day=28):
    #     begin_year = begin.year
    # else:
    #     begin_year = begin.year+1
    #
    # if end >= datetime(month=3, day=1):
    #     end_year = end.year
    # else:
    #     end_year = begin.year-1


    # num_years = end.year - begin.year
    # leapCount = 0
    # for year_count in num_years:
    #     if (begin.year + year_count) % 4 > 0:
    #         leapCount++

    # if (end.microsecond - begin.microsecond) < 0:


    return timedelta(days=(num_years * 365) + leapCount)
#524026




def update_history():
    dateEnd = datetime.now()
    dateStart = yearsago(1, dateEnd)

    time_to_get = dateEnd - dateStart

    get_granularity = 60

    last_date_processed = dateStart
    line_count = 0;
    with open('history.csv', 'r') as read_file:
        csv_reader = csv.reader(read_file, delimiter=',')
        # lines = list(csv_reader)
        for line in csv_reader:
            line_count+=1
            last_date_processed = line[0]
        # print(len(lines))

        if line_count > 0:
            print('last line: %s' % last_date_processed)
            dateStart = datetime.utcfromtimestamp(float(last_date_processed))


        print('Start Date: %s' % dateStart)

    read_file.close()

    while dateStart < dateEnd :
        time_to_get = dateEnd - dateStart
        min_to_get = time_to_get.total_seconds()/60

        data_to_get = 300

        if min_to_get < 300:
            data_to_get = min_to_get


        print('min_to_get: %d' % min_to_get)

        tempend = dateStart + timedelta(minutes=data_to_get)
        PARAMS = {'granularity':get_granularity, 'start':dateStart.isoformat(), 'end': tempend.isoformat()}

        print(dateStart)
        print(dateStart + timedelta(minutes=data_to_get))
        print(dateEnd - dateStart)
        # sending get request and saving the response as response object
        r = requests.get(url = URL, params = PARAMS)

        data = r.json()
        # print(data)

        with open('history.csv', 'a') as write_file:
            writer = csv.writer(write_file)
            new_lines = list(data)
            writer.writerows(reversed(new_lines))
            # writer.writerow('\n')
        write_file.close()

        # Update dateStart with last date aquired from API
        # print(data[0])
        dateStart = tempend
        delaytTime = timedelta(milliseconds=500)
        timecheck = datetime.now()

        while datetime.now() < timecheck + delaytTime:
            pass


update_history()

path_to_file = 'history.csv'

data = pd.read_csv(path_to_file, encoding = 'utf_8')
length = len(data)
print("length: %d" % length)

train_count = length * 0.7

#creating train and test sets
dataset = data.values

train_data = dataset[0:train_count,:]
validate_data = dataset[train_count:,:]

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)

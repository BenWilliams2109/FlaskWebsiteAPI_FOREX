import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, jsonify, request
import json

class Algorithms:  # Each instance of the class is a different data currency pair

    def __init__(self, dataset, time_period_start, time_period_end, time_interval):

        try:

            self.time_period_start = time_period_start  # NOTE: time_period_start/end has format DD.MM.YYYY
            self.time_period_end = time_period_end
            self.time_interval = time_interval

            self.dataset = pd.read_csv(r"./" + str(dataset) + ".csv",
                                       engine='c')  # NOTE: dataset has format CURRENCYPAIR_TICKS_DD.MM.YYYY-DD.MM.YYYY.csv
            self.dataset.columns = ["Localtime", "Ask", "Bid", "AskVolume", "BidVolume"]
            self.dataset = self.dataset.drop_duplicates(keep=False)
            self.dataset['Localtime'] = self.dataset['Localtime'].astype(str).str[:-9]
            self.dataset['Localtime'] = pd.to_datetime(self.dataset['Localtime'],
                                                       format="%d.%m.%Y %H:%M:%S.%f")  # find a way of making dates automatically in datetime in cache on api because converting it is slow every time

        except NameError:
            print("INVALID dataset name or time period")

        self.dataframe = self.dataset.resample(rule=str(self.time_interval) + 'Min', on='Localtime').mean()
        plt.plot(self.dataframe.index, self.dataframe['Bid'])

    def movingAverage(self):

        rolling_mean = self.dataframe.Bid.rolling(window=20).mean()
        rolling_mean2 = self.dataframe.Bid.rolling(window=50).mean()

        plt.plot(rolling_mean)
        plt.plot(rolling_mean2)
        plt.show()


testAlgorithm = Algorithms("GBPUSD_Ticks_21.12.2020-21.12.2020", "21.12.2020 00:00:07.032", "21.12.2020 00:00:07.033",
                           5)

testAlgorithm.movingAverage()

app = Flask(__name__)

@app.route('/algorithm/new', method=['POST'])
def executeAlgorithm():

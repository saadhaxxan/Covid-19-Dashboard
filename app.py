import pandas as pd
import numpy as np
from flask import Flask,render_template
import numpy as np
from datetime import datetime, timedelta
import datetime

x = datetime.datetime.now()
today_date = x.strftime("%x")
app = Flask(__name__)



data_recovered = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
data_confirmed = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
data_deaths = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
data_confirmed=data_confirmed.rename({data_confirmed.columns[-1]: 'Current'}, axis=1)
data_recovered=data_recovered.rename({data_recovered.columns[-1]: 'Current'}, axis=1)
data_deaths=data_deaths.rename({data_deaths.columns[-1]: 'Current'}, axis=1)
data_confirmed.rename(columns = {'Country/Region':'Country'}, inplace = True)
data_recovered.rename(columns = {'Country/Region':'Country'}, inplace = True)
data_deaths.rename(columns = {'Country/Region':'Country'}, inplace = True)
data_confirmed = data_confirmed[['Country','Current']]
data_recovered = data_recovered[['Country','Current']]
data_deaths = data_deaths[['Country','Current']]
total_confirmed = data_confirmed['Current'].sum()
total_deaths = data_deaths['Current'].sum()
total_recovered = data_recovered['Current'].sum()
total_confirmed='{:20,d}'.format(total_confirmed)
total_deaths='{:20,d}'.format(total_deaths)
total_recovered='{:20,d}'.format(total_recovered)
data_deaths = data_deaths.sort_values(by='Current', ascending=False)
data_recovered = data_recovered.sort_values(by='Current', ascending=False)
data_confirmed = data_confirmed.sort_values(by='Current', ascending=False)
data_confirmed.head(10).to_csv(r'static/top10_confirmed.csv',index=False,header=False)
data_deaths.head(10).to_csv(r'static/top10_deaths.csv',index=False,header=False)
data_recovered.head(10).to_csv(r'static/top10_recovered.csv',index=False,header=False)
data_confirmed.drop_duplicates(subset ="Country", keep = 'first', inplace = True) 
data_deaths.drop_duplicates(subset ="Country",keep = 'first', inplace = True) 
data_recovered.drop_duplicates(subset ="Country",keep = 'first', inplace = True) 
data_confirmed.to_csv(r'current_confirmed.csv',index=False,header=False)
data_deaths.to_csv(r'current_deaths.csv',index=False,header=False)
data_recovered.to_csv(r'current_recovered.csv',index=False,header=False)



@app.route('/')
def home():
    import csv
    death_data = []
    confirmed_data = []
    recovered_data = []
    # death_dataframe = pd.read_csv('current_deaths.csv')
    #  = pd.read_csv('current_confirmed.csv')
    # recovered_dataframe = pd.read_csv('current_recovered.csv')
    # deaths = death_dataframe['Current'].sum()
    # confirmed = df_confirmed['3/31/20'].sum()
    with open('current_deaths.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        for row in data:
            death_data.append({
            "Country": row[0],
            "deaths": row[1]
            })
    with open('current_confirmed.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        for row in data:
            confirmed_data.append({
            "Country": row[0],
            "Confirmed": row[1]
            })
    with open('current_recovered.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        for row in data:
            recovered_data.append({
            "Country": row[0],
            "Recovered": row[1]
            })
    return render_template('index.html',date=today_date,total_confirmed = total_confirmed,total_deaths = total_deaths,total_recovered =total_recovered ,death_data=death_data,recovered_data=recovered_data,confirmed_data=confirmed_data)#deaths=deaths,confirmed=confirmed)
data = pd.read_csv('index.csv')
@app.route('/search')
def search():
    return render_template('home.html')

@app.route('/graphs')
def graphs():
    return render_template('graphs.html')

@app.route('/search/results', methods=['GET','POST'])
def request_search():
    import csv
    data = []
    with open('index.csv') as csv_file:
        file_data = csv.reader(csv_file, delimiter=',')
        for row in file_data:
            data.append({
            "title": row[0],
            "abstract": row[1],
            # "publish_time": row[2],
            "authors": row[3],
            "url":row[4]
            })
    

    return render_template('results.html', data=data)
if __name__ == '__main__':
    app.run('127.0.0.1')
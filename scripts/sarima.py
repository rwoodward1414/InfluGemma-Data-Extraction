import pandas
import os, sys
import random
from sklearn.metrics import mean_squared_error, mean_absolute_error, root_mean_squared_error

path = os.path.dirname(os.path.abspath('../database/database_update.py'))
if path not in sys.path:
    sys.path.append(path)

from datebase_update import get_fortnight_surv
from datetime import datetime, timedelta
from statsmodels.tsa.statespace.sarimax import SARIMAX

def sarima_forecast(state_id, date, forecast_steps=1, order=(0,1,0), seasonal_order=(0,0,0,0)):
  start = datetime.strptime(date, "%Y-%m-%d")
  dates = []
  past = []
  for i in range(51,-1,-1):
    dates.append(start - timedelta(days=(i*14)))
  for value in dates:
    case_num = get_fortnight_surv(state_id, value)
    past.append(case_num)


  df = pandas.DataFrame(past)

  model = SARIMAX(df, order=order, seasonal_order=seasonal_order)
  model.initialize_approximate_diffuse()
  model_fit = model.fit(disp=False)
  forecast = model_fit.forecast(steps=forecast_steps)
  output = forecast.tolist()[0]
  if output < 0:
     output = 0
  output = int(output)

  return output

def eval_sarima():
  predicted = []
  actual = []
  start = datetime(2016, 1, 1)
  end = datetime(2023, 12, 30)
  days_between = (end - start).days

  for i in range(0,20):
    random_days = random.randint(1, days_between)
    random_date = datetime.strftime((start + timedelta(days=random_days)), "%Y-%m-%d")
    end_date = start + timedelta(days=random_days + 15)
    state = random.randint(1,59)
    predicted.append(sarima_forecast(state, random_date))
    actual.append(get_fortnight_surv(state, end_date)[0])


  print("Mean square error " + str(mean_squared_error(actual, predicted)))
  print("Mean absolute error " + str(mean_absolute_error(actual, predicted)))
  print("Root mean sqare error " + str(root_mean_squared_error(actual, predicted)))
  print(predicted)
  print(actual)

eval_sarima()
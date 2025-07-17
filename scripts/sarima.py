import pandas
import os, sys

path = os.path.dirname(os.path.abspath('../database/database_update.py'))
if path not in sys.path:
    sys.path.append(path)

from datebase_update import get_fortnight_surv
from datetime import datetime, timedelta
from statsmodels.tsa.statespace.sarimax import SARIMAX

# numbers for parameters came from https://www.kaggle.com/code/skeller/arima-influenza-baselines
def sarima_forecast(state_id, date, forecast_steps=1, order=(1,1,0), seasonal_order=(1,1,0,2)):
  start = datetime.strptime(date, "%Y-%m-%d")
  dates = []
  past = []
  for i in range(6,-1,-1):
    dates.append(start - timedelta(days=(i*14)))
  for value in dates:
    case_num = get_fortnight_surv(state_id, value)
    past.append(case_num)


  df = pandas.DataFrame(past)
  print(df)
  model = SARIMAX(df, order=order, seasonal_order=seasonal_order)
  model_fit = model.fit(disp=False)
  forecast = model_fit.forecast(steps=forecast_steps)
  output = forecast.tolist()[0]
  if output < 0:
     output = 0
  print(output)

  return output

sarima_forecast(4, "2022-05-06")
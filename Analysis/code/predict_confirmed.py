import pandas as pd
from fbprophet import Prophet
# 코로나 국내 현황 시계열 데이터 불러오기
data = pd.read_csv("C:/Users/USER/Desktop/jin/data/Time.csv", encoding = "cp949", engine = "python")
# print(data.tail())
confirmed = data[['date', 'confirmed']]
# print(confirmed.head())

# Facebook Prophet 예측 모델에 넣을 데이터프레임을 만들어준다.
#(날짜는 ds, 다른 변수는 y로 반드시 맞춰준다)
confirmed_prophet = confirmed.rename(columns={'date': 'ds', 'confirmed': 'y'})
print(confirmed_prophet.head())

m = Prophet()
m.fit(confirmed_prophet)

future = m.make_future_dataframe(periods=30)
future
future.tail()

forecast = m.predict(future)
forecast.tail()

m.plot(forecast)


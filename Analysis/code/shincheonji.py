DAYS2FIT = 5
PREDICT_PERIOD = 7
predDatelinear, predY = linearRgPrediction(koreaBeforeSCJ, DAYS2FIT, PREDICT_PERIOD)

popt, pcov = curve_fit(logistic, range(len(koreaBeforeSCJ)), koreaBeforeSCJ['Confirmed'], p0)
predLogistic = logistic(range(len(koreaBeforeSCJ)+DAYS2FIT), *popt)

actualDate = koreaBeforeSCJ['Date']
predDate = pd.date_range(actualDate.iloc[0], actualDate.iloc[-1] + dt.timedelta(days=DAYS2FIT))
futureDate = pd.date_range(actualDate.iloc[-1], predDate[-1])

fig = go.Figure()
fig.add_trace(go.Scatter(x=actualDate, y=koreaBeforeSCJ['Confirmed'],
              marker=dict(color = DEFAULT_PLOTLY_COLORS[0]),name='Confirmed'))
fig.add_trace(go.Scatter(x=actualDate, y=predLogistic[:-DAYS2FIT], # 입력데이터 까지의 예측값
        marker=dict(color = DEFAULT_PLOTLY_COLORS[1]),name='Logistic Prediction'))
fig.add_trace(go.Scatter(x=futureDate, y=predLogistic[-DAYS2FIT:], # 입력이후 진행방향
                         line = dict(color=DEFAULT_PLOTLY_COLORS[1], width=1, dash='dot'),
                         showlegend=True,name='Logistic After 7 days Prediction'))

fig.add_trace(go.Scatter(x=predDatelinear, y=predY.reshape(1,-1)[0],
                         line = dict(color=DEFAULT_PLOTLY_COLORS[2], width=3, ),#dash='dash'
                         showlegend=True, name='Linear After 7 days Prediction'))

fig.update_layout(title='>',
                  font = layout_setting['font'],
                  font_size=14, legend_orientation="h",
                  legend=dict( traceorder="normal",
                             font=dict(family="sans-serif", size=15)))
fig.show()




lastData = korea[-DAYS2FIT:]
predDate, predY = linearRgPrediction(koreaBeforeSCJ, 10, PREDICT_PERIOD)
popt, pcov = curve_fit(logistic, range(len(koreaBeforeSCJ)), koreaBeforeSCJ['Confirmed'], p0)

logisticPeriod = pd.date_range(koreaBeforeSCJ['Date'].iloc[0],
                               koreaBeforeSCJ['Date'].iloc[-1] + dt.timedelta(days=PREDICT_PERIOD))

fig = go.Figure()

fig.add_trace(go.Scatter(x=koreaBeforeSCJ['Date'], y=koreaBeforeSCJ['Confirmed'],
              marker=dict(color = DEFAULT_PLOTLY_COLORS[0]),name='confirmed'))

fig.add_trace(go.Scatter(x=predDate[-9:], y=predY.reshape(1,-1)[0][-9:],
        line = dict(color=DEFAULT_PLOTLY_COLORS[2], width=3, dash='dot'),name='linear regression prediction'))

fig.add_trace(go.Scatter(x=korea['Date'][27:33], y=korea['Confirmed'][27:33],
        line = dict(color=DEFAULT_PLOTLY_COLORS[3], width=3, dash='dot'),name='Actual Confirmed'))

fig.add_trace(go.Scatter(x=logisticPeriod[-9:], y=logistic(range(len(koreaBeforeSCJ)+PREDICT_PERIOD), *popt)[-9:],
        line = dict(color=DEFAULT_PLOTLY_COLORS[1], width=3, dash='dot'),name='logistic prediction'))

# fig.add_trace(go.Scatter(x=list(range(len(koreaBeforeSCJ),len(koreaBeforeSCJ)+7)), y=logistic(range(len(koreaBeforeSCJ)+7), *popt)[-7:],
#                          line = dict(color=DEFAULT_PLOTLY_COLORS[1], width=1, dash='dot'),name='prediction'))
fig.update_layout(title='>',
                  font = layout_setting['font'],
                  height=500, font_size=14, legend_orientation="h",
                  legend=dict( traceorder="normal",
                             font=dict(family="sans-serif", size=15)))
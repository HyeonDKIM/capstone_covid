korea = WHO_Data[WHO_Data['Country'] == 'Republic of Korea']
korea = add_rates(korea)

koreaBeforeSCJ = korea[korea['Date'] < "2020-02-17"] # 신천지 이전 기간 데이터
koreaBeforeSCJ = add_rates(koreaBeforeSCJ)

italy = WHO_Data[WHO_Data['Country'] == 'Italy'] # WHO 데이터
italy = add_rates(italy)

us = WHO_Data[WHO_Data['Country'] == 'United States of America'] # WHO 데이터
us = add_rates(us)

china = WHO_Data[WHO_Data['Country'] == 'China']
china = add_rates(china)

################################## 4개 나라 그래프 #################################
DAYS2FIT = 5
PREDICT_PERIOD = 14

fig = make_subplots(rows=2, cols=2, subplot_titles=['>'])
countries = [china, korea, italy, us]
name = ['China', 'Korea', 'Italy', 'U.S.A']
for i in range(4):
    if i > 1:
        row = 2
        col = i - 1
    else:
        row = 1
        col = i + 1

    legend = False
    if i == 3:
        legend = True

    # 날짜 설정
    actualDate = countries[i]['Date']
    predDate = pd.date_range(actualDate.iloc[0], actualDate.iloc[-1] + dt.timedelta(days=PREDICT_PERIOD))
    futureDate = pd.date_range(actualDate.iloc[-1], predDate[-1])

    # 선형회귀 예측
    predDate, predY = linearRgPrediction(countries[i], DAYS2FIT, PREDICT_PERIOD)
    # 로지스틱 함수 파라미터 찾기
    popt, pcov = curve_fit(logistic, range(len(countries[i])), countries[i]['Confirmed'], p0)

    # 실제 확진자 그래프
    fig.add_trace(go.Scatter(x=actualDate, y=countries[i]['Confirmed'],
                             marker=dict(color=DEFAULT_PLOTLY_COLORS[0]),
                             showlegend=legend, name='real'),
                  row=row, col=col)

    # Logistic Curve
    fig.add_trace(go.Scatter(x=actualDate,
                             y=logistic(range(len(countries[i]) + PREDICT_PERIOD), *popt),
                             marker=dict(color=DEFAULT_PLOTLY_COLORS[1]),
                             showlegend=legend, name='Logistic Curve'), row=row, col=col)

    # Logistic Curve 예측 부분
    fig.add_trace(go.Scatter(x=futureDate,
                             y=logistic(range(len(countries[i]) + PREDICT_PERIOD), *popt)[-PREDICT_PERIOD - 1:],
                             mode='lines', line=dict(color=DEFAULT_PLOTLY_COLORS[1], width=3, dash='dot'),
                             showlegend=legend, name='Logistic Prediction'), row=row, col=col)

    # 선형 회귀 선
    fig.add_trace(go.Scatter(x=predDate, y=predY.reshape(1, -1)[0], mode='lines',
                             line=dict(color=DEFAULT_PLOTLY_COLORS[2], width=3, dash='dot'),
                             showlegend=legend, name='Linear regresstion prediction'),
                  row=row, col=col)

fig.update_layout(title='>',
                  font=layout_setting['font'],
                  font_size=14, legend_orientation="h",
                  legend=dict(traceorder="normal", font=dict(family="sans-serif", size=15)))
fig.show()
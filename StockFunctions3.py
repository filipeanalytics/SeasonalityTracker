import pandas as pd
import pandas_datareader as pdr
import datetime
import plotly.graph_objects as go
from dateutil.relativedelta import relativedelta
import plotly

def getStock(stk1, yearsBack):
    today = datetime.date.today()
    yearsBack = int(yearsBack)
    dtPast = today + relativedelta(years=-yearsBack)

    df = pd.DataFrame(columns=["date","date2","date3","Open","High","Low","Close"])
    # Call Yahoo finance to get stock data for the stock provided.
    df1 = pdr.get_data_yahoo(stk1,
                             start= datetime.datetime(dtPast.year, dtPast.month, dtPast.day),
                             end  = datetime.datetime(today.year, today.month, today.day))

    df['date'] = df1.index.strftime("%Y-%m-%d")  # date is the index in df1
    df['date2'] = df1.index.strftime("%j")  # converts to Day of the Year (1-365)
    df['date3'] = df1.index.strftime("%b %d") # month day format

    df["Open"] = df1["Open"].values
    df["High"] = df1["High"].values
    df["Low"] = df1["Low"].values
    df["Close"] = df1["Close"].values

    dfOhlc = df[["date","date2","date3","Open","High","Low","Close"]]
    return dfOhlc

def graphByYears(dfResult, stk1):
    start_index = 0 #determines starting index for range of dates to be plotted
    firstDate = dfResult.loc[0]['date']  # getting first date
    previousMonth = firstDate[5:7]  # YYYY-MM 01234[56] = Extracting the month
    newMonth = False
    switchVar = True  # controls time to switch graph colors based on year
    plot_list = []  # will store all CandleSticks plots
    day_of_year_list = [] # will store all dates converted to Day of the Year (1-365)
    day_month_list = [] # will store all dates converted to MM-DD(Jan01-Dec31)

    fig = go.Figure()
    for i in range(len(dfResult)):  # navigate through whole dfResult
        dt = dfResult.loc[i]['date']
        mth = dt[5:7] #extract month from date

        yd = pd.to_datetime(dt).timetuple().tm_yday # converts datetime to day of the year
        day_of_year_list.append(yd)

        day_month = pd.to_datetime(dt).strftime("%b %d")
        day_month_list.append(day_month)

        if previousMonth != mth: # If it's a new month
            newMonth = True
            previousMonth = mth

        # if its a new year, plot previous year graph
        if mth == '01' and newMonth == True:  # means it's a new year
            # print('New Year!')
            plot_obj = graphSupport2(fig, dfResult, start_index, i, switchVar,
                                     day_of_year_list, day_month_list)
            plot_list.append(plot_obj)
            switchVar = not switchVar #switchs the value of switch variable
            start_index = i
            newMonth = False

        # if reached end of DF, plot last part of graph
        elif i == len(dfResult) - 1:
            plot_obj = graphSupport2(fig, dfResult, start_index, i, switchVar,
                                     day_of_year_list, day_month_list)
            plot_list.append(plot_obj)
            switchVar = not switchVar  # switchs the value of switch variable

    fig = go.Figure(data=plot_list)
    fig.update_layout(
        # title='Seasonality Tracker',
        title='Analyzing [%s] Stock' %stk1,
        # yaxis_title='%s Stock' %stk1,
        yaxis_title='Prices',
        legend = dict(traceorder='reversed'),
        autosize = True,
        height = 800,
        # width = 1500
    )

    ticksValsTexts = xtickEditor() # function created defined below

    # Set custom x-axis labels to show MM-DD instead of 1-365
    fig.update_xaxes(
        ticktext= ticksValsTexts[0] # ticktextVar
        ,tickvals= ticksValsTexts[1] # tickvalsVar,
        ,tickangle=-90,
        tickfont=dict(
            family='Old Standard TT, serif',
            size=10,
            color='black',
        )
    )# Set custom x-axis labels

    htmlGraph = plotly.io.to_html(fig, include_plotlyjs=False, full_html=False)
    return htmlGraph

def xtickEditor ():
    ticktextVar = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
                   "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    ticks7daysTo28 = list(range(0, 31, 7))[1:]  # [7, 14, 21, 28]
    ticks7daysTo28 = ticks7daysTo28 * 12  # repeat for the 12 months
    ticks7daysTo28.pop(7)  # removed Feb28 as it was interfering with MAR tick
    ticktextVar = ticktextVar + ticks7daysTo28  # appends markers for every 7days to month
    # markers

    # MAR is on 60, but moved to 62 as it was over 28 from FEB
    tickvalsVar = ["2", "32", "60", "91", "121", "152", "182", "213", "244", "274", "305",
                   "335"]
    # List of the days of the year day 7 falls into each month (Non-Leap Year).
    # http://tornado.sfsu.edu/geosciences/classes/m302/DayofYear.html
    map7Month = [7, 38, 66, 97, 127, 158, 188, 219, 250, 280, 311, 341]
    map14Month = [14, 45, 73, 104, 134, 165, 195, 226, 257, 287, 318, 348]
    map21Month = [21, 52, 80, 111, 141, 172, 202, 233, 264, 294, 325, 355]
    map28Month = [28, 59, 87, 118, 148, 179, 209, 240, 271, 301, 332, 362]
    map28Month.remove(59)  # removed Feb28 as it was interfering with MAR tick
    map7Year = map7Month + map14Month + map21Month + map28Month
    map7Year.sort()
    tickvalsVar = tickvalsVar + map7Year

    ticksValsTexts = [ticktextVar, tickvalsVar]
    return ticksValsTexts

# Making graphs plot over each other
def graphSupport2(fig, dfResult, start_index, end_index, switchVar,doy_list, dm_list):
    trace_label = dfResult.loc[start_index]['date'][:4]#extracting Year
    if switchVar:
        plotObj = go.Candlestick(
            x=dfResult[start_index:end_index]['date2'],
            open=dfResult[start_index:end_index]['Open'],
            high=dfResult[start_index:end_index]['High'],
            low=dfResult[start_index:end_index]['Low'],
            close=dfResult[start_index:end_index]['Close'],
            increasing_line_color='cyan', decreasing_line_color='gray',
            name="%s" % trace_label,
        )
    else: #prints with default colors
        plotObj = go.Candlestick(
            x=dfResult[start_index:end_index]['date2'],
            open=dfResult[start_index:end_index]['Open'],
            high=dfResult[start_index:end_index]['High'],
            low=dfResult[start_index:end_index]['Low'],
            close=dfResult[start_index:end_index]['Close'],
            name="%s" % trace_label,
        )
    return plotObj
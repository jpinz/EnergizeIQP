import os
import plotly
import plotly.graph_objs as go
import pandas as pd
import utils
import plot_week


def plot(filename, title, df):
    # df2 = df[df.index % 10 == 0]  # Selects every 10th row starting from 0
    df = df.fillna(method="ffill")
    print(df.head(20))
    if 'Time' in df.columns:
        df['datetime'] = pd.to_datetime(df['Time'])
    else:
        df['datetime'] = pd.to_datetime(df['datetime'])

    df.index = df['datetime']

    start_time = utils.unix_time_millis(df.first_valid_index())

    # act_pow = df.ActPow
    # # print(act_pow[act_pow.notnull()])
    # act_pow = act_pow.replace(0, pd.np.nan)  # .dropna(axis=0, how='any').fillna(0).astype(int)

    # print(act_pow.loc[:, (act_pow != 0).any(axis=0)])
    # print(act_pow.head(20))

    df = df.resample("15T").mean()
    # df = df.replace(pd.np.nan, 0)  # .dropna(axis=0, how='any').fillna(0).astype(int)

    print(df.head(9))
    # commented out because resampling should hopefully get the mean now
    # hwt_outlet = df.HwTOutlet.rolling(60).mean()
    # hwt_outlet.drop(hwt_outlet.index[:59], inplace=True)
    # temp_outlet = df.PrimT.rolling(60).mean()
    # temp_outlet.drop(temp_outlet.index[:59], inplace=True)
    # print(hwt_outlet.head(10))
    # hwt_set = go.Scatter(x=df["Time"], y=df["HwTSet"], name="HW Setpoint", connectgaps=True)
    # trace_temp_set = go.Scatter(x=df.index, y=df.PrimTSet, name="Primary Temp Setpoint", connectgaps=True)

    trace_hwt_outlet = go.Scatter(x=df.index, y=df.HwTOutlet, name="HW Outlet", connectgaps=True)  # HW Outlet
    # is the temperature at the outlet going to the hot water system
    # trace_act_power = go.Scatter(x=df.index, y=act_pow, name="Actual Power", yaxis='y2')
    trace_temp_outlet = go.Scatter(x=df.index, y=df.PrimT, name="Primary Temp", connectgaps=True)  # Primary
    # temperature is the temp measured at the top of the burner that heats up the water

    layout = go.Layout(
        title=title,
        yaxis=dict(
            title='Temperature'
        ),
        # yaxis2=dict(
        #     title='Load on Boiler',
        #     overlaying='y',
        #     # hoverformat='.0%',
        #     side='right',
        #     showgrid=False,
        #     zeroline=False,
        #     showline=False,
        # ),
        xaxis=dict(
            tick0=start_time,
            rangeselector=dict(
                buttons=list([
                    dict(count=7,
                         label='1w',
                         step='day',
                         stepmode='backward'),
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type='date'
        )
    )

    plotly.offline.plot({
        "data": [trace_hwt_outlet, trace_temp_outlet],  # trace_temp_set, trace_act_power],
        "layout": layout
    }, filename=filename, auto_open=False)


def plot_all(HMO_id, df, breaks):
    hot_week = None
    cold_week = None

    HMO_name, HMO_num = utils.map_hmo_to_id(HMO_id)
    path = "hmo_{}".format(HMO_num)

    if not os.path.exists(path):
        os.mkdir(path)

    plot('./{}/plot_season.html'.format(path), "Analysis of HMO #{} for the Heating Season".format(HMO_num), df)

    if os.path.exists("./{}/additional_data.txt".format(path)):
        os.remove("./{}/additional_data.txt".format(path))

    f = open("./{}/additional_data.txt".format(path), "w+")
    f.write("Information about {}\r\n".format(HMO_name))
    f.write("Season boiler temperature average is {}°C\r\n".format(df.PrimT.mean()))
    f.close()

    for key, value in breaks.items():
        print(key)
        if key == "Hot Week":
            hot_week = value
        elif key == "Cold Week":
            cold_week = value
        else:
            plot('./{}/plot_{}.html'.format(path, key.replace(' ', '_').lower()),
                 "Analysis of HMO #{} for {}".format(HMO_num, key), value)

    plot_week.plot_week('./{}/plot_week_comparison.html'.format(path), "Comparison of the Hottest and Coldest week of "
                                                                       "the Season for HMO #{}".format(HMO_num),
                        hot_week, cold_week)

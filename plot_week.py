from plotly import tools
import plotly.graph_objs as go
from plotly.offline import plot
import datetime as dt
import pandas as pd
import utils


# Taken from https://stackoverflow.com/questions/24432605
def get_longest_hot_boiler(df):
    # make another DF to hold info about each region
    regs_above_thresh = pd.DataFrame()

    # first row of consecutive region is a True preceded by a False in tags
    regs_above_thresh['start_idx'] = \
        df.index[df['tag'] & ~ df['tag'].shift(1).fillna(False)]

    # last row of consecutive region is a False preceded by a True
    regs_above_thresh['end_idx'] = \
        df.index[df['tag'] & ~ df['tag'].shift(-1).fillna(False)]

    # how long is each region
    regs_above_thresh['spans'] = \
        [((spam[0] - spam[1]).total_seconds() + 1) for spam in \
         zip(regs_above_thresh['end_idx'], regs_above_thresh['start_idx'])]

    # index of the region with the longest span
    max_idx = regs_above_thresh['spans'].argmax()

    return (regs_above_thresh.ix[max_idx]['spans'] - 1) / 3600


def compare_weeks(filename, title, df_c, df_h):
    HMO_num = filename[2:7]
    print(HMO_num)

    df_c['avg'] = df_c["PrimT"].mean()
    df_h['avg'] = df_h["PrimT"].mean()

    start_time = utils.unix_time_millis(df_c.first_valid_index())

    times = df_c.index.to_series().apply(lambda x: dt.datetime.strftime(x, '%A %H:%M')).tolist()
    trace_hwt_outlet_cold = go.Scatter(x=times, y=df_c.HwTOutlet, name="HW Outlet - Cold Week", connectgaps=True,
                                       line=dict(
                                           color='#1f77b4'
                                       ))
    # HW Outlet is the temperature at the outlet going to the hot water system

    trace_temp_outlet_cold = go.Scatter(x=times, y=df_c.PrimT, name="Primary Temp - Cold Week", connectgaps=True,
                                        line=dict(
                                            color='#ff7f0e'
                                        ))
    # Primary temperature is the temp measured at the top of the burner that heats up the water
    trace_boiler_average_cold = go.Scatter(x=times, y=df_c.avg, name="Boiler Average - Cold Week", connectgaps=True,
                                           line=dict(
                                               color='#2ca02c'
                                           ))

    trace_hwt_outlet_hot = go.Scatter(x=times, y=df_h.HwTOutlet, name="HW Outlet - Hot Week", connectgaps=True,
                                      line=dict(
                                          color='#1f77b4'
                                      ))
    # HW Outlet is the temperature at the outlet going to the hot water system

    trace_temp_outlet_hot = go.Scatter(x=times, y=df_h.PrimT, name="Primary Temp - Hot Week", connectgaps=True,
                                       line=dict(
                                           color='#ff7f0e'
                                       ))
    # Primary temperature is the temp measured at the top of the burner that heats up the water
    trace_boiler_average_hot = go.Scatter(x=times, y=df_h.avg, name="Boiler Average - Hot Week", connectgaps=True,
                                          line=dict(
                                              color='#2ca02c'
                                          ))

    fig = tools.make_subplots(rows=2, cols=1, specs=[[{}], [{}]],
                              subplot_titles=('HMO Analysis of Cold Week', 'HMO Analysis of Hot Week'),
                              shared_xaxes=True, shared_yaxes=False,
                              vertical_spacing=0.1)
    fig.append_trace(trace_hwt_outlet_cold, 1, 1)
    fig.append_trace(trace_temp_outlet_cold, 1, 1)
    fig.append_trace(trace_boiler_average_cold, 1, 1)
    fig.append_trace(trace_hwt_outlet_hot, 2, 1)
    fig.append_trace(trace_temp_outlet_hot, 2, 1)
    fig.append_trace(trace_boiler_average_hot, 2, 1)

    fig['layout'].update(
        title=title,
        yaxis=dict(
            title='Temperature'
        ),
        xaxis=dict(
            tick0=start_time,
            nticks=21
        )
    )

    plot(fig, filename=filename, auto_open=False)

    boiler_temp_threshold = 50
    df_c['tag'] = df_c.PrimT > boiler_temp_threshold
    df_h['tag'] = df_h.PrimT > boiler_temp_threshold

    time_spent_boiler_c = (df_c.PrimT >= 50).values.sum() / 20
    max_time_spent_boiler_c = get_longest_hot_boiler(df_c)
    time_spent_boiler_h = (df_h.PrimT >= 50).values.sum() / 20
    max_time_spent_boiler_h = get_longest_hot_boiler(df_h)

    cold_week_text = "During the cold week, the boiler was above 50°C for {} hours, with the longest period being {} " \
                     "hours long, on average it was {}°C ".format(time_spent_boiler_c, max_time_spent_boiler_c,
                                                                  df_c.avg.values[0])
    hot_week_text = "During the hot week, the boiler was above 50°C for {} hours, with the longest period being {} " \
                    "hours long, on average it was {}°C ".format(time_spent_boiler_h, max_time_spent_boiler_h,
                                                                 df_h.avg.values[0])
    f = open("./{}/additional_data.txt".format(HMO_num), "a+")
    f.write(cold_week_text + "\r\n")
    f.write(hot_week_text + "\r\n")

    print(cold_week_text)

    print(hot_week_text)


def plot_week(filename, title, df_h, df_c):
    df_h = df_h.fillna(method="ffill")
    df_c = df_c.fillna(method="ffill")

    if 'Time' in df_h.columns:
        df_h['datetime'] = pd.to_datetime(df_h['Time'])
    else:
        df_h['datetime'] = pd.to_datetime(df_h['datetime'])

    if 'Time' in df_c.columns:
        df_c['datetime'] = pd.to_datetime(df_c['Time'])
    else:
        df_c['datetime'] = pd.to_datetime(df_c['datetime'])

    df_h.index = df_h['datetime']
    df_c.index = df_c['datetime']

    df_h = df_h.resample("3T").mean()
    df_c = df_c.resample("3T").mean()

    df_h['weekday'] = df_h.index.weekday_name
    df_c['weekday'] = df_c.index.weekday_name

    compare_weeks(filename, title, df_c, df_h)

import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
from datetime import datetime


def matrix(df_end):
    pairs = dict()
    pairs_set = set()
    for i in range(len(df_end) - 1):
        if df_end['event_name'][i] != 'end_session':
            pair = df_end['event_name'][i] + ' to ' + df_end['event_name'][i+1]
            if pair not in pairs_set:
                pairs_set.add(pair)
                pairs[pair] = 1
            else:
                pairs[pair] += 1
            
    first = []
    second = []
    number = []
    for i in pairs_set:
        first.append(i.split(' to ')[0])
        second.append(i.split(' to ')[1])
        number.append(pairs[i])
    
    df_final = pd.DataFrame(data = {'first': first, 'second': second, 'number': number})
    df_final = df_final.sort_values(by = ['first', 'second'])
    df_final = df_final.reset_index(drop = True)

    matrix = pd.DataFrame(columns = list(set(df_final['second'])))
    events = list(set(df_final['second']))
    events_first = {}
    events_second_dict = {}
    events_second_set = set()
    temp = []
    ind = []
    for i in range(len(df_final)-1):
        if df_final['first'][i] == df_final['first'][i+1] and i+1 != len(df_final)-1:
            events_second_dict[df_final['second'][i]] = df_final['number'][i]
            events_second_set.add(df_final['second'][i])
        elif df_final['first'][i] == df_final['first'][i+1] and i+1 == len(df_final)-1:
            events_second_dict[df_final['second'][i]] = df_final['number'][i]
            events_second_set.add(df_final['second'][i])
            for j in events:
                if j in events_second_set:
                    temp.append(events_second_dict[j])
                else:
                    temp.append(0)
            lol = pd.DataFrame(temp).T
            lol.columns = list(set(df_final['second']))
            matrix = matrix.append(lol)
            ind.append(df_final['first'][i])
        else:
            events_second_dict[df_final['second'][i]] = df_final['number'][i]
            events_second_set.add(df_final['second'][i])
            for j in events:
                if j in events_second_set:
                    temp.append(events_second_dict[j])
                else:
                    temp.append(0)
            lol = pd.DataFrame(temp).T
            lol.columns = list(set(df_final['second']))
            matrix = matrix.append(lol)
            events_second_dict = {}
            events_second_set = set()
            temp = []
            ind.append(df_final['first'][i])
        
    matrix = matrix.set_index([pd.Index(ind)])

    full = 0
    for i in matrix:
        full += sum(matrix[i])
    
    fordel = []
    for i in matrix:
        if sum(matrix[i]) / full < 0.01:
            fordel.append(i)
        
    matrix.drop(fordel, axis='columns', inplace=True)
    matrix.drop(fordel, axis='index', inplace=True)
    
    matrix = matrix.sort_values(list(matrix)[0], ascending = False)
    matrix = matrix.T
    matrix = matrix.sort_values(list(matrix)[0], ascending = False)
    matrix = matrix.T

    vegetables = matrix.index
    farmers = matrix.columns

    harvest = matrix.to_numpy(dtype = np.int64)

    def heatmap(data, row_labels, col_labels, ax=None, **kwargs):
        if not ax:
            ax = plt.gca()
            
        im = ax.imshow(data, **kwargs)

        ax.set_xticks(np.arange(data.shape[1]))
        ax.set_yticks(np.arange(data.shape[0]))
        ax.set_xticklabels(col_labels)
        ax.set_yticklabels(row_labels)

        ax.tick_params(top=True, bottom=False,
                       labeltop=True, labelbottom=False)

        plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
                 rotation_mode="anchor")

        for edge, spine in ax.spines.items():
            spine.set_visible(False)

        ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
        ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
        ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
        ax.tick_params(which="minor", bottom=False, left=False)

        return im


    def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                         textcolors=["black", "white"],
                         threshold=None, **textkw):

        if not isinstance(data, (list, np.ndarray)):
            data = im.get_array()

        if threshold is not None:
            threshold = im.norm(threshold)
        else:
            threshold = im.norm(data.max())/2.
        kw = dict(horizontalalignment="center",
                  verticalalignment="center")
        kw.update(textkw)

        if isinstance(valfmt, str):
            valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

        texts = []
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
                text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
                texts.append(text)

        return texts

    fig, ax = plt.subplots(figsize=(12, 12))

    im = heatmap(harvest, vegetables, farmers, ax=ax, cmap="YlGn")
    texts = annotate_heatmap(im, valfmt="{x:}")

    fig.tight_layout()
    plt.show()
    
    return matrix

def adaptation(df):
    delta = timedelta(seconds = 1)

    if type(df['event_time'][0]) == str:
        event_timestamp = []
        for i in df['event_time']:
            event_timestamp.append(datetime.strptime(i, '%Y-%m-%d %H:%M:%S'))
        df['event_time'] =  event_timestamp

    user_pseudo_id = [df['session_web_id'][0]]
    event_timestamp = [df['event_time'][0] - delta]
    concat = ['start_session']
    user_pseudo_id.append(df['session_web_id'][0])
    event_timestamp.append(df['event_time'][0])
    concat.append(df['event_name'][0])

    el = lambda x: (user_pseudo_id.append(df['session_web_id'][x-1]), \
                   event_timestamp.append(df['event_time'][x-1] + delta), \
                   concat.append('end_session'), \
                   user_pseudo_id.append(df['session_web_id'][x]), \
                   event_timestamp.append(df['event_time'][x] - delta), \
                   concat.append('start_session'), \
                   user_pseudo_id.append(df['session_web_id'][x]), \
                   event_timestamp.append(df['event_time'][x]), \
                   concat.append(df['event_name'][x])) \
                   if df['session_web_id'][x] != df['session_web_id'][x-1] \
                   else \
                   (user_pseudo_id.append(df['session_web_id'][x]), \
                   event_timestamp.append(df['event_time'][x]), \
                   concat.append(df['event_name'][x]))

    x = list(map(el, list(range(1, len(df)))))

    user_pseudo_id.append(df['session_web_id'][len(df)-1])
    event_timestamp.append(df['event_time'][len(df)-1] + delta)
    concat.append('end_session')

    df_end = pd.DataFrame(data = {'event_timestamp': event_timestamp, 'user_pseudo_id': user_pseudo_id, 'event_name': concat})
    
    return df_end

def event_adaptation(df, event):
    session_set = frozenset(df[df['event_name'] == event].drop_duplicates()['session_web_id'])
    df['fordel'] = df['session_web_id'].map(lambda x: 1 if x in session_set else 0)
    df = df.loc[df['fordel'] == 1]
    adaptation(df)
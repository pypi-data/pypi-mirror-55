# -*- coding:utf-8 -*- 
from __future__ import division
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_toolkits.axes_grid.inset_locator import inset_axes
from xpinyin import Pinyin
import matplotlib.font_manager as fm
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
myfont = fm.FontProperties(fname='msyh.ttf') # 设置字体

class plot_max:
    '''
    a union framework of plot

    :param figsize: the size of figure, default (16,5)
    :type figsize: tuple of (int, int)
    
    :param figtitle: the title of figure, default ''
    :type figtitle: str
    
    :param capacity: the max curve capacity for each subplot
    :type capacity: int

    :param savepath: the save path of figure
    :type savepath: str
    
    :param style: the background style, default, seaborn-dark, ggplot, bmh, seaborn-bright
    :type style: str
    
    example:
        graph = plot_max(capacity=5)
        graph.load_data(x, y)
        graph.show()
    '''

    def __init__(self, 
                 figsize=(16,5), 
                 figtitle='', 
                 capacity=1, 
                 savepath='', 
                 count_cut=100, 
                 style='seaborn-bright'):
        self.figtitle = figtitle
        self.figsize = figsize
        self.capacity = capacity
        self.data_list = []
        self.savepath = savepath
        self.count_cut = count_cut
        plt.style.use(style)

    def get_ax(self):
        '''
        lay out, find the ax for recent subplot
        return ax
        '''
        col = int(self.subplot_index/self.nrows)
        row = self.subplot_index - self.nrows * col

        if self.ncols == 1 and self.nrows == 1:
            return self.axes
        if self.ncols == 1:
            return self.axes[row]
        if self.nrows == 1:
            return self.axes[col]

        return self.axes[row, col]
    
    def load_df(self, df, x, keys=[], ys=[], color='hotpink',
             marker='.', 
             label='',
             xlabel='', 
             ylabel='', 
             rotation=0,
             xsize=15,
             ysize=15,
             width=0.5,
             title='',
             xtype='simple',
             plot_type='曲线',
             legend=True,
             legendsize=20,
             to_pin=False,
             bins=10,
             legend_loc=0,
             titlesize=20):
        '''
        load pandas dataframe
        example:
        graph
        '''
        if len(keys) == 0:
            for y in ys:
                self.load_data(df[x].values, df[y].values, title=y, label=y, xtype=xtype, legend=legend, legendsize=legendsize)
        elif isinstance(keys, str) or len(keys)==1:
            for w in df[keys].unique():
                s = df[df[keys]==w]
                for y in ys:
                    self.load_data(s[x].values, s[y].values, title=y, label=w, xtype=xtype, legend=legend, legendsize=legendsize)
        else:
            for key1 in df[keys[0]].unique():
                s1 = df[df[keys[0]]==key1].copy()
                s1.sort_values(keys[1], inplace=True)
                for key2 in s1[keys[1]].unique():
                    s2 = s1[s1[keys[1]]==key2].copy()
                    s2.sort_values('ptdate', inplace=True)
                    for y in ys:
                        self.load_data(x=s2[x].values, y=s2[y].values, ylabel=y, label=key2, title=key1, titlesize=titlesize)
        
    def load_data(self, x, y=None, 
             color='hotpink',
             marker='.', 
             label='',
             xlabel='', 
             ylabel='', 
             rotation=0,
             xsize=15,
             ysize=15,
             width=0.5,
             title='',
             xtype='time',
             plot_type='曲线',
             legend=True,
             legendsize=20,
             to_pin=False,
             bins=10,
             legend_loc=0,
             titlesize=20,
             barcolor=[]):
        '''
        load data into dict
        args:
            -- genearl 
            marker: ['o', '.', ',', 'x', '+', 'v', '^', '<', '>', 's', 'd']
            color: ['hotpink','blue','green','red','orange','black','yellow']
            label: legend information
            xlabel: the label of x axis
            ylabel: the label of y axis
            rotation: the rotation degree of x axis
            xsize: the font size of the scale of x axis
            ysize: the font size of the scale of y axis
            title: the title of subplot
            xtype: the type of x axis, time, numeric, what else...
            plot_type: 'curve', 'bar', 'hist', '曲线', '直方图'
            legend: whether to show the label
            legendsize: the font size of legend
            to_pin: translate the Chinese font into pinyin
            titlesize : dict
                    A dictionary controlling the appearance of the title text, the default fontdict is:
                    {'fontsize': rcParams['axes.titlesize'],
                     'fontweight' : rcParams['axes.titleweight'],
                     'verticalalignment': 'baseline',
                     'horizontalalignment': loc}

            -- bar 
            width: the width of bar

            -- hist 
            bins: the number of bars
        '''
        if y is not None:
            assert len(x) >= 0 and len(y)==len(x), 'data length is 0 or the lengh of x is not equal to y'

        if xtype == 'time':
            x = [datetime.datetime.strptime(t, '%Y-%m-%d').date() for t in x]

        if to_pin:
            x = [hanzi_to_pinyin(s) for s in x]

        self.data_list.append({'x':x, 'y':y, 'marker':marker, 'color':color, 'titlesize':titlesize, 'barcolor':barcolor, \
                               'legend_loc':legend_loc, 'label':label, 'plot_type':plot_type, 'xlabel':xlabel, \
                               'rotation':rotation,'title':title,'xtype':xtype, 'xsize':xsize, 'ysize':ysize, \
                               'ylabel':ylabel, 'width':width, 'legend':legend, 'bins':bins, 'legendsize':legendsize})

    def get_row_col(self, count):
        '''
        calculate the row and column number according to the number of data passed
        return row, column
        '''
        if count == 1:
            return 1, 1
        if count <=self.count_cut:
            if count % 2 == 0:
                return int(count/2), 2
            else:
                return int(np.ceil(count/3)), 3
        else:
            return int(np.ceil(np.sqrt(count))), int(np.ceil(np.sqrt(count)))

    def show(self, exchange=False, hspace=0.3, wspace=0.1, dfs={}):
        '''
        build a figure frame to show data list
        args:
            exchange: False/True, exchange the row number with the column number
            hspace: control the subplot distance in the vertical direction
            wspace: control the subplot distance in the horizontal direction
            dfs: dataframe describe
        '''
        
        data_count = len(self.data_list)
        graph_count = int(np.ceil(data_count/self.capacity))

        if exchange:
            self.ncols, self.nrows = self.get_row_col(graph_count)
        else:
            self.nrows, self.ncols = self.get_row_col(graph_count)

        _, self.axes = plt.subplots(nrows=self.nrows, ncols=self.ncols, 
                                    figsize=(self.figsize[0] * self.ncols, self.figsize[1] * self.nrows))
        plt.subplots_adjust(wspace=wspace, hspace=hspace)

        self.subplot_index = 0
        labels = []
        xlabels = []
        for i in range(data_count):
            ax = self.get_ax()
            d = self.data_list[i]
            xlabels = d['x'] if len(xlabels) < len(d['x']) else xlabels
            if '曲' in d['plot_type'] or '线' in d['plot_type'] or 'line' in d['plot_type']:
                ax.plot(d['x'], d['y'], marker=d['marker'], label=d['label'])
            elif '条' in d['plot_type'] or 'bar' in d['plot_type']:
                ax.bar(d['x'], d['y'], color=d['color'] if len(d['barcolor'])==0 else d['barcolor'], width=d['width'])
            elif '散' in d['plot_type'] or 'scatter' in d['plot_type']:
                if len(d['barcolor']) > 0:
                    ax.scatter(d['x'], d['y'], marker=d['marker'], c=d['barcolor'])
                else:
                    ax.scatter(d['x'], d['y'], marker=d['marker'])
            elif '雷' in d['plot_type']:
                ax = plt.subplot(111, projection='polar')
                ax.set_rlim(0,12)
                ax.plot(d['x'], d['y'], '.--', label=d['label'], alpha=0.9);
                ax.fill(d['x'], d['y'], alpha=0.2)
            elif '饼' in d['plot_type'] or 'pie' in d['plot_type']:
                ax.pie(d['x'], labels=d['label'], autopct='%1.1f%%', shadow=False, startangle=90)
            elif '盒' in d['plot_type'] or 'box' in d['plot_type']:
                pass
            elif '分布' in d['plot_type'] or '直方' in d['plot_type'] or 'hist' in d['plot_type']:
                s = np.mean(d['x']); label = 'mean='+str(round(s,4))
                h = ax.hist(d['x'], bins=d['bins'], color=d['color'])
                ax.vlines(s, h[0].min(), h[0].max(), label=label, color='black', linestyle='--')
                labels.append(label)
            else:
                raise 'no corresponding plot type'

            labels.append(d['label'].decode('Utf-8'))
            ax.set_xlabel(d['xlabel'], fontproperties=myfont)
            ax.set_ylabel(d['ylabel'], fontproperties=myfont)
            plt.title(d['title'].decode('Utf-8'), fontproperties=myfont)
            ax.tick_params(axis='x', labelsize=d['xsize'])
            ax.tick_params(axis='y', labelsize=d['ysize'])
            ax.set_title(d['title'].decode('Utf-8'), fontdict={'fontsize':d['titlesize']}, fontproperties=myfont)
            if d['rotation'] > 0 and not isinstance(xlabels[0], datetime.date):
                    ax.set_xticklabels(xlabels, rotation=d['rotation'])

            if i >= self.capacity * (self.subplot_index+1)-1 or i == data_count-1:
                self.subplot_index += 1
                if d['legend']:
                    ax.legend(labels, fontsize=d['legendsize'], loc=d['legend_loc'], prop=myfont)
                labels = []
                xlabels = []

        if graph_count > self.count_cut or len(self.savepath) > 0:
            print 'save figure'
            plt.savefig(self.savepath)
            plt.close()
        else:
            plt.show()

        self.data_list = [] #reuse plot_max()

        if len(dfs) > 0:
            for key, df in dfs.items():
                print '\n*********', key, '*********'
                print '>>> Data <<<'
                print df.head()
                print df.tail()

                print '\n>>> Describe <<<'
                print df.describe()


def compare_wc(d1, d2, keys=['price', 'gmv', 'gp', 'sales'], labels=[0,1]):
    graph = plot_max(figsize=(16,5), capacity=2)
    for key in keys:
        graph.load_data(d1.ptdate.values, d1[key].values,
                     xlabel='ptdate', ylabel=key, xtype='time', label=labels[0],
                    title=key+' of total warehouse', rotation=90, plot_type='line')
        graph.load_data(d2.ptdate.values, d2[key].values,
                     xlabel='ptdate', ylabel=key, xtype='time',label=labels[1],
                    title=key+' of total warehouse', rotation=90, plot_type='line')

    graph.show(dfs={labels[0]:d1, labels[1]:d2})

def hanzi_to_pinyin(one_str,flag=''):
    '''
    将汉字转化为对应的拼音
    '''
    translator=Pinyin()
    one_kw_pinyin=translator.get_pinyin(unicode(one_str), flag).strip()
    print '{0} Pinyin is: {1}'.format(one_str.decode('utf-8'),one_kw_pinyin)
    return one_kw_pinyin

def pd_to_pin(df, key):
    df[key+'_en'] = df[key].apply(hanzi_to_pinyin)

def stats_concat(df, groupkey=[], fill={}, method='mean'):
    if isinstance(df, pd.Series):
        df = pd.Series({'mean':df.mean(), 'std':df.std()})
    else:
        cols = df.columns
        if len(groupkey)>0:
            add = df.groupby(groupkey).mean()
            add.reset_index(inplace=True)
        else:
            add = df.mean()
            add = pd.DataFrame(add).T
            add.reset_index(inplace=True)
            if len(fill) == 0: add.index = [method]

        for key, value in fill.items():
            add[key] = value
        df = pd.concat([df, add])
        df = df[cols]
    return df

def astype(df, columns, type):
    for col in columns:
        df[col] = df[col].astype(type)

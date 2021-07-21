import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def conv_duration(df):
    """Make new column 'duration_s' in dataframe with 'duration_ms' column"""
    
    df['duration_s'] = df['duration_ms']/1000    

    
def conv_year(df):
    """Make new column 'year' in dataframe with 'release_date' column"""
    
    df['year'] = pd.to_datetime(df['release_date']).dt.year

    
def make_df(data_loc):
    """Make dataframe with relevant columns from data stored in data_loc location"""
    
    df = pd.read_csv(data_loc)
    if 'duration_s' not in df.columns: 
        conv_duration(df)  
        print("Added 'duration_s' column")
    if 'year' not in df.columns:
        conv_year(df)
        print("Added 'year' column")
        
    return df


def slice_data(df,year,popularity,cutoff=np.inf):
    """
    Extract relevant data from dataframe

    Args:
        df (DataFrame): pandas dataframe with columns: 'year', 'popularity' and 'duration_s'
        year (tuple): tuple with year range
        popularity (tuple): tuple with popularity range
        cutoff (float): duration cutoff in seconds

    Returns:
        data (DataFrame):    
    """

    data = df[
        (df['year'] >= year[0]) & 
        (df['year'] <= year[1]) & 
        (df['popularity'] >= popularity[0]) & 
        (df['popularity'] <= popularity[1]) & 
        (df['duration_s'] <= cutoff)
    ].copy()
    
    return data


def save_visual(location,name):
    """Save the visualisation in specified location with specified name"""
    
    link = location + name + '.jpg'
    plt.savefig(link,dpi=200)
    print(f'Visalisation saved in {link}')

    
def make_hist(df,year,popularity,cutoff,bins,xlim,kde=True,color='blue',facecolor='snow',
              size=(15,8),save=False,save_loc='./',save_name='histogram'):
    """
    Makes histogram of duration distribution of songs from relevant years and popularity range
    
    Args:
        df (DataFrame): DataFrame with the relevant data and columns: 'year', 'popularity' and 'duration_s'
        year (tuple): tuple with year range
        popularity (tuple): tuple with popularity range
        cutoff (float): duration cutoff in seconds
        bins (int): number of bins on the histogram
        xlim (tuple): limits on x axis [x1,x2]
        kde (boolean): include kernel density estimation curve (default is True)
        color (string): color of bins and kde curve (default is 'blue')
        facecolor (string): color of background in seaborn (default is 'snow')
        size (tuple): figsize in matplotlib (default is (15,8))
        save (boolean): save figure (default is False)
        save_loc (string): location where figure is saved (default is './')
        save_name (string): name of saved figure (default is 'histogram')
    """

    data = slice_data(df,year,popularity,cutoff)

    plt.figure(figsize=size)
    sns.set(rc={'axes.facecolor' :facecolor,
                'grid.color'     :'grey'})

    hist = sns.histplot(data['duration_s'],bins=bins,kde=kde,color=color)

    hist.set_title(
        f'Tracks from {year[0]}-{year[1]} with popularity {popularity[0]}-{popularity[1]}',fontsize=25)
    hist.set_xlabel('Duration (seconds)',fontsize=20)
    hist.set_ylabel('Count',fontsize=20)
    
    plt.yticks(fontsize=15)
    plt.xticks(fontsize=15)
    plt.xlim(xlim)
    plt.text(hist.get_xlim()[1]*0.65, hist.get_ylim()[1]*0.85,
             f'Number of tracks: {data.shape[0]}',size='xx-large',weight='bold')

    y = hist.lines[0].get_ydata()
    maxi = np.argmax(y)
    x = hist.lines[0].get_xdata()[maxi]

    plt.text(hist.get_xlim()[1]*0.65, hist.get_ylim()[1]*0.75,
             f'Peak duration (seconds): {x:.0f}',size='xx-large',weight='bold')

    print(f'{year} tracks: {data.shape[0]}')

    if save == True:
        save_visual(save_loc,save_name)
        
def make_line(df,year,popularity,width=5,color='blue',facecolor='snow',
              size=(15,8),save=False,save_loc='./',save_name='trend_line'):
    """
    Makes trend line of yearly average duration of songs from relevant years and popularity range
    
    Args:
        df (DataFrame): DataFrame with the relevant data and columns: 'year', 'popularity' and 'duration_s'
        year (tuple): tuple with year range
        popularity (tuple): tuple with popularity range
        width (int): width of trend line (default is 5)
        color (string): color of bins and kde curve (default is 'blue')
        facecolor (string): color of background in seaborn (default is 'snow')
        size (tuple): figsize in matplotlib (default is (15,8))
        save (boolean): save figure (default is False)
        save_loc (string): location where figure is saved (default is './')
        save_name (string): name of saved figure (default is 'trend_line')
    """
    
    data = slice_data(df,year,popularity) 
    data = data.groupby('year')['duration_s'].mean().reset_index()

    plt.figure(figsize=size)
    sns.set(rc={'axes.facecolor' :facecolor,
                'grid.color'     :'grey'})

    line = sns.lineplot(x=data['year'],y=data['duration_s'],color=color,linewidth=width)

    line.set_title(
        f'Average duration of tracks from {year[0]}-{year[1]} with popularity {popularity[0]}-{popularity[1]}',
        fontsize=25)
    line.set_xlabel('Year',fontsize=20)
    line.set_ylabel('Duration (seconds)',fontsize=20)

    plt.yticks(fontsize=15)
    plt.xticks(fontsize=15)

    if save == True:
        save_visual(save_loc,save_name)
        
def make_barplot(df,year,popularity,tick_rotation=False,color='blue',facecolor='snow',
              size=(15,8),save=False,save_loc='./',save_name='bar_plot'):
    """
    Makes bar plot of yearly number of songs from relevant years and popularity range
    
    Args:
        df (DataFrame): DataFrame with the relevant data and columns: 'year', 'popularity' and 'duration_s'
        year (tuple): tuple with year range
        popularity (tuple): tuple with popularity range
        tick_rotation (boolean): rotate x ticks 90 degrees (vertical) to fit in more text (default is False)
        color (string): color of bins and kde curve (default is 'blue')
        facecolor (string): color of background in seaborn (default is 'snow')
        size (tuple): figsize in matplotlib (default is (15,8))
        save (boolean): save figure (default is False)
        save_loc (string): location where figure is saved (default is './')
        save_name (string): name of saved figure (default is 'bar_plot')
    """
        
    data = slice_data(df,year,popularity)
    data = data.groupby('year')['id'].count().reset_index()

    f = np.array(data).T

    plt.figure(figsize=size)
    sns.set(rc={'axes.facecolor' :facecolor,
                'grid.color'     :'grey'})

    bar = sns.barplot(x=f[0], y=f[1], color=color)

    bar.set_title(
        f'Number of tracks from {year[0]}-{year[1]} with popularity {popularity[0]}-{popularity[1]}',
        fontsize=25)
    bar.set_xlabel('Year',fontsize=20)
    bar.set_ylabel('Count',fontsize=20)

    plt.yticks(fontsize=15)
    
    if tick_rotation == True:
        plt.xticks(fontsize=15,rotation=90)
    else:
        plt.xticks(fontsize=15)

    if save == True:
        save_visual(save_loc,save_name)

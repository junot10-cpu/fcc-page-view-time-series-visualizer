from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Folder of this project: the CSV is read from it and the charts are saved
# in it, no matter which folder the script is run from.
BASE_DIR = Path(__file__).resolve().parent

MONTHS = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December',
]

# Import data (parse the dates and use them as the index)
df = pd.read_csv(
    BASE_DIR / 'fcc-forum-pageviews.csv',
    parse_dates=['date'],
    index_col='date',
)

# Clean data: remove the days in the top 2.5% and bottom 2.5% of page views
df = df[
    (df['value'] >= df['value'].quantile(0.025))
    & (df['value'] <= df['value'].quantile(0.975))
]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig
    fig.savefig(BASE_DIR / 'line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot: average daily page views
    # for each month, grouped by year
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()
    df_bar = (
        df_bar.groupby(['year', 'month'])['value']
        .mean()
        .unstack()
        .reindex(columns=MONTHS)
    )

    # Draw bar plot
    ax = df_bar.plot(kind='bar', figsize=(10, 8))
    fig = ax.get_figure()
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months')

    # Save image and return fig
    fig.savefig(BASE_DIR / 'bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    month_order = [m[:3] for m in MONTHS]

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))

    sns.boxplot(data=df_box, x='year', y='value', ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    sns.boxplot(data=df_box, x='month', y='value', order=month_order, ax=ax2)
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    # Save image and return fig
    fig.savefig(BASE_DIR / 'box_plot.png')
    return fig

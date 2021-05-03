# -*- coding: utf-8 -*-
# script : timeline_plotter.py

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime

def construct_timeline(dict_data):

    corporation_names = dict_data["Corporation"]
    founded_dates = dict_data["Founded"]
    print(founded_dates)


    
    # Convert date strings (e.g. 2014-10-18) to datetime
    # dates = [datetime.strptime(d, "%d/%m/%Y") for d in founded_dates]
    # dates = [parse_date(d) for d in founded_dates]
    # print(dates)

    # Chooses various sized levels
    levels = np.tile([-5, 5, -3, 3, -1, 1],
                 int(np.ceil(len(founded_dates)/6)))[:len(founded_dates)]

    
    # Create figure and plot a stem plot with the date
    fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
    ax.set(title="Timeline of Corporations & Business Organisations")

    # The vertical stems..
    ax.vlines([1,2,3], np.repeat(0, 3), [1,2,3], color="tab:red", linestyles="dashdot")

    # Baseline and markers
    ax.plot(founded_dates, np.zeros_like(founded_dates), "-o",
        color="k", markerfacecolor="w") 

    # annotates lines of graph
    for d, l, names in zip(founded_dates, levels, corporation_names):
        ax.annotate(names, xy=(d, l),
                xytext=(-3, np.sign(l)*3), textcoords="offset points",
                horizontalalignment="right",
                verticalalignment="bottom" if l > 0 else "top")

    # format xaxis with 4 month intervals   
    ax.get_xaxis().set_major_locator(mdates.MonthLocator(interval=4))
    ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

    # remove y axis and spines
    ax.get_yaxis().set_visible(False)
    for spine in ["left", "top", "right"]:
        ax.spines[spine].set_visible(False)

    ax.margins(y=0.1)
    plt.show()


def parse_date(date_txt):
    try:
        return datetime.strptime(date_txt, "%d/%m/%Y")
    except ValueError:
        return None
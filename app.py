import yfinance as yf
import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import date, timedelta
import warnings
warnings.simplefilter("ignore")

def companies():
    """S&P100 Components data."""
    df = pd.read_csv('nasdaq_100.csv', sep=';')
    key = [l for l in df.Symbol]
    value = [g for g in df.Company]
    companies_dict = dict(zip(key, value))
    return companies_dict


def analysis(params):
    """Transform values."""
    d = pd.DataFrame(columns=params.values())
    std_list = []
    rnd = []
    close_0 = []
    close_1 = []
    for key, value in params.items():
        try:
            df = yf.download(tickers=key, period='1mo', interval="1d", progress=False)
        except:
            print(key, "didn't found")
            
        if len(df) > 0:
            std_value = float(df['Close'].diff().std().iloc[0])  
            rnd_value = float((df['Close'].values[-1] - df['Close'].values[0]) / df['Close'].values[0]) 
            close_0_value = float(df['Close'].values[0])  
            close_1_value = float(df['Close'].values[-1])  
            std_list.append(std_value)
            rnd.append(rnd_value)
            close_0.append(close_0_value)
            close_1.append(close_1_value)
        else:
            d = d.drop(columns=value, errors='ignore')


    d = d.T
    d['rnd'] = rnd
    d['std'] = std_list
    d['Close_t0'] = close_0
    d['Close_t1'] = close_1
    d = d.reset_index().rename(columns={'index': 'ticker'})
    median_std = d['std'].median()
    median_rnd = d['rnd'].median()
    return d, median_std, median_rnd


def plotting():
    """Plot the graph."""
    d, median_std, median_rnd = analysis(companies())
    today = date.today()
    today_str = today.strftime("%Y/%m/%d")
    d1 = today - timedelta(days=30)
    d1 = d1.strftime("%Y/%m/%d")
    fig = px.scatter(d, x="std", y="rnd",  text="ticker", title='Nasdaq100 Daily Data from {} to {}'.format(d1, today_str))
    fig.update_traces(textposition="bottom right")
    fig.add_hline(y=median_rnd, line_color="red")
    fig.add_vline(x=median_std, line_color="red")
    
    st.plotly_chart(fig)


def main():
    """Define main function."""
    plotting()


if __name__ == "__main__":
    main()

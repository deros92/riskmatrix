"""Risk & Returns matrix: daily data."""
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import date, timedelta


def companies():
    """S&P100 Components data."""
    df = pd.read_csv(r'C:\Users\yurid\Dtrades folder\nasdaq_100.csv', sep=';')
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
            df = yf.download(tickers=key, period='30d',
                    interval="1d", progress=False)
        except:
            print(key, "didn't found")
            
        if len(df) > 0:
            std_list.append(df['Close'].diff().std())
            rnd.append((df['Close'][len(df)-1] - df['Close'][0])/df['Close'][0])
            close_0.append(df['Close'][0])
            close_1.append(df['Close'][len(df)-1])
        else:
            d = d.drop(columns=value)

    d = d.T
    d['rnd'] = rnd
    d['std'] = std_list
    d['Close_t0'] = close_0
    d['Close_t1'] = close_1
    d = d.reset_index().rename(columns={'index': 'ticker'})
    median_std = d['std'].median()
    median_rnd = d['rnd'].median()
    return d, median_std, median_rnd


def plotting(save=False, draw=True):
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
    if save:
        fig.write_html("riskmatrix_nasdaq.html")
    if draw:
        fig.show()


def main():
    """Define main function."""
    plotting(save=True, draw=False)


if __name__ == "__main__":
    # main()
    main()

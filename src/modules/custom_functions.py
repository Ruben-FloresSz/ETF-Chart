import pandas as pd
import os
import mplfinance as mpf

def data_dict(data_path):
    """
    Función para crear un diccionario con un conjunto de archivos CVS
    """
    list_stocks = os.listdir(data_path)
    repositorio_stocks = {}

    for ticker in list_stocks:
        path = os.path.join(data_path, ticker)
        ticker_name = os.path.splitext(ticker)[0]
        repositorio_stocks[ticker_name] = pd.read_csv(path)
    
    return repositorio_stocks 



def candle_chart(df, ticker, title="Candlestick Chart", save_fig=False, save_path="o"):
    """
    Función para crear graficas de velas
    """
    db_dict = {
        "m_date" : "date",
        "c_adjusted_open": "Open",
        "c_adjusted_high": "High",
        "c_adjusted_low": "Low",
        "m_adjusted_close": "Close",
        "m_volume": "Volume",
        "m_close": "Adj Close",
        "c_relative_strength_index_14d" : "RSI"

         }

    df_rename = df.rename(columns=db_dict)
    if "date" in df_rename.columns:
        df_rename["date"] = pd.to_datetime(df_rename["date"])
        df_rename = df_rename.set_index("date")
        
    
    RSI = mpf.make_addplot(df_rename["RSI"], panel = 2, color="green")
    ax = mpf.plot(df_rename, type="candle", volume=True, title=title, addplot=RSI,  
                  mav=(21,63, 252), mavcolors=('red', 'green', 'orange'),figsize=(10, 6), 
                  style= "charles")
   
    if save_fig:
       file_name = f"{ticker}_candlestick.png"
       path = os.path.join(save_path, file_name)
       mpf.plot(df_rename, type="candle", volume=True, title=title, addplot=RSI, 
                mav=(21,63, 252), mavcolors=('red', 'green', 'orange'), figsize=(10, 6), 
                savefig=path, style="charles")
       return print(f"Graph save in: {path}")  

       return ax  







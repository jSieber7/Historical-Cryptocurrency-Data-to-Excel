import bs4 as bs
import urllib.request
import pandas as pd
import xlwt


def retrieve(coin='Bitcoin', start_date='Jan 1, 2017', end_date='Jan 1, 2018'):
    """Function dedicated to scraping coinmarketcap and retrieving a Pandas DataFrame. The coin and date is able to be
    changed easily"""

    # Ensures proper formatting of user inputs
    coin = coin.lower()
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    start_date = start_date.strftime('%Y%m%d')
    end_date = end_date.strftime('%Y%m%d')


    # Retrieves data with BeautifulSoup and parses
    url = 'https://coinmarketcap.com/currencies/' + coin + '/historical-data/?start=' + start_date + '&end='+end_date
    print(url)
    link = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(link, "html.parser")
    prices_table = soup.find_all('tr')

    # Creates list of dictionaries to feed into the DataFrame
    list_of_dic = []
    for count, itemset in enumerate(prices_table):
        date = itemset.text.splitlines()[1]
        open = itemset.text.splitlines()[2]
        high = itemset.text.splitlines()[3]
        low = itemset.text.splitlines()[4]
        close = itemset.text.splitlines()[5]
        volume = itemset.text.splitlines()[6]
        marketcap = itemset.text.splitlines()[7]
        dictionary = {'Date' : date, 'Coin' : coin.capitalize(), 'Opening Price' : open,'Closing Price' : close, 'Low' :
            low, 'High': high, 'Volume' : volume, 'Market Cap': marketcap}
        list_of_dic.append(dictionary)

    # Creates and sends our DataFrame
    df = pd.DataFrame(list_of_dic)
    df = df.drop(df.index[0])
    df['Date'] = pd.to_datetime(df['Date'])
    # df.set_index(['Date','Coin'], inplace = True)
    return df


def retrievealldata(coinlist, s_date = 'Jan 1, 2017', e_date = 'Jan 1, 2018'):
    """This function uses the retrieve function multiple times
    in order to create a DataFrame with multiple cryptocoins"""

    if coinlist is list:
        raise Exception('Must pass a list')

    alldata = pd.DataFrame()
    for coin in coinlist:
        df = retrieve(coin, s_date, e_date)
        alldata = alldata.append(df)

    alldata = alldata.sort_values(by=['Date'], ascending=True)
    # alldata.Date = alldata.Date.dt.strftime('%b %d, %Y')
    alldata.set_index(['Date', 'Coin'], inplace=True)

    return alldata

#
# def quick_fix(dataf):
#     """Fixes some columns names to the proper naming for CoinMarketCap """
#
#
#     dataf.Currency[dataf['Currency'] == 'Ethereum Classic'] = 'ethereum-classic'
#     dataf.Currency[dataf['Currency'] == 'Infinium-8'] = 'infchain'
#     dataf.Currency[dataf['Currency'] == 'Aeon Coin'] = 'aeon'
#     dataf.Currency[dataf['Currency'] == 'bytecoin'] = 'bytecoin-bcn'
#
#     return dataf



# example calls
# final_data = retrievealldata(coinlist =['Bitcoin','Ethereum','Ripple'],s_date= 'Jan 1, 2017',e_date= 'Jan 1, 2018')


# final_data.Date = final_data.Date.dt.strftime('%b %d, %Y')
# final_data.to_excel(excel_writer='export.xls')




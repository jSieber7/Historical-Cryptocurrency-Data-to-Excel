import pandas as pd
from Scrape import scrape
import xlwt



# Load data
df = pd.read_csv('Dirty Data.csv', parse_dates=True).dropna(how='all')
df = df.drop([547])

# Assures right currency naming
df.loc[df['Currency'] == 'Ethereum Classic','Currency'] = 'Ethereum-Classic'
df.loc[df['Currency'] == 'Infinium-8','Currency'] = 'Infchain'
df.loc[df['Currency'] == 'Aeon Coin','Currency'] = 'Aeon'
df.loc[df['Currency'] == 'Bytecoin','Currency'] = 'Bytecoin-bcn'


# Create a list of the coins we want more information on and the dates we want retrived
coin_list = df['Currency'].unique()



# Gets the minimum date and the maximum date to search for
df['Date'] = pd.to_datetime(df['Date'])
first_date = (df.Date.min())
last_date = (df.Date.max())


# Cleans the data
df.rename(columns={'Currency': 'Coin'},inplace=True)
df.set_index(['Date', 'Coin'], inplace=True)
df = df.drop(['Value USD','Value BTC','Coin Price'], axis = 1)
df.loc[:,'Balance':'Total mined:']=df.loc[:,'Balance':'Total mined:'].fillna(0)
df.Status = df.Status.fillna('OFF LINE')



# Calls our function to scrape
bs_df = scrape.retrievealldata(coin_list, s_date = first_date, e_date = last_date)


# Renames columns for a clean join between our dirty data and our beaufiul soup data
bs_df = bs_df.reset_index()
bs_df.loc[bs_df['Coin'] == 'Digitalnote','Coin'] = 'DigitalNote'
bs_df.loc[bs_df['Coin'] == 'Ethereum-classic','Coin'] = 'Ethereum-Classic'
bs_df.loc[bs_df['Coin'] == 'Fantomcoin','Coin'] = 'FantomCoin'
bs_df.set_index(['Date', 'Coin'], inplace=True)


# Joins and then calculates a final USD value column
final_df = df.join(bs_df, how='left')
final_df['Market Cap'] = final_df['Market Cap'].str.replace(',', '')
final_df['Volume'] = final_df['Volume'].str.replace(',', '')
final_df.iloc[:,4:] = final_df.iloc[:,4:].apply(pd.to_numeric,errors='coerce')
final_df['USD Value'] = final_df.apply(lambda row: row['Balance']*row['Closing Price'], axis=1)


# Exports the data
final_df.to_excel(excel_writer='export.xls')


#import basic modules required
from nsepy import get_history
import datetime 
from datetime import date 
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np 


s = date(2017,12,31)

#Tables ‘niftydata’ and ‘optiondata’ created to store data of Nifty future and options respectively
nifty_fut = get_history(symbol="NIFTY", 
                        start=s, 
                        end=s, 
                        index=True,
                        futures=True, 
                        expiry_date=s)
niftydata = nifty_fut

nifty_opt = get_history(symbol="NIFTY", 
                        start=s,
                        end=s,
                        index=True,
                        option_type='CE',
                        strike_price=15000,
                        expiry_date=s)
optiondata = nifty_opt

#date of 1st January 2018 assigned in variable ‘s’. Earlier this variable was having date of 31st December 2017 so 1 day increased.
s = s + datetime.timedelta(days=1)

#expiry dates of January, February taken in variable
expiry = [date(2018,1,25), date(2018,2,22)]
# expiry = [date(2018,2,22),date(2018,12,27)]
#date(2018,4,26),date(2018,5,31)]


#Loops created to fetch data of all expiries
for x in expiry:
    expiry = x 
    nifty_fut = get_history(symbol="NIFTY", 
                            start=s, 
                            end=x,  
                            index=True, 
                            futures=True,
                            expiry_date=x) 
    #Nifty future data of fetched above stored in nifty data table. Every month data will be appended in ‘niftydata’ table.
    niftydata = niftydata.append(nifty_fut)
    

    #Highest value of Nifty taken in variable ‘High’
    high = nifty_fut[['Close']].max() 
    
    #Lowest value of Nifty taken in variable ‘low’
    low = nifty_fut[['Close']].min()
    
    #values rounded off to get nearest 100 strike
    high = int((round(high/100)*100)+100) 
    #values rounded off to get nearest strike
    low = int((round(low/100)*100)-100)
    
    
    # one more loop created to fetch option data
    for z in range (low, high, 100):
        #Call data appended in table ‘optiondata’
        nifty_opt = get_history(symbol="NIFTY",
                                start=s,
                                end=expiry,
                                index=True,
                                option_type='CE',
                                strike_price=z,
                                expiry_date=x)
        optiondata = optiondata.append(nifty_opt)
        
        #Put data appended in table ‘optiondata’
        nifty_opt = get_history(symbol="NIFTY",
                                start=s,
                                end=expiry,
                                index=True,
                                option_type='PE',
                                strike_price=z,
                                expiry_date=x)
        optiondata = optiondata.append(nifty_opt)
        
    #first date of next expiry assigned in variable ‘s'
    s = x + datetime.timedelta(days=1) 
        
    
####################################################

NiftyCF = pd.DataFrame({"Nifty": niftydata["Close"]})

NiftyCO = pd.DataFrame({"Expiry":optiondata['Expiry'],
                       "Type":optiondata['Option Type'],
                       "Strike":optiondata['Strike Price'],
                       "Last": optiondata['Last']})

Opttable = pd.pivot_table(NiftyCO, values ='Last', index =['Date', 'Type', 'Expiry'], columns =['Strike'], aggfunc = np.sum)
Opttable = Opttable.join(NiftyCF)
print(Opttable)


####################################################


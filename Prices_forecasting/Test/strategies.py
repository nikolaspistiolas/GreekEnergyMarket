from urllib.parse import urljoin
import datetime as datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import csv
from csv import reader
import math
import matplotlib as mpl
plt.rcParams["figure.figsize"] = (14,10)
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 9}

mpl.rc('font', **font)


from matplotlib.pyplot import figure

data = pd.read_csv('Final_data_april.csv')

data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', drop=True, inplace=True)
data.index.name = None
######## Reference Revenue

reference = pd.DataFrame()
reference["Day_ahead_price"] = data["Day_ahead_price"]
reference["Production"]      = data["Production"].values
reference['Revenue']         = reference["Production"]*reference["Day_ahead_price"]

reference_revenue = reference["Revenue"].sum()


print('The revenue for reference (Perfect Forecast): {}'.format(reference_revenue))



######## Deterministic Strategy

strategy_deterministic = pd.DataFrame()
strategy_deterministic[["Day_ahead_price","Imbalance_price"]] = data[["Day_ahead_price","Imbalance_price"]]
strategy_deterministic["Bid"] = 1.02*data['Forecast'].values
strategy_deterministic["Production"] = data["Production"].values
strategy_deterministic["Dayahead Revenue"] = strategy_deterministic['Bid']*strategy_deterministic["Day_ahead_price"]
strategy_deterministic['Imbalance_Revenue'] = strategy_deterministic['Imbalance_price']*(strategy_deterministic['Bid'] - strategy_deterministic['Production'])
strategy_deterministic['Total_Revenue'] = strategy_deterministic["Production"]*strategy_deterministic["Day_ahead_price"] - (strategy_deterministic["Day_ahead_price"]- strategy_deterministic["Imbalance_price"])*(strategy_deterministic["Production"] - strategy_deterministic["Bid"])

strategy_deterministic_revenue = strategy_deterministic['Total_Revenue'].sum()
strategy_deterministic_ratio = strategy_deterministic_revenue/reference_revenue

##### We are going to add now the Penalty fro the imbalances beeing the Tolerance level of our Deviations

DEV_deterministic = strategy_deterministic["Production"] - strategy_deterministic["Bid"]
ADEV_deterministic = sum(DEV_deterministic)

NADEV_deterministic = ADEV_deterministic/sum(strategy_deterministic["Production"])

RMSDEV_deterministic = math.sqrt(sum(DEV_deterministic**2))

TOL_DETERMINISTIC = max(0.2,min(1,(0.35-0.009*(sum(strategy_deterministic["Production"])**(0.28)))))

NCBAL_deterministic = max((10*ADEV_deterministic)*(NADEV_deterministic - TOL_DETERMINISTIC),0)

final_revenue_det = strategy_deterministic_revenue - NCBAL_deterministic

print('The final revenue from the determenistic strategy is : {}'.format(final_revenue_det))


####### Probabilistic Strategy
### 1) We iterate over all possible sets of quantile combinations
### 2) Which combination gives the best overall Revenue Gain


##################################################################
quantiles = data.iloc[:,1:20].columns

list_of_quantiles = [["q5","q95"],["q10","q90"],["q15","q85"],["q20","q80"],["q25","q75"],["q30","q70"],["q35","q65"],["q40","q60"],["q45","q65"]]

for i in range(len(list_of_quantiles)):
    # Gets the class
    comb = list_of_quantiles[i]
    c1 = comb[0]
    c2 = comb[1]
        ######## Probabilistic Strategy - Lets Play with the quantiles
    strategy3_probabilistic = data

        ##### Using Probabilistic Forecast (Risk Constrained Trading Strategy)

    risk_down = strategy3_probabilistic[strategy3_probabilistic['Predicted'] == 0][[c1,"Day_ahead_price","Imbalance_price","Production"]]
    risk_up   = strategy3_probabilistic[strategy3_probabilistic['Predicted'] == 1][[c2,"Day_ahead_price","Imbalance_price","Production"]]


    risk_down["Revenue"] = risk_down["Production"]*risk_down["Day_ahead_price"] - (risk_down["Day_ahead_price"]- risk_down["Imbalance_price"])*(risk_down["Production"] - risk_down[c1])
    risk_up["Revenue"] = risk_up["Production"]*risk_up["Day_ahead_price"] - (risk_up["Day_ahead_price"] - risk_up["Imbalance_price"])*(risk_up["Production"] -risk_up[c2])


    strategy3_probabilistic_revenue = risk_down['Revenue'].sum() + risk_up["Revenue"].sum()
    strategy3_ratio_probabilistic = strategy3_probabilistic_revenue/reference_revenue


    print(strategy3_probabilistic_revenue)


    result = pd.concat([risk_up, risk_down], ignore_index=False, sort=True)
    result = result.sort_index()
    result["Determenistic_Strategy"] = strategy_deterministic["Total_Revenue"]
    result["Probabilistic_Strategy"] = result["Revenue"]


    result[c2].fillna(result[c1],inplace = True)
    del result[c1]

    result["Bid"] = result[c2]

    DEV_probabilistic = result["Production"] - result["Bid"]
    ADEV_probabilistic = sum(DEV_probabilistic)

    NADEV_probabilistic = ADEV_probabilistic/sum(strategy3_probabilistic["Production"])

    RMSDEV_probabilistic = math.sqrt(sum(DEV_probabilistic**2))

    TOL_probabilistic = max(0.2,min(1,(0.35-0.009*(sum(result["Production"])**(0.28)))))

    NCBAL_probabilistic = max((10*ADEV_probabilistic)*(NADEV_probabilistic - TOL_probabilistic),0)
    print(NCBAL_probabilistic)

    final_revenue_probabilistic = strategy3_probabilistic_revenue - NCBAL_probabilistic

    print('The final revenue gain from the probabilistic strategy is : {}'.format(final_revenue_probabilistic))

######## Plot to shpw the difference

    #result_daily = result.iloc[:,:].resample('D').sum()
    #result_daily["Date"] = result_daily.index
    #result_daily.head()
    #ax = result_daily.plot(x="Date", y="Probabilistic_Strategy", kind="bar",fc=(0, 0, 1, 0.5))
    #result_daily.plot(x="Date", y="Determenistic_Strategy", kind="bar", ax=ax,fc=(1, 0, 0, 0.5))
    #plt.show()



    y = [reference_revenue, final_revenue_det,final_revenue_probabilistic]
    plt.figure(figsize=[15,10])
    plt.xticks(rotation=45)

    plt.bar(['Perfect Knowledge', 'Forecast (Determenistic)', f'Probabilistic model with {c1,c2}'] , y)
    plt.ylim([min(final_revenue_det,reference_revenue,final_revenue_probabilistic)-10000,max(reference_revenue,final_revenue_det,final_revenue_probabilistic)+100])
#plt.grid()
    plt.ylabel('Revenue [€]')
    plt.show()
    #plt.savefig('figures/comparison2_rev.png',bbox_inches = 'tight', dpi = 300)

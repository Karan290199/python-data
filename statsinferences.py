#Applying Annova
#Import the neccessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols

complete_Data = pd.read_csv('lok-sabha-candidate-details-2019.csv') #Load the csv file
complete_Data = pd.DataFrame(complete_Data) #Convert to Dataframe
complete_Data.drop(['NAME','SYMBOL','ASSETS','LIABILITIES','CATEGORY','GENERAL\nVOTES', 
'POSTAL\nVOTES','OVER TOTAL ELECTORS \nIN CONSTITUENCY','AGE',
'OVER TOTAL VOTES POLLED \nIN CONSTITUENCY'],axis = 1,inplace=True) #Remove unwanted features
#Preprocessing
#Replacing the Nan values
complete_Data['GENDER'] = complete_Data['GENDER'].replace(np.nan,'Unknown') 
complete_Data['CRIMINAL\nCASES'] = complete_Data['CRIMINAL\nCASES'].replace(np.nan,'0')
complete_Data['CRIMINAL\nCASES'] = complete_Data['CRIMINAL\nCASES'].replace(['Not Available'],0)
complete_Data['CRIMINAL\nCASES'] = pd.to_numeric(complete_Data['CRIMINAL\nCASES'])
complete_Data['EDUCATION'] = complete_Data['EDUCATION'].replace(np.nan,'UnKnown')
#Categorising the data
complete_Data['EDUCATION'] = complete_Data['EDUCATION'].replace(['Not Given','Not Available',
'Illiterate','12th Pass','10th Pass','8th Pass','5th Pass'],'Not Suitable')
complete_Data['EDUCATION'] = complete_Data['EDUCATION'].replace(['Post Graduate','Doctorate',
'Graduate','Others','Graduate Professional','Literate', 'Post Graduate\n'],'Suitable')
complete_Data['GENDER'] = pd.Categorical(complete_Data['GENDER']).codes

def conv(val):
    if(val>0):
        return 1
    return 0

complete_Data = complete_Data.rename(columns = {'CRIMINAL\nCASES':'CRIMINALCASES'})
complete_Data['CRIMINALCASES'] = complete_Data['CRIMINALCASES'].apply(conv)

x_1 = complete_Data.loc[complete_Data['PARTY']!='NOTA']['WINNER']
x_2 = complete_Data.loc[complete_Data['PARTY']!='NOTA']['CRIMINALCASES']
x_3 = complete_Data.loc[((complete_Data['PARTY']!='NOTA')&(complete_Data['GENDER']==0))]['WINNER']#0 represents women
x_4 = complete_Data.loc[((complete_Data['PARTY']!='NOTA')&(complete_Data['GENDER']==0))]['GENDER']
res = pd.concat([x_1, x_2],axis = 1)
res1 = pd.concat([x_3,x_4],axis = 1)
model = ols('WINNER~CRIMINALCASES',data = res).fit()
aov = sm.stats.anova_lm(model,type = 2)
print(aov)
model1 = ols('WINNER~GENDER',data = res1).fit()
aov1 = sm.stats.anova_lm(model1,type = 2)
print(aov1)
#Import the neccessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

uni = complete_Data.PARTY.unique() #Get unique parties
#Visualise the plots
x0 = []
y0 = []
for i in range(len(uni)):
    if i%2==0:
        x0.append(uni[i] + "  ")
    else:
        x0.append(uni[i])
    data = complete_Data[(complete_Data['PARTY']==uni[i])&(complete_Data['WINNER']==1)]
    k = data['WINNER'].sum(0)
    y0.append(k)
fig0 = plt.figure(1,figsize=(300,100))
ax0 = fig0.add_subplot(1,1,1)
ax0.bar(x0,y0)
ax0.set_xticklabels(x0, rotation = 90,horizontalalignment='right',fontsize = '8')
ax0.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
ax0.set_title('Winners of all the party')

x1 = ['M','F','Unknown']
y1 = []
datam = complete_Data[complete_Data.GENDER == 'MALE']
dataf = complete_Data[complete_Data.GENDER == 'FEMALE']
datan = complete_Data[complete_Data.GENDER == 'Unknown']
y1.append(len(datam))
y1.append(len(dataf))
y1.append(len(datan))
fig1 = plt.figure(2,figsize=(20,5))
ax1 = fig1.add_subplot(1,1,1)
ax1.pie(y1,labels = x1,autopct = "%0.0f%%",startangle = 45)
ax1.set_title('Gender Distribution')

x2 = []
y2 = []
for i in range(len(uni)):
    if i%2==0:
        x2.append(uni[i] + "  ")
    else:
        x2.append(uni[i])
    y2.append(complete_Data[complete_Data['PARTY']==uni[i]]['CRIMINAL\nCASES'].sum(0))
fig2 = plt.figure(3,figsize=(20,5))
ax2 = fig2.add_subplot(1,1,1)
ax2.bar(x2,y2)
ax2.set_xticklabels(x2, rotation = 90,horizontalalignment='right',fontsize = '8')
ax2.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
ax2.set_title('Criminal Cases against individual parties')

x3 = []
xc_0 = complete_Data[complete_Data['CRIMINAL\nCASES'] > 0]
xc_1 = complete_Data[complete_Data['CRIMINAL\nCASES'] == 0]
crime = len(xc_0)
ncrime = len(xc_1)
x3 = ['Criminal Case','Innocent']
y3 = []
y3.append((100*xc_0['WINNER'].sum(0))//crime)
y3.append((100*xc_1['WINNER'].sum(0))//ncrime)
fig3 = plt.figure(4,figsize=(20,5))
ax3 = fig3.add_subplot(1,1,1)
rects = ax3.bar(x3,y3,label = 'Criminal Case')
ax3.set_xticklabels(x3, rotation = 0,horizontalalignment='right',fontsize = '8')
ax3.set_title('Criminal Case against winning')
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax3.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')
autolabel(rects)

uni1 = complete_Data.STATE.unique()
x4 = []
y4 = []
for i in range(len(uni1)):
    if i%2==0:
        x4.append(uni1[i] + "  ")
    else:
        x4.append(uni1[i])
    y4.append(complete_Data[complete_Data['STATE']==uni1[i]]['CRIMINAL\nCASES'].sum(0))
fig4 = plt.figure(5,figsize=(20,5))
ax4 = fig4.add_subplot(1,1,1)
ax4.bar(x4,y4)
ax4.set_xticklabels(x4, rotation = 90,horizontalalignment='right',fontsize = '8')
ax4.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
ax4.set_title('Criminal Cases in every State')

uni2 = complete_Data.CONSTITUENCY.unique()
yt = []
ye = []
for i in range(len(uni2)):
    yt.append(complete_Data[complete_Data['CONSTITUENCY']==uni2[i]]['TOTAL\nVOTES'].sum(0))
    ye.append(complete_Data[complete_Data['CONSTITUENCY']==uni2[i]]['TOTAL ELECTORS'].max(0))
k = 0
h = 0
for i in yt:
    k+=i
for i in ye:
    h+=i
x5 = ['Voters','Not Voted']
y5 = [k,h-k]
fig5 = plt.figure(6,figsize=(20,5))
ax5 = fig5.add_subplot(1,1,1)
ax5.pie(y5,labels=x5, autopct = "%0.0f%%",startangle = 45)
ax5.set_title('Voting Distribution')

#Converting categorical variables to Numeric values
data = complete_Data
data['GENDER'] = pd.Categorical(data['GENDER']).codes
data['EDUCATION'] = pd.Categorical(data['EDUCATION']).codes
x6 = ['MALE','FEMALE','UNKNOWN']
y6 = []
data_m = complete_Data[complete_Data['GENDER']==1]
data_f = complete_Data[complete_Data['GENDER']==0]
data_n = complete_Data[complete_Data['GENDER']==2]
m = data_m['WINNER']
m = len(m)
f = data_f['WINNER']
f = len(f)
n = data_n['WINNER']
n = len(n)
m1 = data_m['WINNER'].sum(0)
f1 = data_f['WINNER'].sum(0)
n1 = data_n['WINNER'].sum(0)
y6.append(100*m1//m)
y6.append(100*f1//f)
y6.append(100*n1//n)
x7 = ['Educated with Degree','Educated with no Degree/UnEducated','UNKNOWN']
y7 = []
datae = complete_Data[complete_Data['EDUCATION']==0]
dataue = complete_Data[complete_Data['EDUCATION']==1]
dataun = complete_Data[complete_Data['EDUCATION']==2]
e_u = len(datae)
ue_u = len(dataue)
un_u = len(dataun)
y8 = []
y8.append(e_u)
y8.append(ue_u)
y8.append(un_u)
e = datae['WINNER']
e = len(e)
ue = dataue['WINNER']
ue = len(ue)
un = dataun['WINNER']
un = len(un)
e1 = datae['WINNER'].sum(0)
ue1 = dataue['WINNER'].sum(0)
un1 = dataun['WINNER'].sum(0)
y7.append(100*e1//e)
y7.append(100*ue1//ue)
y7.append(100*un1//un)

fig6 = plt.figure(7,figsize=(20,5))
ax6 = fig6.add_subplot(1,1,1)
rects1 = ax6.bar(x6,y6)
ax6.set_xticklabels(x6, rotation = 45,horizontalalignment='right',fontsize = '8')
ax6.set_title('Gender wise Win rate')
fig7 = plt.figure(8,figsize=(20,5))
ax7 = fig7.add_subplot(1,2,1)
ax8 = fig7.add_subplot(1,2,2)
rects2 = ax7.bar(x7,y7)
ax7.set_xticklabels(x7, rotation = 45,horizontalalignment='right',fontsize = '8')
ax7.set_title('Education wise Win rate')
def autolabel_1(rects):
    for rect in rects:
        height = rect.get_height()
        ax6.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')
autolabel_1(rects1)
def autolabel_2(rects):
    for rect in rects:
        height = rect.get_height()
        ax7.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')
autolabel_2(rects2)
ax8.pie(y8, labels = x7, autopct = '%0.0f%%', startangle = 45)
plt.show()

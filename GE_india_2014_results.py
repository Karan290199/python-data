#Import the neccessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data_2014 = pd.read_csv('GE_india_2014_results.csv') #Load the csv File
data_2014 = pd.DataFrame(data_2014) #Convert to Dataframe
data_2014.drop(['Rank','candidate_name'],axis = 1)#Remove unwanted columns
data_2014_unique = data_2014['PC'].unique() #Get the unique constituencies
#Preprocessing the dataset 
for i in data_2014_unique:
    data = data_2014[data_2014['PC'] == i]
    sorted_df = data.sort_values(by = ['total_votes'],ascending = False) #Sort the data
    sorted_df = sorted_df.sort_values(by = ['state/ut'],ascending = True)
    data_2014[data_2014['PC'] == i] = sorted_df    
data_2014_party_state = data_2014['state/ut'].unique() #Get unique states from the data

x1 = [] #Declare the x coordinates of the bar chart
y1 = [] #Declare the y coordinates of the bar chart of BJP
for i in data_2014_party_state:
    x1.append(i) #X coordinates are the states
    data = data_2014[data_2014['party'] == 'Bharatiya Janata Party']
    y1.append(data[data['state/ut'] == i]['total_votes'].sum(0)) #Y coordinates are the total votes recieved from that state
m = y1[0]
for i in range(len(y1)):
    m = max(m,y1[i])
print(m)
for i in range(len(y1)):
    if y1[i] == m:
        print(x1[i])
        break
print(sum(y1))
y2 = [] #Declare the y coordinates of the bar chart of INC
for i in data_2014_party_state:
    data = data_2014[data_2014['party'] == 'Indian National Congress']
    y2.append(data[data['state/ut'] == i]['total_votes'].sum(0)) #Y coordinates are the total votes recieved from that state

m1 = y2[0]
for i in range(len(y2)):
    m1 = max(m1,y2[i])
print(m1)
for i in range(len(y2)):
    if y2[i] == m1:
        print(x1[i])
        break
print(sum(y2))
#Visualise the plots
x = np.arange(len(x1))
fig = plt.figure(1,figsize=(20,5))
ax = fig.add_subplot(1,1,1)
w = 0.35
ax.bar(x-w/2,y1,w,color = 'b',label = 'BJP')
ax.bar(x+w/2,y2,w,color = 'r',label = 'INC')
ax.set_xticks(x)
ax.set_xticklabels(x1, rotation = 45,horizontalalignment='right',fontsize = '8')
ax.set_title('State wise Total votes secured by BJP and INC')
ax.legend()

plt.show()
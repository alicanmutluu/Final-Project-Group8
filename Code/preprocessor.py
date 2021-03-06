import pandas as pd
import numpy as np

from sklearn import  preprocessing as prepro

class preprocessing():
    def __init__(self):
        self.data_health = pd.read_csv('https://raw.githubusercontent.com/alicanmutluu/DMDatasets/main/2.12_Health_systems.csv',  sep = ',')
        self.data_clean = pd.read_csv('https://raw.githubusercontent.com/alicanmutluu/DMDatasets/main/cleanFuelAndTech.csv',  sep = ',')
        self.data_pollution = pd.read_csv('https://raw.githubusercontent.com/alicanmutluu/DMDatasets/main/death-rates-from-air-pollution.csv',  sep = ',')
        self.data_GDP=pd.read_csv('https://raw.githubusercontent.com/alicanmutluu/DMDatasets/main/Country_wise_GDP_from_1994_to_2017.csv', sep = ',')
        self.data_energy = pd.read_csv('https://raw.githubusercontent.com/alicanmutluu/DMDatasets/main/Percentage_of_Energy_Consumption_by_Country.csv',  sep = ',')
        self.set1 = {i for i in self.data_health['World_Bank_Name']}
        self.set2 = {i for i in self.data_clean['Location']}
        self.set3 = {i for i in self.data_pollution['Entity']}
        self.set4 = {i for i in self.data_GDP['Country']}
        self.set5 = {i for i in self.data_energy['Entity']}
        self.setf = self.set1.intersection(self.set2)
        self.setf = self.setf.intersection(self.set3)
        self.setf = self.setf.intersection(self.set4)
        self.setf = self.setf.intersection(self.set5)     
        self.setf2= self.set1.intersection(self.set2)
        self.setf2= self.setf2.intersection(self.set3)
        self.setf2= self.setf2.intersection(self.set4)

    def dfselection(self,s, df, v):
        ans = df.copy()
        for n, i in df.iterrows():
            if i[v] not in s:
                ans = ans.drop(n, axis=0)

        return ans
    def indoor2016(self):
        df1=self.dfselection(self.setf2,self.data_health,'World_Bank_Name')
        df2=self.dfselection(self.setf2,self.data_clean,'Location')
        df3=self.dfselection(self.setf2,self.data_pollution,'Entity')
        df4=self.dfselection(self.setf2,self.data_GDP,'Country')
        df2=df2[df2['Period']==2016]
        df3=df3[df3['Year']==2016]
        df4=df4[df4['Year']==2016]
        df1=df1.rename(columns={"World_Bank_Name": "Location"})
        df3=df3.rename(columns={'Entity':'Location'})
        df4=df4.rename(columns={'Country':'Location'})
        out=pd.merge(df1,df2,how='outer',on='Location')
        out=pd.merge(out,df3,how='outer',on="Location")
        out=pd.merge(out,df4,how='outer',on='Location')
        out=out.drop(columns='Province_State')
        
        return out

    def indoor(self):
        # merge df2 df3 df4 on location and year, on=outer do not drop na
        df2=self.dfselection(self.setf2,self.data_clean,'Location')
        df3=self.dfselection(self.setf2,self.data_pollution,'Entity')
        df4=self.dfselection(self.setf2,self.data_GDP,'Country')
        df2 = df2.rename(columns={"Period": "Year"})
        df3 = df3.rename(columns={'Entity': 'Location'})
        df4 = df4.rename(columns={'Country': 'Location'})
        out = pd.merge(df2, df3, how='outer', on=['Location','Year'])
        out = pd.merge(out, df4, how='outer', on=['Location','Year'])
        
        return out

    def outdoor(self):
        # merge df3 df4 df5, on location and year, on=outer do not drop na
        df3=self.dfselection(self.setf,self.data_pollution,'Entity')
        df4=self.dfselection(self.setf,self.data_GDP,'Country')
        df3 = df3.rename(columns={'Entity': 'Location'})
        df4 = df4.rename(columns={'Country': 'Location'})
        out = pd.merge(df3, df4, how='outer', on=['Location', 'Year'])
        return out

    def Merge_energy(self):
        df5 = self.dfselection(self.setf2, self.data_energy, 'Entity')
        df3 = self.dfselection(self.setf2, self.data_pollution, 'Entity')
        df4 = self.dfselection(self.setf2, self.data_GDP, 'Country')
        df3 = df3.rename(columns={'Entity': 'Location'})
        df4 = df4.rename(columns={'Country': 'Location'})
        df5 = df5.rename(columns={'Entity': 'Location'})
        out = pd.merge(df5, df3, how='outer', on=['Location', 'Year'])
        out = pd.merge(out, df4, how='outer', on=['Location', 'Year'])
        out = out.drop(columns='Wind Generation -TWh')
        out = out.drop(columns='Solar Generation - TWh')
        out = out.drop(columns='Nuclear Generation - TWh')
        out = out.drop(columns='Hydro Generation - TWh')
        out = out.drop(columns='Geo Biomass Other - TWh')
        out = out.drop(columns='Gas Consumption - EJ')


        return out

#prepare data for indoor2016 
pre=preprocessing()
indoor2016=pre.indoor2016()
print(indoor2016.columns)
print(indoor2016.shape)        
#prepare data for indoor
pre=preprocessing()
indoor=pre.indoor()
print(indoor.columns)
print(indoor.shape)
#prepare data for outdoor
pre=preprocessing()
outdoor=pre.outdoor()
print(outdoor.columns)
print(outdoor.shape)
#prepare data for Merge_energy
pre=preprocessing()
Merge_energy=pre.Merge_energy()
print(Merge_energy.columns)
print(Merge_energy.shape)

# Plotting
import matplotlib.pyplot as plt
# clean_fuel, coal, oil, indoor death rate, outdoor death rate, GDP
data_clean_p = pd.read_csv('https://raw.githubusercontent.com/alicanmutluu/DMDatasets/main/cleanFuelAndTech.csv',
                         sep=',')
dc2016 = data_clean_p[data_clean_p['Period'] == 2016]
num_bins = 50
n, bins, patches = plt.hist(dc2016['First Tooltip'], num_bins, facecolor='blue', alpha=0.5)
plt.xlabel('First Tooltip')
plt.ylabel('count')
plt.title('data_clean clean_fuel Year2016')
plt.show()

data_energy_p = pd.read_csv(
    'https://raw.githubusercontent.com/alicanmutluu/DMDatasets/main/Percentage_of_Energy_Consumption_by_Country.csv',
    sep=',')
de2016 = data_energy_p[data_energy_p['Year'] == 2016]
num_bins = 100
n, bins, patches = plt.hist(de2016['Coal Consumption - EJ'], num_bins, facecolor='blue', alpha=0.5)
plt.xlabel('Coal Consumption - EJ')
plt.ylabel('count')
plt.title('data_energy Coal Consumption Year2016')
plt.show()


num_bins = 100
n, bins, patches = plt.hist(de2016['Oil Consumption - EJ'], num_bins, facecolor='blue', alpha=0.5)
plt.xlabel('Oil Consumption - EJ')
plt.ylabel('count')
plt.title('data_energy Oil Consumption Year2016')
plt.show()

data_pollution_p = pd.read_csv(
    'https://raw.githubusercontent.com/alicanmutluu/DMDatasets/main/death-rates-from-air-pollution.csv', sep=',')
dp2016 = data_pollution_p[data_pollution_p['Year'] == 2016]
num_bins = 75
n, bins, patches = plt.hist(dp2016['Outdoor particulate matter (deaths per 100,000)'], num_bins, facecolor='blue', alpha=0.5)
plt.xlabel('Outdoor particulate matter (deaths per 100,000)')
plt.ylabel('count')
plt.title('data_pollution Outdoor pollution Year2016')
plt.show()

num_bins = 100
n, bins, patches = plt.hist(dp2016['Indoor air pollution (deaths per 100,000)'], num_bins, facecolor='blue', alpha=0.5)
plt.xlabel('Indoor air pollution (deaths per 100,000)')
plt.ylabel('count')
plt.title('data_pollution Indoor air pollution Year2016')
plt.show()

data_GDP_p = pd.read_csv(
    'https://raw.githubusercontent.com/alicanmutluu/DMDatasets/main/Country_wise_GDP_from_1994_to_2017.csv', sep=',')
dg2016 = data_GDP_p[data_GDP_p['Year'] == 2016]
num_bins = 75
n, bins, patches = plt.hist(dg2016['GDP per capita (in USD)'], num_bins, facecolor='blue', alpha=0.5)
plt.xlabel('GDP per capita (in USD)')
plt.ylabel('count')
plt.title('data_GDP GDP per capita Year2016')
plt.show()

import seaborn as sns; sns.set_theme()
le = prepro.LabelEncoder()
Merge_energy['Location'] =le.fit_transform(Merge_energy['Location'])
Merge_energy= Merge_energy.drop(columns='Code_x')
Merge_energy= Merge_energy.drop(columns='Code_y')

tc = Merge_energy.corr()
plt.figure(figsize=(16,20))
sns.heatmap(tc,cmap='coolwarm')
plt.show()
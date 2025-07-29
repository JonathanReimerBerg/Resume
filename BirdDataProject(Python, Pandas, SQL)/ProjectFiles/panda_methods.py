import pandas
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime


def cleanCSV():       #mostly just removing columns we don't need, and then writing to new CSV file 
    data = pandas.read_csv('ProjectFiles/MyEBirdData.csv')
    data.drop(columns = ['Scientific Name', 'Taxonomic Order', 'Distance Traveled (km)', 'Area Covered (ha)',
                     'Breeding Code', 'Observation Details', 'Checklist Comments', 'ML Catalog Numbers',
                     'Location ID', 'Latitude', 'Longitude', 'Time', 'Protocol', 'Duration (Min)',
                     'All Obs Reported', 'Number of Observers'], inplace = True)
    data.drop(data[data.County != 'Polk'].index, inplace = True)
    data.reset_index(drop = True, inplace = True)
    data.columns = [c.replace(' ', '_') for c in data.columns]
    data.to_csv('ProjectFiles/CSVs/CleanedData.csv', encoding = 'utf-8', index = False)
    return(data)

def removeOtherTaxa(data):  #remove all non countable taxa, coultn't get all of these in one line
    data = data[~data.Common_Name.str.contains(" x ")]  
    data = data[~data.Common_Name.str.contains(" sp.")]   
    data = data[~data.Common_Name.str.contains("/")]
    data = data[~data.Common_Name.str.contains("Domestic")]
    data['Common_Name'] = data['Common_Name'].str.replace(r'\s+\([^()]*\)$', '', regex=True) #remove stuff in parenthesis
    return(data)

def hotspotList():  #will return the name of each location birds have been reported from
    data = pandas.read_csv('ProjectFiles/CSVs/CleanedData.csv')
    hotspots = data['Location'].unique()
    hotspots.sort()
    return(hotspots)

def lifelist(printed = False):  #create a list of all birds seen in Polk, can print
    data = pandas.read_csv('ProjectFiles/CSVs/CleanedData.csv')     
    data = removeOtherTaxa(data)
    birdlist = data['Common_Name'].unique()  #we are left with one of each species in list form
    if printed:
        for i in birdlist:
            print(i)
        print('\n', len(birdlist), '\n')
    return(birdlist)

def scatterplot(species): #create a scatterplot of all the reports of a species by time of year and count
    data = pandas.read_csv('ProjectFiles/CSVs/CleanedData.csv')
    data.drop(data[data.Common_Name != species].index, inplace = True)  #remove everything but the target sp.

    data['Date'] = pandas.to_datetime(data['Date'])           
    data['Date'] = data['Date'].apply(lambda x: x.replace(year = 2024)) #make everything the same year (one with leap day)
    for i in data.index:
        if data.loc[i, "Count"] == 'X':    #need integer values only
            data.drop(i, inplace = True) 
    data['Count'] = data['Count'].apply(pandas.to_numeric) 
    
    plt.scatter(data['Date'], data['Count'])
    #plt.gcf().autofmt_xdate()      #different visual option
    
    date_format = mdates.DateFormatter('%b, %d')    #format the x-axis to show day/month instead of year
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.grid()

    fig = plt.gcf()   #formatting
    fig.set_size_inches(13, 7.5)
    plt.xlim([datetime.date(2024, 1, 1), datetime.date(2024, 12, 31)])    #make jan 1 with 0 count flush with the origin
    plt.ylim([0, data['Count'].max()*1.15])    #make a top margin
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.title(str(species) + ' in Polk county')

    plt.show()


def yearlist(year, last = False):   #print a list of species for a given year, can sort by first seen or last
    data = pandas.read_csv('ProjectFiles/CSVs/CleanedData.csv')
    data = removeOtherTaxa(data)
    data = data[data.Date.str.contains(str(year))]  #include only species in given year

    data = data.sort_values('Date')
    if last:            #removing duplicates keeps the first occurence, so by flipping we can get the latest seen date instead
        data = data.reindex(index=data.index[::-1])
    data = data.drop_duplicates('Common_Name', keep='first')  #after sorting, keep the first occurence of each species

    firsts = [data['Common_Name'].values.tolist(), data['Date'].values.tolist(), data['Location'].values.tolist()]  #get all the data we want into a list to easily print  
    print('')
    for i in range(0, len(firsts[0])):
        print(i + 1, ' '*(3 - len(str(i + 1))), firsts[0][i], ' '*(30 - len(firsts[0][i])), firsts[1][i], firsts[2][i][:60])
    print('')
    return




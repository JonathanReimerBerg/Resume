import sqlite3

def runCommand(command, fetchone = False, fetchall = False):
    connection = sqlite3.connect("PolkDatabase.db")
    crsr = connection.cursor()
    try:
        crsr.execute(command)
    except:
        print(command)
    result = crsr.fetchall()
    connection.commit()
    connection.close
    return(result)

def speciesData(species):  #print each occurence of a species, accompanies the scatterplot  
    dates = []
    
    command = "select Month, Day, Year, Hotspot, Count from CHECKLISTS RIGHT JOIN [" + species + "] on CHECKLISTS.ID = ["
    command += species + "].Checklist;"
    dates = runCommand(command)

    print('\n')
    dates =  sorted(dates, key=lambda tup: (tup[0], tup[1])) #sort by date
    for i in dates:
        print(i[0], i[1], i[2], i[3], i[4])

def checkHotspotBird(species, hotspot): #check if a given species has been seen at a given hotspot
    command = "select Month, Day, Year from CHECKLISTS RIGHT JOIN [" + species
    command += "] on CHECKLISTS.ID = [" + species + "].Checklist WHERE Hotspot = '"
    command += hotspot + "' Order By CHECKLISTS.YEAR, CHECKLISTS.MONTH, CHECKLISTS.DAY  Limit 1"
    return(runCommand(command)) #returns earliest date if seen, otherwise returns nothing 

def hotspotList(birdlist, hotspot): #get a species list for a  given hotspot
    fullList = []
    for i in range(0, len(birdlist)):
        earliestDate = checkHotspotBird(birdlist[i], hotspot)
        if earliestDate:  #if the species has been seen there, store it and the first occurence (which was returned)
            fullList.append([birdlist[i], earliestDate])
    fullList = sorted(fullList, key=lambda element: (element[1][0][2], element[1][0][0], element[1][0][1])) #sort by date

    count = 1 
    for i in fullList:
        print(count, ' '*(5-len(str(count))), i[0], ' '*(30 - len(i[0])), i[1][0])
        count += 1
    print('\n', len(fullList), 'species \n')
    return(fullList)





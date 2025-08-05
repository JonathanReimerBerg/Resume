import ProjectFiles.sql_methods as sm
import ProjectFiles.panda_methods as pm
import ProjectFiles.DB_writer as dw
import os

all_Possible_Locations = ['Oregon', 'Polk', 'Marion', 'Yamhill', 'Benton', 'Linn', 'Lane', 'Clackamas', 'Washington', 'Columbia', 'Multnomah',
                    'Clatsop', 'Tillamook', 'Lincoln', 'Douglas', 'Coos', 'Curry', 'Jackson', 'Josaphine', 'Hood River', 'Wasco', 'Sherman',
                    'Gilliam', 'Morrow', 'Umatilla', 'Union', 'Baker', 'Malheur', 'Wallawa', 'Grant', 'Wheeler', 'Deschutes', 'Klamath', 
                    'Lake', 'Harney', 'Crook', 'Jefferson']    #this is a static list of all compatable locations this database is compatible for


def selectHotspot(hotspots):  #attempts to autofill a given location
    hotspot = input("Enter hotspot name (enough chars to identify, spelling must be exact):\n")
    for spot in hotspots:
        if hotspot in spot and len(hotspot) > 4: #need to address locations with similar names
            print(spot, 'found')
            return(spot)
    spot= None
    if input("loc not found, press 't' to try again: ") == 't':
        spot = selectHotspot(hotspots)  #recursive function, above line insures no return if loc not found, needs to be before function call
    return(spot)

def setupLoc(loc, new = False):
    if new:
        os.mkdir('ProjectFiles/DBs')
        os.mkdir('ProjectFiles/CSVs')
    dw.initializeDB(loc)
    pm.cleanCSV(loc)
    return

def pickLoc():
    while True:
        loc = input('Choose a county (or the whole state): ')
        if loc not in all_Possible_Locations:
            print(str(loc), "not found")
        else:
            break
    return(loc)

def main():
    if not os.path.isfile('ProjectFiles/DBs/OregonDatabase.db'):
        setupLoc('Oregon', True)
    while True:   #option menu, trying to keep simple functionality
        inp = input('''\nu: update data \np: print life list \ns: species summary \ny: print year list \nh: hotspot list \nc: high counts \nq: quit \n''')
        if inp == 'u':
            doAll = input("Press '1' to update/add all Oregon regions (this may take a while): ")
            if doAll == '1':
                loc = all_Possible_Locations
            else:
                loc = [pickLoc()]
            for i in loc:
                if not os.path.isfile('ProjectFiles/DBs/' + i + 'Database.db'):
                    setupLoc(i)
                dw.updateDB(i)
        elif inp == 'p':
           pm.lifelist(pickLoc(), True)
        elif inp == 's':
            loc = pickLoc()
            while True:
                species = input("Species: ")
                if species in pm.lifelist(loc):
                    sm.speciesData(species, loc)
                    pm.scatterplot(species, loc)
                    break
                else:
                    print('\n', species, 'not found')
        elif inp == 'y':
            loc = pickLoc()
            year = input("Enter a year: ")
            seen = input("Would you like to see first seen (f) or last (l): ")
            pm.yearlist(year, loc, seen == 'l')
        elif inp == 'h':
            loc = pickLoc()
            hotspots = pm.hotspotList(loc)
            for i in hotspots:
                print(i)
            hotspot = selectHotspot(hotspots)
            if hotspot:
                sm.hotspotList(pm.lifelist(loc), hotspot, loc) 
        elif inp == 'c':
            loc = pickLoc()
            year = input("Enter a year: ")
            sm.highCounts(pm.lifelist(loc), year, loc)
        elif inp == 'q':
            break


main()

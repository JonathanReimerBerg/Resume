import ProjectFiles.sql_methods as sm
import ProjectFiles.panda_methods as pm
import ProjectFiles.DB_writer as dw
import os


def inputLoc(hotspots):  #attempts to autofill a given location
    hotspot = input("Enter hotspot name (enough chars to identify, spelling must be exact):\n")
    for spot in hotspots:
        if hotspot in spot and len(hotspot) > 4: #need to address locations with similar names
            print(spot, 'found')
            return(spot)
    spot= None
    if input("loc not found, press 't' to try again: ") == 't':
        spot = inputLoc(hotspots)  #recursive function, above line insures no return if loc not found, needs to be before function call
    return(spot)

def setup(Loc = None):
    os.mkdir('ProjectFiles/DBs')
    os.mkdir('ProjectFiles/CSVs')
    dw.initializeDB()
    pm.cleanCSV()
    return

def main():
    if not os.path.isfile('ProjectFiles/DBs/PolkDatabase.db'):
        setup()
    while True:   #option menu, trying to keep simple functionality
        inp = input('''\nu: update data \np: print life list \ns: species summary \ny: print year list \nh: hotspot list \nc: high counts \nq: quit \n''')
        if inp == 'u':
            dw.updateDB()
        elif inp == 'p':
           pm.lifelist(True)
        elif inp == 's':
            species = input("Species: ")
            if species in pm.lifelist():
                sm.speciesData(species)
                pm.scatterplot(species)
            else:
                print('\n', species, 'not found')
        elif inp == 'y':
            year = input("Enter a year: ")
            seen = input("Would you like to see first seen (f) or last (l): ")
            pm.yearlist(year, seen == 'l')
        elif inp == 'h':
            hotspots = pm.hotspotList()
            for i in hotspots:
                print(i)
            hotspot = inputLoc(hotspots)
            if hotspot:
                sm.hotspotList(pm.lifelist(), hotspot) 
        elif inp == 'c':
            year = input("Enter a year: ")
            sm.highCounts(pm.lifelist(), year)
        elif inp == 'q':
            break


main()

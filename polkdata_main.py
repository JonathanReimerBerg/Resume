import sql_methods as sm
import panda_methods as pm


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


def main():
    while True:   #option menu, trying to keep simple functionality
        inp = input('''p: print life list \ns: species summary \ny: print year list \nh: hotspot list \nq: quit \n''')
        if inp == 'p':
           pm.lifelist(True)
        elif inp == 's':
            species = input("Species: ")
            sm.speciesData(species)
            pm.scatterplot(species)
        elif inp == 'y':
            year = input("Enter a year: ")
            seen = input("Would you like to see first seen (f) or last (l): ")
            pm.yearlist(year, seen == 'l')
        elif inp == 'h':
            birdlist = pm.lifelist() #could add this stuff to inputLoc but it is also used again later
            hotspots = pm.hotspotList()
            print(hotspots)
            hotspot = inputLoc(hotspots)
            sm.hotspotList(birdlist, hotspot)     
        elif inp == 'q':
            break


main()

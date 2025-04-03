#File used to create a DB from a downloaded CSV file from eBird.
#To update, just delete the DB and this will create a new one, I could implement
#a feature in the future to update the DB from an newer CSV file. 

import csv
import sqlite3
import re

def runCommand(command, fetchone = False, fetchall = False):
    connection = sqlite3.connect("PolkDatabase.db")
    crsr = connection.cursor()
    try:
        crsr.execute(command)
    except:         
        print(command)      #print the command if it doesn't work, usually a formatting issue
    connection.commit()
    connection.close

runCommand("DROP TABLE IF exists CHECKLISTS;")

command = """CREATE TABLE CHECKLISTS ( 
    ID varchar(64),
    Hotspot varchar(64),
    Time varchar(16),
    Month INTEGER varchar(2),
    Day INTEGER varchar(2),
    Year INTEGER varchar(4),
    Observers Integer varchar(2),
    UNIQUE(ID),
    CONSTRAINT CHECKLISTS_PK
    );"""

runCommand(command)   #create a table to store each checklists using its given ebird identifier
birds = []  # a table for each species, using list to check dups
lists = []  #checklists can show up multiple times in the data, so we should check dups

with open('MyEBirdData.csv', 'r', encoding='utf') as file:
    reader = csv.reader(file)
    for row in reader:
        if row[6] == 'Polk':    #database only being set up for Polk Co.
            if row[0] not in lists:   #check if we arleady entered the checklist in 'checklists' table
                values = '"'+row[0]+'","'+row[8]+'","'+row[12]+'''
                    ",'''+row[11][5:7]+','+row[11][8:10]+','+row[11][0:4]+','+row[18] 
                command = '''INSERT INTO CHECKLISTS (ID, Hotspot, Time, Month, Day, Year, Observers)
                    VALUES (''' + values + ''');'''
                runCommand(command)
                lists.append(row[0])

            if '(' in row[1]:      #basically removes sub-taxa
                row[1] = re.sub(r"\((.*?)\)", "", row[1])[:-1]
            
            if row[1] not in birds:  #if we don't have a table for that bird yet
                command = ("CREATE TABLE if not exists '" + str(row[1].replace("'","''")) + "'" + '''(
                    Checklist varchar(10),
                    Count INTEGER varchar(5));''')
                runCommand(command)
                birds.append(row[1])
                print(row[1], ' added')

            if row[4] == 'X':   #integers only, defaulting to 1 bird seen
                row[4] = str(1)

            command = ("INSERT INTO '" + str(row[1].replace("'","''")) + "'(Checklist, Count) VALUES" + '''
                ("''' + str(row[0]) + '", ' + row[4] + ');')
            runCommand(command)   #adds the report to the species table
            
    print('done')
            

#The following code fragment can create a table for each checklist, which is much less efficient
    
#command = ('CREATE TABLE if not exists ' + str(row[0]) + '''(Species varchar(64),
#                Count INTEGER varchar(5), CONSTRAINT ''' + str(row[0]) + '_PK);')
#            runCommand(command)

#            if row[4] == 'X':
#                row[4] = str(1)

#            command = ('INSERT INTO ' + str(row[0]) + '''(Species, Count) VALUES
#                ("''' + str(row[1]) + '", ' + row[4] + ');')
#            runCommand(command)

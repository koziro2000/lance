# coding: utf-8

"""
This module processes time entries to db.
"""
import os
import sqlite3
import pandas as pd

def list_all_files_in_current_directory():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        print(f)

importFileName = 'time sample.xlsx'
dbFileName = 'lanceCostAcct.xlsx'

def processFile(fname):
    times = pd.read_excel(fname, index_col=None, header=None)
    times = times.iloc[2:24, 2:11]
    times = times.fillna(0)
    times = times.drop(columns=[3, 10])
    return times

currentTimes = processFile(importFileName)

def processFirstWeek(currentTimeEntries):
    firstWeekEntries = currentTimeEntries.iloc[0:9, 0:11]
    firstWeekEntries.columns = firstWeek.iloc[0]
    firstWeekEntries = firstWeekEntries.iloc[1:8]
    firstWeekEntries.rename(columns={0:'Date'}, inplace=True)
    firstWeekEntries['Date'] = firstWeekEntries['Date'].astype(str)
    firstWeekEntries = firstWeek.applymap(str)
    return firstWeekEntries

def processSecondWeek(currentTimeEntries):
    secondWeekEntries = currentTimeEntries.iloc[11:21, 0:11]
    secondWeekEntries.columns = secondWeekEntries.iloc[0]
    secondWeekEntries = secondWeekEntries.iloc[1:8]
    secondWeekEntries.rename(columns={0:'Date'}, inplace=True)
    secondWeekEntries['Date'] = secondWeekEntries['Date'].astype(str)
    secondWeekEntries = secondWeekEntries.applymap(str)
    return secondWeekEntries

list_all_files_in_current_directory()

firstWeek = processFirstWeek(currentTimes)
secondWeek = processSecondWeek(currentTimes)


#Task 3: Produce Weekly report on projects
#3.1 DB!

contractorName = 'John Doe'

conn = sqlite3.connect(dbFileName)
c = conn.cursor()

#3.2 Create Table - Project (Project Name: Description)
c.execute('''Create table if not exists projects(ProjName text, ProjDesc text)''')
c.execute('''Create Table if not exists timeEntries(ContName text, ProjName text, Date text, Hour text)''')

c.execute("Delete from projects")
c.execute("Delete from timeEntries")

conn.commit()
conn.close()

conn = sqlite3.connect(dbFileName)
c = conn.cursor()

c.execute("INSERT INTO projects values ('CBC', 'Canada Broadcasting Service')")
for index, row in firstWeek.iterrows():
    for i in range(1, row.size-1):
        c.execute("REPLACE INTO timeEntries(ContName, ProjName ,Date ,Hour) values(?, ?, ?, ?)", (contractorName, row.index[i], row[0], row[i]))


for index, row in secondWeek.iterrows():
    for i in range(1, row.size-1):
        c.execute("REPLACE INTO timeEntries(ContName, ProjName,Date  ,Hour) values(?, ?, ?, ?)", (contractorName, row.index[i], row[0], row[i]))
    
conn.commit()
conn.close()


conn = sqlite3.connect(dbFileName)
c = conn.cursor()

for row in c.execute('SELECT rowid, * FROM projects ORDER BY ProjName'):
    print(row)

conn.close()


conn = sqlite3.connect(dbFileName)
c = conn.cursor()

for row in c.execute('SELECT rowid, ContName, Date, ProjName, Hour from timeentries order by date asc'):
    print(row)

for row in c.execute('SELECT ContName, ProjName, sum(Hour) from timeentries group by ContName, ProjName'):
    print(row)
    
conn.close()

invoices = pd.read_excel('invoice sample.xlsx')
invoices.head(3)


import sys
import pandas as pd
from flask import Flask
from flask_mail import Mail
from flask_mail import Message
from datetime import datetime

def emailAlert(dfile):
    pass

def expirationCheck(dfile):
    # Format date
    dfile['Cert End Date'] = pd.to_datetime(dfile['Cert End Date'].astype(str), errors='coerce')
    
    # Fill in NaN values
    dfile.fillna(datetime.now())
    
    # Compare authorization to expiration date
    today = datetime.now()
    print("Today: ",today)
    for row in range(119):
        dateList = dfile.at[dfile.index[row],'Cert End Date']
        for date in dateList:
            print(date)
            if (date-today).days >= 14:
               print("Removed")

    print("After sql statement")
    # Call email fnc on expiring auth
    emailAlert(dfile)

class Update:
    def __init__(self, fname, lname, code, auth):
        self.fname = fname
        self.lname = lname
        self.code = code
        self.auth = auth

    def operation():
        df = pd.read_excel(sys.argv[1],index_col=0)
        expirationCheck(df)
        
    operation()

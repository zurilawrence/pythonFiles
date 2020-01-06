import sys
import pandas as pd
from flask import Flask
from flask_mail import Mail
from flask_mail import Message
from datetime import datetime

class Update:
    def __init__(self, fname, lname, code, auth):
        self.fname = fname
        self.lname = lname
        self.code = code
        self.auth = auth
     
    def expirationCheck(dfile):
        # Format date
        dfile = pd.to_datetime(df.Cert_End_Date)
        dfile['Cert_End_Date'] = dfile['Cert_End_Date'].dfile.strftime('%Y,%m,%d')

        # Compare authorization to expiration date
        today = datetime.now()
        dfile[((dfile['Cert_End_Date'] - today).days <= 14)]

        # Call email fnc on expiring auth
        # emailAlert(dfile)
        print(df)

    def operation():
        df = pd.read_excel(sys.argv[1],index_col=0)
        expirationCheck(df)

    operation()

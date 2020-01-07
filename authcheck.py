import sys
import pandas as pd
from flask import Flask
from flask_mail import Mail
from flask_mail import Message
from datetime import datetime

def emailAlert(dfile):
    pass

def expirationCheck(dfile):
    dfile.drop(['ID'],axis=0)
    dfile.columns = ["LastName","FirstName","HomePhone","Address","City","State","PostalCode","StartOfCare","CertEndDate","Ins","DOB","MedRecordNo","Hours","ServiceCodes","Diagnosis","AuthNumber","Billed","Profit","","","","","","",""]
    # Format date
    dfile = pd.to_datetime(dfile['CertEndDate'])
    # dfile['CertEndDate'] = dfile['CertEndDate'].strftime('%Y,%m,%d')

    # Compare authorization to expiration date
    # today = datetime.now()
    # dfile[((dfile['CertEndDate'] - today).days <= 14)]

    # Call email fnc on expiring auth
    emailAlert(dfile)
    print(dfile.index[0])

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

#  Created by Zuri Lawrence on 12/31/19.
#  Copyright © 2019 Zuri Lawrence. All rights reserved.

import sys
import pandas as pd
from datetime import date
from flask import Flask
from flask_mail import Mail
from flask_mail import Message
from datetime import datetime

def emailAlert(dfile):
    pass

def expirationCheck(dfile):


    #Add index
    newIndex = list(range(len(dfile.index)))
    dfile['Index'] = newIndex
    dfile.set_index('Index',inplace=True)

    # Fill in NaN values
    dfile.fillna(date.today())

    # Format date
    dfile.rename(columns={"Cert End Date":"CertEndDate"},inplace=True)
    print(dfile['CertEndDate'])
    dfile['CertEndDate'] = pd.to_datetime(dfile.CertEndDate)
    # dfile['Start Date'] = rep['Start Date'].dt.strftime('%m/%d/%Y')

    # Compare authorization to expiration date
    today = datetime.now()
    newIndex = list(range(119))
    dfile.rename(index=newIndex,inplace=True)

    for row in range(119):
        dateList = dfile.at[dfile.index[row],'Cert End Date']
        print("Line: ",dateList)
        # for date in dateList:
            # print(date)
            # if (date-today).days >= 14:
              #  print("Removed")

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
        df = pd.read_csv(sys.argv[1],index_col=0)
        expirationCheck(df)

    operation()

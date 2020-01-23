#  Created by Zuri Lawrence on 12/31/19.
#  Copyright © 2019 Zuri Lawrence. All rights reserved.

import pandas as pd
from datetime import date
import sys
import formatSonetoPayments as FSP
from decimal import Decimal
from flask import Flask
from flask_mail import Mail
from flask_mail import Message

def emailResults():
    mail = Mail()
    app = Flask(__name__)
    mail.init_app(app)

    with open("resultMessage.txt") as f:
        message = f.read()

    with open("resultMessage.txt","a") as f:
        f.write(date.today().strftime('%m/%d/%Y') + ".")
            
    with open("recipients.txt") as f:
        msg = Message(recipients=f.readline(),
                sender=f.readline(),
                body=message,
                subject="Billing reconciliation")

    # Attach csv of errors
    with app.open_resource("billingAlerts.csv") as fp:
        msg.attach("billingAlerts.csv","billingAlerts/csv",fp.read())

    # Send mail
    with mail.connect() as conn:
        conn.send(msg)


def selectMissedPayments(rep):
    # Missing payments in report record are sent to be emailed
    finalReport = rep[rep['Difference'] != 0]
    rep.to_csv("billingAlerts.csv")

    emailResults()

def authorizePayments(pay,rep):
    # Format reports columns to datetime object
    rep.rename(columns={"Start Date":"StartDate"},inplace=True)
    rep['Start Date'] = pd.to_datetime(rep.StartDate)
    rep['Start Date'] = rep['Start Date'].dt.strftime('%m/%d/%Y')

    # For every row in report SELECT column from payment record
    for idx in range(len(rep.index)-1):
        client = rep.loc[idx, 'Client']
        startDate = rep.loc[idx, 'Start Date']
        serviceCode = rep.loc[idx, 'Service']

        # Set sql query selection
        query = pay[(pay['Client']==client) & (pay['ServiceDate']==startDate) & (pay['ServiceCodeName']==serviceCode)]

        # UPDATE if a row is selected
        if next(iter(query.index), 'no match') != 'no match':
            dfb = next(iter(query.index), 'no match') # set index

            rep.loc[idx, 'DateBilled'] = pay.loc[dfb, 'PostingDate'] # date billed
            rep.loc[idx, '$ Paid'] = pay.loc[dfb, 'AmountPaid'] # amount paid
            rep.loc[idx, 'Check #'] = pay.loc[dfb, 'PaymentNo'] # check number
            rep.loc[idx, 'Difference'] = Decimal(rep.loc[idx, '$ Paid']) - Decimal(rep.loc[idx, 'Billed']) # difference

    print(rep)
    selectMissedPayments(rep)

formattedFile = FSP.formatPayments(pd.read_csv(sys.argv[1]))
reportToSend = pd.read_csv(sys.argv[2])

authorizePayments(formattedFile,reportToSend)

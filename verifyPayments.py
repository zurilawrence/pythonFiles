#  Created by Zuri Lawrence on 12/31/19.
#  Copyright © 2019 Zuri Lawrence. All rights reserved.

import pandas as pd
import sys
import formatSonetoPayments as FSP
from flask import Flask
from flask_mail import Mail
from flask_mail import Message

def emailResults():
    mail = Mail()
    app = Flask(__name__)
    mail.init_app(app)

    f = open("resultMessage.txt", "r")
    message = f.read()
    f.write(datetime.today().date + ".")
    f.close()

    with open("recipients.txt") as f:
        msg = Message(recipients=f.readline(),
                sender=f.readline(),
                body=message,
                subject="Billing reconciliation")

    # Attach csv of errors
    with app.open_resource("billingAlerts.csv") as fp:
        msg.attach("billingAlerts.csv","billingAlerts/csv",fp.read())

    # Send mail
    mail.msg(msg)

def selectMissedPayments(rep):
    # Missing payments in report record are sent to be emailed
    pass

def authorizePayments(pay,rep):
    # Format reports columns to datetime object
    rep.rename(columns={"Start Date":"StartDate"},inplace=True)
    rep['Start Date'] = pd.to_datetime(rep.StartDate)
    rep['Start Date'] = rep['Start Date'].dt.strftime('%m/%d/%Y')

    length = len(pay.index)-1
    # For every row in report SELECT column from payment record
    for idx in range(length):
        client = rep.loc[idx, 'Client']
        startDate = rep.loc[idx, 'Start Date']
        serviceCode = rep.loc[idx, 'Service']

        # Set sql query selection
        query = pay[(pay['Client']==client) & (pay['ServiceDate']==startDate) & (pay['ServiceCodeName']==serviceCode)]

        # UPDATE if a row is selected
        if next(iter(query.index), 'no match') != 'no match':
            dfb = next(iter(query.index), 'no match') # set index
            print()
            #print(f'This is the index: {dfb}')
            #print(pay[(pay['Client']==client) & (pay['ServiceDate']==startDate) & (pay['ServiceCodeName']==serviceCode)])

            rep.loc[idx, 'DateBilled'] = pay.loc[dfb, 'PostingDate'] # date billed
            """
            # Amount Paid
            rep.loc[idx, '$ Paid'] = pay[(pay['Client']==client) & (pay['ServiceDate']==startDate) & (pay['ServiceCodeName']==serviceCode), ['AmountPaid']]
            # Check Number
            rep.loc[idx, 'DateBilled'] = pay[(pay['Client']==client) & (pay['ServiceDate']==startDate) & (pay['ServiceCodeName']==serviceCode), ['PaymentNo']]
            """
        else:
            pass

formattedFile = FSP.formatPayments(pd.read_csv(sys.argv[1]))
reportToSend = pd.read_csv(sys.argv[2])

authorizePayments(formattedFile,reportToSend)

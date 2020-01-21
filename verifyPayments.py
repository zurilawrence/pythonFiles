#  Created by Zuri Lawrence on 12/31/19.
#  Copyright © 2019 Zuri Lawrence. All rights reserved.

import pandas as pd
import sys
import formatSonetoPayments as FSP
from flask import Flask
from flask_mail import Mail
from flask_mail import Message

def emailResults():
    # TODO: Edit recipients list
    mail = Mail()
    app = Flask(__name__)
    mail.init_app(app)

    @app.route("/")
    f = open("resultMessage.txt", "r")
    message = f.read()
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

def authorizePayments(pay,rep): # using UPDATE
    # Date Billed
    rep.loc[rep['Client']==pay.['Client'] & rep['StartDate']==pay['ServiceDate'] & rep['Service']==pay['Service'],'DateBilled'] = pay['PostingDate']

    # Amount Paid
    rep.loc[rep['Client']==pay['Client'] & rep['StartDate']==pay['ServiceDate'] & rep['Service']==pay['Service'], '$ Paid'] = pay['AmountPaid']

    # Check number
    rep.loc[rep['Client']==pay['Client'] & rep['StartDate']==pay['ServiceDate'] & rep['Service']==pay['Service'], 'Check #'] = pay['PaymentNo']

# TODO: Call formatSonetoPayments for proper file
payments = pd.read_tocsv(sys.argv[1])
oldReports = pd.read_tocsv(sys.argv[2])
# TODO: For loop to account for row
authorizePayments(payments,reports)

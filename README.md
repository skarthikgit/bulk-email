# bulk-email

sendmail.py reads lists of emails from email-list.csv and send email with personalized name with an attachment. email_template.html has the content.

The sendmail.py script reads a list of emails from email-list.csv and sends personalized emails to each recipient. The content of the emails is defined in email_template.html.

Example email-list.csv
post2sk@gmail.com,M Sunrise

# Set necessary env varialble

EMAIL_ATTACHMENT: File to be attached

EMAIL_USERNAME: email ID

EMAIL_APP_PASSWORD: It's NOT plain password
Follow the steps [here](https://support.google.com/accounts/answer/185833?visit_id=638631829327093147-1159351658&p=InvalidSecondFactor&rd=1) to get the App Password
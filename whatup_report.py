import ConfigParser
import datetime
import requests
import smtplib
import sys

from json import dumps
from email.mime.text import MIMEText
from os.path import expanduser

# Get config
#toaddr = ['theownage@gmail.com']
toaddr = ['project-whatup@googlegroups.com', 'jks29@drexel.edu']
base_address = 'http://projectwhatup.us:5000/api/posts'
base_view_address = 'http://arena.projectwhatup.us/#/posts/view/'

config = ConfigParser.RawConfigParser(allow_no_value=True)
config_file = expanduser('~/.checksite.cfg')
config.read(config_file)
try:
    mail_server = config.get('Required', 'mail_server')
    mail_port = config.get('Required', 'mail_port')
    fromaddr = config.get('Required', 'from_addr')
    password = config.get('Required', 'password')
    post_id = config.get('Required', 'post_id')

except ConfigParser.NoOptionError, error:
    print error
    sys.exit(4)

# Get Current post
headers = {'content-type': 'application/json'}
current_post_url = '{0}/{1}'.format(base_address, post_id)
resp = requests.get(current_post_url, headers=headers)
post_text = resp.json()['body']

current_post_view_url = '{0}{1}'.format(base_view_address, post_id)
link_text = 'Link to the report (with markdown rendered) on WhatUp: {0}'.format(
    current_post_view_url)
auto_notice = 'This email was automatically generated using the WhatUp API.\n' \
        'Please email project-whatup@googlegroups.com with any problems'
body = '{0}\n\n{1}\n\n{2}'.format(link_text, post_text, auto_notice)

# Send email
mailserv = smtplib.SMTP(mail_server, mail_port)
msg = MIMEText(body)
msg['Subject'] = "Senior Design: Project WhatUp Weekly Report"
msg['From'] = fromaddr
msg['To'] = ', '.join(toaddr)
mailserv.ehlo('x')
mailserv.starttls()
mailserv.ehlo('x')
mailserv.login(fromaddr, password)
mailserv.sendmail('jdb356@drexel.edu', toaddr, msg.as_string())
mailserv.quit()

# Create new post
tomorrow = datetime.date.today() + datetime.timedelta(days=1)
tomrrow = tomorrow.strftime('%B %d %Y')
new_post_topic = 'Status Report for week of {0}'.format(tomorrow)
names = ['Noah Black', 'John Brodie', 'Lakshit Dhanda', 'Anthony Hurst',
         'Damali Martin', 'Ayush Sobti']
new_post_body = ''
for name in names:
    new_post_body = '{0}\n\n**{1}**:'.format(new_post_body, name)
new_post = {'user_id': 10, 'topic': new_post_topic, 'body': new_post_body}
resp = requests.post(base_address, headers=headers, data=dumps(new_post))
new_post_id = resp.json()['id']
config.set('Required', 'post_id', new_post_id)
with open('/home/ogmios/.checksite.cfg', 'wb') as configfile:
    config.write(configfile)

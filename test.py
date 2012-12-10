import csv
import collections 

#email_counter = collections.Counter()

data = 'trilogy_base.csv'
f=open(data,'rU')

def get_data():
    read_data=csv.DictReader(f,fieldnames=None)
    raw_leads = list(read_data)
    return raw_leads


def find_duplicate_emails(raw_leads):
    emails = {}
    for row in raw_leads:
        if row['Email'] in emails:
            emails[row['Email']] += 1
        else:
            emails[row['Email']] = 1
    return emails
    
def update_status(raw_leads,emails):
    duplicate_emails = []
    for key, value in emails.iteritems():
        if value > 1:
            duplicate_emails.append([key, value])
    print len(duplicate_emails),    
    return duplicate_emails, len(duplicate_emails)

def main():
    raw_leads = get_data()
    emails = find_duplicate_emails(raw_leads)
    update_status(raw_leads,emails)

if __name__ == "__main__":

    main()
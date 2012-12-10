import csv
import collections 

#email_counter = collections.Counter()

data = 'trilogy_base.csv'
f=open(data,'rU')

def get_data():
    read_data=csv.DictReader(f,fieldnames=None)
    raw_leads = list(read_data)
    print len(raw_leads), "leads"
    return raw_leads


def get_unique_emails(raw_leads):
    emails = {}
    for row in raw_leads:
        if row['Email'] in emails:
            emails[row['Email']] += 1
        else:
            emails[row['Email']] = 1
    print len(emails), "unique email addresses within", sum(emails.itervalues()), "leads"
    return emails
    
def find_duplicate_emails(raw_leads,emails):
    duplicate_emails = []
    for key, value in emails.iteritems():   
        if value > 1:
            duplicate_emails.append([key, value])
    print len(duplicate_emails), "emails are duplicates"
    return duplicate_emails

def raw_duplicate_count(duplicate_emails):
    list_count = 0
    for list in duplicate_emails:
        list_count += list[1]
    print "Duplicate emails appear", float(list_count)/len(duplicate_emails), "times, on average"
    return list_count


def assign_status_to_lead(raw_leads,emails):
    garbage_lead = 0
    duplicate_lead = 0
    good_lead = 0 
    r_length = len(raw_leads)
    for i in range(r_length):
        if raw_leads[i]['Email'] == '':
            raw_leads[i]['Email'] = 'No Email Provided'
            raw_leads[i]['Status'] = 'Garbage Lead'
            garbage_lead += 1
            break 
        #         raw_leads[i]['Status'] = 'Duplicate Lead'
        #         duplicate_lead += 1
        # else:
        #     raw_leads[i]['Status'] = 'Good Lead'
        #     good_lead += 1
    print garbage_lead,duplicate_lead,good_lead
    return raw_leads, garbage_lead,duplicate_lead,good_lead


def main():
    raw_leads = get_data()
    emails = get_unique_emails(raw_leads)
    duplicate_emails = find_duplicate_emails(raw_leads,emails)
    raw_duplicate_count(duplicate_emails)
    print assign_status_to_lead(raw_leads,duplicate_emails)


    print "Process Complete"

if __name__ == "__main__":

    main()
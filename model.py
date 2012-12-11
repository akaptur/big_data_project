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


#----Tagging the dataset with enriched info 

def assign_status_to_garbage_leads(raw_leads,emails):
    garbage_lead = 0
    r_length = len(raw_leads)
    for i in range(r_length):
        if raw_leads[i]['Email'] == '':
            raw_leads[i]['Email'] = 'No Email Provided'
            raw_leads[i]['Data Group'] = 'Garbage Lead'
            raw_leads[i]['Status'] = 'Purge'
            raw_leads[i]['Action'] = 'Purge'
            garbage_lead += 1
    print garbage_lead
    return raw_leads, garbage_lead



def assign_status_to_rest(raw_leads,duplicate_emails):
    duplicate_lead = 0
    good_lead = 0
    dupe_emails = []
    dupes_length = len(duplicate_emails)
    for i in range(dupes_length):
        dupe_email = duplicate_emails[i][0]
        if dupe_email is not None:
            dupe_emails.append(dupe_email)
    r_length = len(raw_leads)
    for i in range(r_length):
        if raw_leads[i]['Email'] in dupe_emails:
            raw_leads[i]['Data Group'] = 'Duplicate Lead'
            raw_leads[i]['Status'] = 'Duplicate'
            raw_leads[i]['Action'] = 'Pending'
            duplicate_lead += 1
        else:
            raw_leads[i]['Data Group'] = 'Good Lead'
            raw_leads[i]['Status'] = 'Retain'
            raw_leads[i]['Action'] = 'Retain'
            good_lead += 1
    print good_lead, "Good Leads", duplicate_lead, "Duplicates with", len(dupe_emails),"unique email addresses"
    return raw_leads


def write_test_file(raw_leads):
    output = raw_leads
    csv_file = open('test_output.csv','w')
    # writer = csv.writer("Lead ID,iContact Contact Id,First Name,Last Name,Email,Email Opt Out,Email Bounced Reason,Phone,Type,Position (Player),Other Phone,Title,Lead Owner,Company / Account,Description,Created By,Lead Source,Rating,Street,Street Line 1,City,State/Province,Zip/Postal Code,Country,Data Group,Status,Action")
    # file.write("\n")
    r_length = len(raw_leads)
    for i in range(r_length):
        print raw_leads[i]
        for key,value in raw_leads[i].items():
            
            print key,value 
        import pdb; pdb.set_trace()
        break 


    # for j in full[i]:
    # line = str(j) + ',' + str(i) + '\n'
    # csv.write(line)


def main():
    raw_leads = get_data()
    emails = get_unique_emails(raw_leads)
    duplicate_emails = find_duplicate_emails(raw_leads,emails)
    raw_duplicate_count(duplicate_emails)
    assign_status_to_garbage_leads(raw_leads,duplicate_emails)
    raw_leads = assign_status_to_rest(raw_leads,duplicate_emails)
    write_test_file(raw_leads)   
    #assess_duplicates(raw_leads,stats)
    print "Process Complete"

if __name__ == "__main__":

    main()
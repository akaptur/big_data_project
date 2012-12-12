import csv
from collections import *
from itertools import * 


#email_counter = collections.Counter()


# Import Data from base file 
data = 'trilogy_base.csv'
f=open(data,'rU')

def get_data():
    read_data=csv.DictReader(f,fieldnames=None)
    raw_leads = list(read_data)
    print len(raw_leads), "leads"
    return raw_leads

#Find all Unique email addresses & count how many times they appear  
def get_unique_emails(raw_leads):
    emails = {}
    for row in raw_leads:
        if row['Email'] in emails:
            emails[row['Email']] += 1
        else:
            emails[row['Email']] = 1
    print len(emails), "unique email addresses within", sum(emails.itervalues()), "leads"
    return emails

#create separate list for duplicates 
def find_duplicate_emails(raw_leads,emails):
    duplicate_emails = []
    for key, value in emails.iteritems():   
        if value > 1:
            duplicate_emails.append([key, value])
    print len(duplicate_emails), "emails are duplicates"
    return duplicate_emails

#how many duplicates in aggregrate 
def raw_duplicate_count(duplicate_emails):
    list_count = 0
    for list in duplicate_emails:
        list_count += list[1]
    print "Duplicate emails appear", float(list_count)/len(duplicate_emails), "times, on average"
    return list_count

#--------->


#add data to key empty fields 
def fill_empty_field_no_data_label(raw_leads):
    r_length = len(raw_leads)
    for i in range(r_length):
        raw_leads[i]['Lead Owner'] = 'Mitch Belisle'
        if raw_leads[i]['iContact Contact Id'] == '':
            raw_leads[i]['iContact Contact Id'] = "No Data"
        if raw_leads[i]['Street'] == '':
            raw_leads[i]['Street'] = "No Data"
        if raw_leads[i]['Email'] == '':
            raw_leads[i]['Email'] = "No Data"

    return raw_leads 

#determine quality of lead + assign preliminary status, action, dupe rationale,merge id reference
def assign_status(raw_leads,duplicate_emails):
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
            raw_leads[i]['Dupe Rationale'] = 'Pending'
            raw_leads[i]['Merge Lead ID'] = 'Pending'
            duplicate_lead += 1
        else:
            raw_leads[i]['Data Group'] = 'Good Lead'
            raw_leads[i]['Status'] = 'Retain'
            raw_leads[i]['Action'] = 'Retain'
            raw_leads[i]['Dupe Rationale'] = 'Not Applicable'
            raw_leads[i]['Merge Lead ID'] = 'Not Applicable'
            good_lead += 1

    print  "There are", good_lead, "Good Leads"
    print "There are", duplicate_lead, "duplicates with", len(dupe_emails),"unique email addresses"
    return raw_leads, dupe_emails

#find garbage leads -- this will be refactored and inserted into assign status
def find_garbage_leads(raw_leads):
    r_length = len(raw_leads)
    garbage_lead = 0 
    for i in range(r_length):
        if raw_leads[i]['Email'] == 'No Data':
            raw_leads[i]['Data Group'] = 'Garbage Lead'
            raw_leads[i]['Status'] = 'Purge'
            raw_leads[i]['Action'] = 'Purge'
            raw_leads[i]['Dupe Rationale'] = 'Not Applicable'
            raw_leads[i]['Merge Lead ID'] = 'Not Applicable'
            garbage_lead += 1
    print "There are", garbage_lead, "Garbage Leads. Garbage Leads have no email address."
    return raw_leads

#create stage_file csv
def data_output(raw_leads):
    fields = ["Lead ID", "iContact Contact Id", "First Name","Last Name","Email","Email Opt Out","Email Bounced Reason","Phone","Type","Position (Player)","Other Phone","Title","Lead Owner","Company / Account","Description","Created By","Lead Source","Rating","Street","Street Line 1","City","State/Province","Zip/Postal Code","Country","Data Group","Status","Dupe Rationale", "Action", "Merge Lead ID"]

    with open('staging_file_a.csv','wb') as csvfile:
        writer = csv.writer(csvfile, quotechar=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(fields)
        for lead in raw_leads:
            lead_values = [lead[field] for field in fields]
            writer.writerow(lead_values)

#provide stats to support tie-out 
def stats(raw_leads):
    duplicate_lead = 0
    good_lead = 0
    garbage_lead = 0 
    r_length = len(raw_leads)
    for i in range(r_length):
        if raw_leads[i]['Data Group'] == 'Duplicate Lead':
            duplicate_lead += 1
        if raw_leads[i]['Data Group'] == 'Good Lead':
            good_lead += 1
        if raw_leads[i]['Data Group'] == 'Garbage Lead':
            garbage_lead += 1
    return duplicate_lead, garbage_lead, good_lead


def get_duplicate_list(raw_leads):
    dup_list = []
    fields = ["Lead ID", "iContact Contact Id", "First Name","Last Name","Email","Email Opt Out","Email Bounced Reason","Phone","Type","Position (Player)","Other Phone","Title","Lead Owner","Company / Account","Description","Created By","Lead Source","Rating","Street","Street Line 1","City","State/Province","Zip/Postal Code","Country","Data Group","Status","Dupe Rationale", "Action", "Merge Lead ID"]

    for lead in raw_leads:
        if lead["Data Group"] == 'Duplicate Lead':
            lead_value = [lead[field] for field in fields]
            dup_list.append(lead_value)
    return dup_list


def dup_entries_grouped_by_email(dup_list):
    dup_entries_by_email = {}
    dup_lead_group = []
    for lead in dup_list:
        email = lead[4]
        if email in dup_entries_by_email:
            dup_entries_by_email[email].append(lead) #append to nested list within dictionary as value 
        else:
            dup_entries_by_email[email] = [lead] #create a list 
    return dup_entries_by_email

def test(dup_entries_group):
    for key,value in dup_entries_group.iteritems():
        print key,value 
        break 


def main():
    raw_leads = get_data()
    emails = get_unique_emails(raw_leads)
    duplicate_emails = find_duplicate_emails(raw_leads,emails)
    raw_duplicate_count(duplicate_emails)
    fill_empty_field_no_data_label(raw_leads)
    assign_status(raw_leads,duplicate_emails)
    find_garbage_leads(raw_leads)
    data_output(raw_leads)
    print stats(raw_leads)
    dup_list = get_duplicate_list(raw_leads)
    dup_entries_group = dup_entries_grouped_by_email(dup_list)
    test(dup_entries_group)


    print "Process Complete"

if __name__ == "__main__":

    main()
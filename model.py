import csv
import collections
import itertools
# from collections import *
# from itertools import * 

#1 Import Data from base file 
data = 'trilogy_base.csv'
f=open(data,'rU')

def get_data():
    read_data=csv.DictReader(f,fieldnames=None)
    raw_leads = list(read_data)
    print len(raw_leads), "leads"
    return raw_leads

#2 Find all Unique email addresses & count how many times they appear  
def get_unique_emails(raw_leads):
    emails = {}
    for row in raw_leads:
        if row['Email'] in emails:
            emails[row['Email']] += 1
        else:
            emails[row['Email']] = 1
    print len(emails), "unique email addresses within", sum(emails.itervalues()), "leads"
    return emails

#3 Create separate list for duplicates 
def find_duplicate_emails(raw_leads,emails):
    duplicate_emails = []
    for key, value in emails.iteritems():   
        if value > 1:
            duplicate_emails.append([key, value])
    print len(duplicate_emails), "emails are duplicates"
    return duplicate_emails

#4 how many duplicates in aggregrate 
def raw_duplicate_count(duplicate_emails):
    list_count = 0
    for list in duplicate_emails:
        list_count += list[1]
    print "Duplicate emails appear", float(list_count)/len(duplicate_emails), "times, on average"
    return list_count

#--------->


#5 add data to critical empty fields 
def fill_empty_field_no_data_label(raw_leads):
    r_length = len(raw_leads)
    for i in range(r_length):
        raw_leads[i]['Lead Owner'] = 'Mitch Belisle'
        if raw_leads[i]['Lead ID'] == '':
            raw_leads[i]['Lead ID'] = "No Data"
        if raw_leads[i]['iContact Contact Id'] == '':
            raw_leads[i]['iContact Contact Id'] = "No Data"
        if raw_leads[i]['Street'] == '':
            raw_leads[i]['Street'] = "No Data"
        if raw_leads[i]['Email'] == '':
            raw_leads[i]['Email'] = "No Data"
        if raw_leads[i]['City'] == '':
            raw_leads[i]['City'] = "No Data"
        if raw_leads[i]['State/Province'] == '':
            raw_leads[i]['State/Province'] = "No Data"
    return raw_leads 

#6 determine quality of lead & assign preliminary status, action, dupe rationale,merge id reference
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

#6a Find garbage leads -- this will be refactored and inserted into assign status
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

# #7 Create 1st Stage File for Review 
# def data_output(raw_leads):
#     fields = ["Lead ID", "iContact Contact Id", "First Name","Last Name","Email","Email Opt Out","Email Bounced Reason","Phone","Type","Position (Player)","Other Phone","Title","Lead Owner","Company / Account","Description","Created By","Lead Source","Rating","Street","Street Line 1","City","State/Province","Zip/Postal Code","Country","Data Group","Status","Dupe Rationale", "Action", "Merge Lead ID"]

#     with open('staging_file_a.csv','wb') as csvfile:
#         writer = csv.writer(csvfile, quotechar=',', quoting=csv.QUOTE_MINIMAL)
#         writer.writerow(fields)
#         for lead in raw_leads:
#             lead_values = [lead[field] for field in fields]
#             writer.writerow(lead_values)

#8 Provide stats to support tie-out 
# def stats(raw_leads):
#     duplicate_lead = 0
#     good_lead = 0
#     garbage_lead = 0 
#     r_length = len(raw_leads)
#     for i in range(r_length):
#         if raw_leads[i]['Data Group'] == 'Duplicate Lead':
#             duplicate_lead += 1
#         if raw_leads[i]['Data Group'] == 'Good Lead':
#             good_lead += 1
#         if raw_leads[i]['Data Group'] == 'Garbage Lead':
#             garbage_lead += 1
#     return duplicate_lead, garbage_lead, good_lead


#9 Create a Dictionary (hash_table) with email & nested list of all lead_data

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


#10 - Comb each lead same email address and compare critical fields, starting with first and last name 
def assess_duplicate_entries(dup_entries_group,raw_leads):
    identical = 0
    same_family = 0
    pending = 0
    for key in dup_entries_group:
        nested_list_level = dup_entries_group[key]
        #print nested_list_level #level
        lead_id_list = []
        icontact_list = []
        first_name_list = []
        last_name_list = []
        city_list = []
        state_list = []
        for field in nested_list_level:
            lead_id = field[0]
            icontact = field[1]
            first_name = field[2]
            last_name = field[3]
            city = field[20]
            state =field[21]
            lead_id_list.append(lead_id)
            icontact_list.append(icontact)
            first_name_list.append(first_name)
            last_name_list.append(last_name)
            city_list.append(city)
            state_list.append(state)
        #Identical
        if all(x == first_name_list[0] for x in first_name_list) and all(y == last_name_list[0] for y in last_name_list):
            #print first_name,last_name, 'Identical'
            best_field_selection(lead_id_list,icontact_list,city_list,state_list,raw_leads)
            identical += 1
        #Same Family (potentially...)
        elif all(x == first_name_list[0] for x in first_name_list) or all(y == last_name_list[0] for y in last_name_list):
            best_field_selection(lead_id_list,icontact_list,city_list,state_list,raw_leads)
            same_family += 1 #this will be assigned to Dupe Rationale
        else:
        #'Unknown - Different Names'
            best_field_selection(lead_id_list,icontact_list,city_list,state_list,raw_leads)
            pending += 1
    #print identical, "identical lead(s).", same_family, "leads are most kids that from the same family", pending, "are still pending evaluation"
    return icontact_list, lead_id_list, first_name_list,last_name_list,city_list,state_list

def best_field_selection(lead_id_list,icontact_list,city_list,state_list,raw_leads):
    best_fields_list = []
    merge_lead_id = lead_id_list[0]

    #lead_id
    if all(x == lead_id_list[0] for x in lead_id_list):
        best_fields_list.append(lead_id_list[0])
    else:
        lead_id_list = [item for item in lead_id_list if item != 'No Data']
        best_fields_list.append(lead_id_list[0])

    #icontact_list
    if all(x == icontact_list[0] for x in icontact_list):
        best_fields_list.append(icontact_list[0])
    else:
        icontact_list = [item for item in icontact_list if item != 'No Data']
        best_fields_list.append(icontact_list[0])
    
    #city_list 
    if all(x == city_list[0] for x in city_list):
        best_fields_list.append(city_list[0])
    else:
        city_list = [item for item in city_list if item != 'No Data']
        best_fields_list.append(city_list[0])
    
    #state_list
    if all(x == state_list[0] for x in state_list):
        best_fields_list.append(state_list[0])
    else:
        state_list = [item for item in state_list if item != 'No Data']
        best_fields_list.append(state_list[0])

    update_merged_duplicate_master(raw_leads,best_fields_list,merge_lead_id, lead_id_list)
    update_duplicates_for_merge_purge(raw_leads,best_fields_list,merge_lead_id, lead_id_list)
    
    # print "The following records were merged\n", lead_id_list, "\n",  merge_lead_id, 'is the merge_lead_id.\n', best_fields_list, "are more likely the best fields for critical fields in the merged row"
    return raw_leads


#11 - Update the merge_id within raw_leads with best_fields
def update_merged_duplicate_master(raw_leads,best_fields_list,merge_lead_id,lead_id_list):
    leads = raw_leads
    best_fields = best_fields_list
    merge_id = merge_lead_id
    lead_ids_for_merge = lead_id_list[1:] 
    for lead in lead_id_list:
        merge_id = lead_id_list[0]
        r_length = len(raw_leads)
        for i in range(r_length):
            if raw_leads[i]['Lead ID'] == merge_id and best_fields[0] == merge_id:
                raw_leads[i]['iContact Contact Id'] = best_fields[1]
                raw_leads[i]['City'] = best_fields[2]
                raw_leads[i]['State'] = best_fields[3]
                raw_leads[i]['Duplicate Rationale'] = 'Test'
                raw_leads[i]['Action'] = 'Retain'
                raw_leads[i]['Merge Lead ID'] = 'Master Merge'

#12 - Assign 'Merge & Purge' to duplicates in lead_id_list and merge_id to Merge Lead ID (represents the retained duplicate)
def update_duplicates_for_merge_purge(raw_leads,best_fields_list,merge_lead_id, lead_id_list):
    leads = raw_leads
    best_fields = best_fields_list
    for lead in lead_id_list:
        merge_id = lead_id_list[0]
        lead_ids_for_merge = lead_id_list[1:]
        r_length = len(raw_leads)
        for i in range(r_length):
            if raw_leads[i]['Lead ID'] == lead and lead != merge_id:
                raw_leads[i]['Duplicate Rationale'] = 'TBD'
                raw_leads[i]['Action'] = 'Merge & Purge'
                raw_leads[i]['Merge Lead ID'] = merge_id
 

#14 - Create staging_file_retain, staging_file_merge_purge

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
    for i in range(r_length):
        if raw_leads[i]['Action'] == 'Purge':
            purge += 1
        if raw_leads[i]['Action'] == 'Merge & Purge':
            merge_purge += 1
        if raw_leads[i]['Action'] == 'Retain':
            retain += 1
    print purge, "leads should be purged \n"
    print merge_purge, "leads should be merged & then purged"
    print retain, "leads should be retained. This includes a master merge lead with best selected data from duplicates"

    return duplicate_lead, garbage_lead, good_lead, purge, merge_purge, retain


#13 - Create a new staging_file_b (Master with everything)
def stage_file_with_updates(raw_leads):
    fields = ["Lead ID", "iContact Contact Id", "First Name","Last Name","Email","Email Opt Out","Email Bounced Reason","Phone","Type","Position (Player)","Other Phone","Title","Lead Owner","Company / Account","Description","Created By","Lead Source","Rating","Street","Street Line 1","City","State/Province","Zip/Postal Code","Country","Data Group","Status","Dupe Rationale", "Action", "Merge Lead ID"]

    with open('stage_file_w_updates.csv','wb') as csvfile:
        writer = csv.writer(csvfile, quotechar=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(fields)
        for lead in raw_leads:
            lead_values = [lead[field] for field in fields]
            writer.writerow(lead_values)

#14 - Create staging_file_retain, staging_file_merge_purge




###### Main 
def main():
    raw_leads = get_data()
    emails = get_unique_emails(raw_leads)
    duplicate_emails = find_duplicate_emails(raw_leads,emails)
    raw_duplicate_count(duplicate_emails)
    fill_empty_field_no_data_label(raw_leads)
    assign_status(raw_leads,duplicate_emails)
    find_garbage_leads(raw_leads)
    #data_output(raw_leads)
    print stats(raw_leads)
    dup_list = get_duplicate_list(raw_leads)
    dup_entries_group = dup_entries_grouped_by_email(dup_list)
    assess_duplicate_entries(dup_entries_group,raw_leads)
    stage_file_with_updates(raw_leads)

    print "Process Complete"

if __name__ == "__main__":

    main()
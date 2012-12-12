import model 
import collections


# c = collections.Counter(['Kisha', 'Kisha'])
# print c['Kisha']
# print c['eggs']

    fields = ["Lead ID", "iContact Contact Id", "First Name","Last Name","Email","Email Opt Out","Email Bounced Reason","Phone","Type","Position (Player)","Other Phone","Title","Lead Owner","Company / Account","Description","Created By","Lead Source","Rating","Street","Street Line 1","City","State/Province","Zip/Postal Code","Country","Data Group","Status","Dupe Rationale", "Action", "Merge Lead ID"]
f_list = [t for t in enumerate(fields)]

print f_list
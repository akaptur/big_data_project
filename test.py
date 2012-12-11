import model 
output = mraw_leads

def writeOutput(filename, output):
   #Open the file
  file = open(filename, "w")

  file.write("Lead ID,iContact Contact Id,First Name,Last Name,Email,Email Opt Out,Email Bounced Reason,Phone,Type,Position (Player),Other Phone,Title,Lead Owner,Company / Account,Description,Created By,Lead Source,Rating,Street,Street Line 1,City,State/Province,Zip/Postal Code,Country,Data Group,Status,Action")
  file.write("\n")

  for record in output:
   print record
   brea
   for item in record:
      itemAsString = str(item)
      file.write(itemAsString)
      file.write(",")
      file.write("\n")
file.close()


writeOutput("test_output.csv", output)
import unicodecsv

def read_csv(filename):
    with open(filename, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)

enrollments = read_csv('/datasets/ud170/udacity-students/enrollments.csv')
daily_engagement = read_csv('/datasets/ud170/udacity-students/daily_engagement.csv')
project_submissions = read_csv('/datasets/ud170/udacity-students/project_submissions.csv')
    
### For each of these three tables, find the number of rows in the table and
### the number of unique students in the table. To find the number of unique
### students, you might want to create a set of the account keys in each table.

def look1stRow():
    print enrollments[0]
    print daily_engagement[0]
    print project_submissions[0]

def getUniqStudent(dict_, key_):
    tmpset = set()
    for row in dict_:
        tmpset.add(row[key_])
    return tmpset

enrollment_num_rows = len(enrollments)             # Replace this with your code
enr_uniq_students = getUniqStudent(enrollments, 'account_key')
enrollment_num_unique_students = len(enr_uniq_students) # Replace this with your code

engagement_num_rows = len(daily_engagement)             # Replace this with your code
eng_uniq_students = getUniqStudent(daily_engagement, 'acct')
engagement_num_unique_students = len(eng_uniq_students)  # Replace this with your code

submission_num_rows = len(project_submissions)             # Replace this with your code
subm_uniq_students = getUniqStudent(project_submissions, 'account_key')
submission_num_unique_students = len(subm_uniq_students)  # Replace this with your code

def summarizeData():
    '''print some basic summary numbers of the dataset'''
    print enrollment_num_rows, enrollment_num_unique_students,\
          engagement_num_rows, engagement_num_unique_students,\
          submission_num_rows, submission_num_unique_students

#Quiz 10
for dict_ in daily_engagement:
    dict_['account_key'] = dict_['acct']
    del dict_['acct']
#print "Modified dict:"
#print daily_engagement[0]['account_key'] #The same as required
# print 'acct' in daily_engagement[0] # To check if  del works perfect. Indeed this is false

#Quiz 11
'''
for i, it in enumerate(diff):
    print it
    if i > 9: break
'''
#canceledList = [ss for ss in enrollments if ss['status'] == 'canceled']
#print len(getUniqStudent(canceledList, 'account_key'))
#set_ = {'1304', '1129', '1186', '875', '1222'}
def getEnrNotEngaging():
    diff = enr_uniq_students.difference(eng_uniq_students) # some account key:1304, 1129, 1186, 875, 1222, 1213, 1120, 749, 1148, 707
    return [std for std in enrollments if std['account_key'] in diff]

#print [ss for ss in getEnrNotEngaging() if not ss['days_to_cancel'] == '0']
print [ss for ss in getEnrNotEngaging() if not ss['days_to_cancel'] == '0']

#Quiz14
from datetime import datetime as dt
def is_paid_std(record):
    '''Arg: a row in raw enrollments; Return: boolean'''
    return (record['days_to_cancel'] == '' or int(record['days_to_cancel']) > 7) and record['is_udacity'] != 'True'

#paid_students = {std['account_key']:std['join_date'] for std in enrollments if is_paid_std(std)}
# Above solution did not take into account multiple records in enrollment with different join-date
def parse_date(datestr):
    '''Take a date as string, and return datetime object'''
    if datestr == '' : return None # Effective Python: should prefer raise ValueError("Cannot convert empty str to date")
    else: return dt.strptime(datestr, "%Y-%m-%d")
    
paid_students = {}
for std in enrollments:
    if is_paid_std(std):
        if std['account_key'] not in paid_students\
            or parse_date(std['join_date']) > parse_date(paid_students[std['account_key']]):
            paid_students[std['account_key']] = std['join_date']

print len(paid_students) #995

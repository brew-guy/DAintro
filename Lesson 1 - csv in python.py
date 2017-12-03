# Udacity Intro to Data Analysis - Lesson 1
# Runs with python 2 in DAND conda environment

import unicodecsv
from datetime import datetime as dt

## Longer version of code (replaced with shorter, equivalent version below)
# enrollments = []
# f = open(enrollments_filename, 'rb')
# reader = unicodecsv.DictReader(f)
# for row in reader:
#     enrollments.append(row)
# f.close()

# Shorter version
# with open(enrollments_filename, 'rb') as f:
#     reader = unicodecsv.DictReader(f)
#     enrollments = list(reader)

### Write code similar to the above to load the engagement
### and submission data. The data is stored in files with
### the given filenames. Then print the first row of each
### table to make sure that your code works. You can use the
### "Test Run" button to see the output of your code.

# My code:
def read_csv (filename):
    with open(filename, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)

enrollments_filename = 'datasets/enrollments.csv'
engagement_filename = 'datasets/daily_engagement.csv'
submissions_filename = 'datasets/project_submissions.csv'

enrollments = read_csv(enrollments_filename)
daily_engagement = read_csv(engagement_filename)
project_submissions = read_csv(submissions_filename)

# Takes a date as a string, and returns a Python datetime object.
# If there is no date given, returns None
def parse_date(date):
    if date == '':
        return None
    else:
        return dt.strptime(date, '%Y-%m-%d')

# Takes a string which is either an empty string or represents an integer,
# and returns an int or None.
def parse_maybe_int(i):
    if i == '':
        return None
    else:
        return int(i)

# Clean up the data types in the enrollments table
for enrollment in enrollments:
    enrollment['cancel_date'] = parse_date(enrollment['cancel_date'])
    enrollment['days_to_cancel'] = parse_maybe_int(enrollment['days_to_cancel'])
    enrollment['is_canceled'] = enrollment['is_canceled'] == 'True'
    enrollment['is_udacity'] = enrollment['is_udacity'] == 'True'
    enrollment['join_date'] = parse_date(enrollment['join_date'])

# Clean up the data types in the engagement table
for engagement_record in daily_engagement:
    engagement_record['lessons_completed'] = int(float(engagement_record['lessons_completed']))
    engagement_record['num_courses_visited'] = int(float(engagement_record['num_courses_visited']))
    engagement_record['projects_completed'] = int(float(engagement_record['projects_completed']))
    engagement_record['total_minutes_visited'] = float(engagement_record['total_minutes_visited'])
    engagement_record['utc_date'] = parse_date(engagement_record['utc_date'])

# Clean up the data types in the submissions table
for submission in project_submissions:
    submission['completion_date'] = parse_date(submission['completion_date'])
    submission['creation_date'] = parse_date(submission['creation_date'])

print "1st row in enrollments:", enrollments[0]
print "1st row in daily_engagement:", daily_engagement[0]
print "1st row in project_submissions:", project_submissions[0]

# Questions to raise from the student data files
# 1. How many unique accounts are there in each file?
# 2. Which days of the week were users more engaged?
# 3. How many lessons/projects did users complete?
# 4. How many mintutes did users spend to complete lessons/projects?
# 5. Did users with DISTINCTION rating spend more time completing lessons/project than users with other ratings?

# For each of the three files you've loaded, find the total number of rows in the csv and the number of unique students.
# To find the number of unique students in each table, you might want to try creating a set of the account keys.

def set_from_list(list, dictkey):
    valueset = set()
    for record in list:
        valueset.add(record[dictkey])
    return valueset

unique_enrolled_students = set_from_list(enrollments, 'account_key')
unique_engagement_students = set_from_list(daily_engagement, 'acct')
unique_project_submitters = set_from_list(project_submissions, 'account_key')

print "Rows in enrollments:"+"\t"*5, len(enrollments)
print "Unique accounts in enrollments:"+"\t"*3, len(unique_enrolled_students)

print "Rows in daily_engagement:"+"\t"*4, len(daily_engagement)
print "Unique accounts in daily_engagement:\t", len(unique_engagement_students)

print "Rows in project_submissions:"+"\t"*3, len(project_submissions)
print "Unique accounts in project_submissions:\t", len(unique_project_submitters)

# Rename the 'acct' column to 'account_key' in the daily_engagement table
# Show the output of daily_engagement[0]["account_key"]

for dict in daily_engagement:
    dict["account_key"] = dict.pop("acct")
    # Alternative code that renames a key in the dictionary:
    # dict["account_key"] = dict["acct"]
    # del[dict["acct"]]

print "1st row in daily_engagement:", daily_engagement[0]
print daily_engagement[0]["account_key"]

# Why are students missing from daily_engagement?
# Identify surprising data points: Any enrollment record with no corresponding engangement data

# Using difference operation on my sets to identify students not in both sets
students_missing_from_engagement = unique_enrolled_students - unique_engagement_students

problem_count = 0
for enrollment in enrollments:
    student = enrollment["account_key"]
    if student not in unique_engagement_students:
        print enrollment
        problem_count += 1

print "Total: ", problem_count

# Results show that some accounts have joined date = canceled date
# This may explain why these don't show up on engagement. They may need at least one day before their engagement is recorded.

# Show records where students stayed enrolled for at least a day but are missing from the daily_engagement:

problem_count = 0
for enrollment in enrollments:
    student = enrollment["account_key"]
    if student not in unique_engagement_students and enrollment['join_date'] != enrollment['cancel_date']:
            print enrollment
            problem_count += 1

print "Total: ", problem_count

# These were all Udacity test accounts and should be removed from the data set

udacity_test_accounts = set()
for enrollment in enrollments:
    if enrollment['is_udacity']:
        udacity_test_accounts.add(enrollment['account_key'])
print "Udacity test accounts:", len(udacity_test_accounts)

def remove_udacity_test_accounts (list):
    non_udacity_list = []
    for record in list:
        if record['account_key'] not in udacity_test_accounts:
            non_udacity_list.append(record)
    return non_udacity_list

non_udacity_enrollments = remove_udacity_test_accounts(enrollments)
non_udacity_engagement = remove_udacity_test_accounts(daily_engagement)
non_udacity_submissions = remove_udacity_test_accounts(project_submissions)

print "Enrollments without Udacity test accounts:"+"\t"*3, len(non_udacity_enrollments)
print "Engagement without Udacity test accounts:"+"\t"*3, len(non_udacity_engagement)
print "Project submissions without Udacity test accounts:\t", len(non_udacity_submissions)

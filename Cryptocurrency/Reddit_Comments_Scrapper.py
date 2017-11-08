# Dependencies
import praw
import csv
import os

absolute_path = os.path.abspath(__file__)
directory_name = os.path.dirname(absolute_path)
os.chdir(directory_name)

r = praw.Reddit(client_id='',
                client_secret='',
                password='',
                user_agent='',
                username='')

uniq_id = ''
campaing = ''
counter = ''

output_csv = "Reddit_Comments.csv"

with open(output_csv, "a") as output:
    writer = csv.writer(output, lineterminator='\n')
    for comment in r.subreddit(uniq_id).comments(limit=None):
        print(comment.body)
        writer.writerow([counter]+[campaing]+[comment.body])
        counter += 1
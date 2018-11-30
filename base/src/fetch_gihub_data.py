import os
import argparse
import pandas as pd
from github import Github

LOGIN = os.environ['GITHUB_LOGIN']
PASSWORD = os.environ['GITHUB_PASSWORD']

api = Github(LOGIN, PASSWORD)

# Parsing flags.
parser = argparse.ArgumentParser()
parser.add_argument("--topic_name")
args = parser.parse_args()
print(args)

result = api.search_repositories(
    'topic:{}'.format(args.topic_name), sort='stars')

columns = ('repo_name', 'html_url',
           'description', 'topics')


# loop through 1,000 repositories order by the number of stars
data = []
for index in range(0, 33):
    for item in result.get_page(index):
        if item.description and not item.fork:
            try:
                data.append([item.name, item.html_url, item.description.encode('utf-8'),
                             item.get_topics()])
            except Exception as e:
                print(e)
                break

# create pandas dataframe
df = pd.DataFrame(data, columns=columns)
# save to CSV
df.to_csv('{}_output.csv'.format(args.topic_name), index=False)
print('file {}_output.csv created'.format(args.topic_name))

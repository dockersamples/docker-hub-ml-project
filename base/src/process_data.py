from nltk.corpus import stopwords
import ast
import argparse
import pickle
import pandas as pd
import nltk
import re
from sklearn.model_selection import train_test_split

# Parsing flags.
parser = argparse.ArgumentParser()
parser.add_argument("--input_csv")
parser.add_argument("--mount_path")
parser.add_argument("--output_train_csv")
parser.add_argument("--output_test_csv")
parser.add_argument("--selected_categories")
parser.add_argument("--test_size")
args = parser.parse_args()
print(args)


# Load data from CVS
raw_data = pd.read_csv('{}/{}'.format(args.mount_path, args.input_csv))

# Remove records with empty descriptions
data = raw_data[raw_data.FULL_DESCRIPTION.notna()]
# Lower case
data.FULL_DESCRIPTION = data.FULL_DESCRIPTION.str.lower()
# Remove punctuation
data.FULL_DESCRIPTION = data.FULL_DESCRIPTION.str.replace('[^\w\s]', '')
# Remove numbers
data.FULL_DESCRIPTION = data.FULL_DESCRIPTION.str.replace('\d+', '')
# Remove `\n` and  `\t` characters
data.FULL_DESCRIPTION = data.FULL_DESCRIPTION.str.replace('\n', ' ')
data.FULL_DESCRIPTION = data.FULL_DESCRIPTION.str.replace('\t', ' ')
# Remove long strings (len() > 24)
data.FULL_DESCRIPTION = data.FULL_DESCRIPTION.str.replace('\w{24,}', '')
# Remove urls
data.FULL_DESCRIPTION = data.FULL_DESCRIPTION.str.replace('http\w+', '')
# Remove extra spaces
data.FULL_DESCRIPTION = data.FULL_DESCRIPTION.str.strip()
data.FULL_DESCRIPTION.replace({r'[^\x00-\x7F]+': ''}, regex=True, inplace=True)
data.FULL_DESCRIPTION = data.FULL_DESCRIPTION.str.replace(' +', ' ')
data.FULL_DESCRIPTION = data.FULL_DESCRIPTION.replace('\s+', ' ', regex=True)
# Drop duplicates
data = data.drop_duplicates()

# build-test-deploy,languages & frameworks,databases,web servers,application utilities,devops
# operating systems,business tools,continuous integration,message queue,support-sales-and-marketing
selected_categories = args.selected_categories.split(',')

for col in selected_categories:
    data[col] = 0

for index, row in data.iterrows():
    labels = row.labels
    labels = ast.literal_eval(labels)
    labels = [e.strip()for e in labels]
    for l in labels:
        if l in selected_categories:
            data.loc[index, l] = 1
data = data.dropna(axis=1)

# Remove stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
stop_words.update([
    'default',
    'image',
    'docker',
    'container',
    'service',
    'production',
    'dockerfile',
    'dockercompose',
    'build',
    'latest',
    'file',
    'tag',
    'instance',
    'run',
    'running',
    'use',
    'will',
    'work',
    'please',
    'install',
    'tags',
    'version',
    'create',
    'want',
    'need',
    'used',
    'well',
    'user',
    'release',
    'config',
    'dir',
    'support',
    'exec',
    'github',
    'rm',
    'mkdir',
    'env',
    'folder',
    'http',
    'repo',
    'cd',
    'ssh',
    'root'])

re_stop_words = re.compile(r"\b(" + "|".join(stop_words) + ")\\W", re.I)
data.FULL_DESCRIPTION = data.FULL_DESCRIPTION.apply(
    lambda sentence: re_stop_words.sub(" ", sentence))

# Split data into test and train datasets
train, test = train_test_split(
    data, test_size=float(args.test_size), shuffle=True)

# Print stats about the shape of the data.
print('Train: {:,} rows {:,} columns'.format(train.shape[0], train.shape[1]))
print('Test: {:,} rows {:,} columns'.format(test.shape[0], test.shape[1]))

# save output as CSV.
train.to_csv('{}/{}'.format(args.mount_path,
                            args.output_train_csv), index=False)
test.to_csv('{}/{}'.format(args.mount_path,
                           args.output_test_csv), index=False)
# save list of categories
f2 = open('{}/selected_categories.pckl'.format(args.mount_path), 'wb')
pickle.dump(selected_categories, f2)

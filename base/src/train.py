import argparse
import pickle
import pandas as pd
from keras.layers import Dense
from keras.models import Sequential
from keras import layers
from keras.preprocessing.text import Tokenizer


# Parsing flags.
parser = argparse.ArgumentParser()
parser.add_argument("--mount_path")
parser.add_argument("--input_train_csv")
parser.add_argument("--input_test_csv")
parser.add_argument("--output_model")
parser.add_argument("--output_vectorized_descriptions")
parser.add_argument("--loss", default="binary_crossentropy")
parser.add_argument("--batch_size", default=100)
parser.add_argument("--epochs", default=15)
parser.add_argument("--validation_split", default=0.1)
args = parser.parse_args()
print(args)

# Load data from CVS
train_data = pd.read_csv(
    '{}/{}'.format(args.mount_path, args.input_train_csv))
test_data = pd.read_csv(
    '{}/{}'.format(args.mount_path, args.input_test_csv))

# Remove records with empty descriptions
train_data = train_data[train_data.FULL_DESCRIPTION.notna()]
test_data = test_data[test_data.FULL_DESCRIPTION.notna()]

# Extract full description from datasets
train_text = train_data.FULL_DESCRIPTION.tolist()
test_text = test_data.FULL_DESCRIPTION.tolist()

t = Tokenizer()
t.fit_on_texts(train_text + test_text)

# integer encode documents
x_train = t.texts_to_matrix(train_text, mode='tfidf')
x_test = t.texts_to_matrix(test_text, mode='tfidf')

# Remove unnecessary columns from the datasets
y_train = train_data.drop(labels=['index', 'FULL_DESCRIPTION', 'NAME',
                                  'DESCRIPTION', 'PULL_COUNT', 'CATEGORY1', 'CATEGORY2', 'labels'], axis=1)
y_test = test_data.drop(labels=['index', 'FULL_DESCRIPTION', 'NAME', 'DESCRIPTION',
                                'PULL_COUNT', 'CATEGORY1', 'CATEGORY2', 'labels'], axis=1)

# KERAS MODEL
n_cols = x_train.shape[1]
model = Sequential()

# input layer of 70 neurons:
model.add(Dense(70, activation='relu', input_shape=(n_cols,)))

# output layer of 82 neurons:
model.add(Dense(82, activation='sigmoid'))

# determining optimizer, loss, and metrics:
model.compile(optimizer='adam', loss=args.loss,
              metrics=['binary_accuracy'])

history = model.fit(
    x_train, y_train, batch_size=int(args.batch_size),
    epochs=int(args.epochs), verbose=0, validation_split=float(args.validation_split))
score, acc = model.evaluate(
    x_test, y_test, batch_size=int(args.batch_size), verbose=0)
print("Score/Loss: ", score)
print("Accuracy: ", acc)
# save model
model.save('{}/{}'.format(args.mount_path, args.output_model))
# save tokenizer
f1 = open('{}/{}'.format(args.mount_path,
                         args.output_vectorized_descriptions), 'wb')
pickle.dump(t, f1)

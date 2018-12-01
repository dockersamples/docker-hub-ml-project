import pickle
import re
import numpy as np
from keras.models import load_model


class DockerHubClassification(object):
    def __init__(self):
        self.model = load_model('hub_classifier.h5')
        self.model._make_predict_function()
        self.selected_categories = pickle.load(
            open('selected_categories.pckl', 'rb'))
        self.tokenizer = pickle.load(
            open('vectorized_descriptions.pckl', 'rb'))

    def _clean_string(self, text):
        text = re.sub('[!@#$,.)(=*`]', '', text)
        return text.lower()

    def _predict_labels(self, text):
        labels = []
        description = self._clean_string(str(text))
        description_matrix = self.tokenizer.texts_to_matrix([
            description], mode='tfidf')
        preds = self.model.predict(
            description_matrix, batch_size=None, verbose=1, steps=None)

        preds[preds > 0.4] = 1
        preds[preds < 0.4] = 0

        for c in range(len(self.selected_categories)):
            if preds[0][c] == 1:
                labels.append(self.selected_categories[c])
        return labels

    def predict(self, text, features_names):
        return np.array([self._predict_labels(text)])

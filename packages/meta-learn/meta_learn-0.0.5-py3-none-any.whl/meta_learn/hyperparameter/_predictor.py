# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import os

from sklearn.externals import joblib

from ..data_wrangler import find_best_hyperpara


class Predictor:
    def __init__(self):
        pass

    def search(self, X_test):
        best_para, best_score = self._predict(X_test)
        return best_para, best_score

    def load_model(self, path):
        if os.path.isfile(path):
            self.meta_reg = joblib.load(path)
        else:
            print("File at path", path, "not found")

    def _predict(self, X_test):
        score_pred = self.meta_reg.predict(X_test)
        best_features, best_score = find_best_hyperpara(X_test, score_pred)

        return best_features, best_score

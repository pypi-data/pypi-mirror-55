# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import itertools
import pandas as pd

from .collector._dataset_features import DatasetFeatures
from ..data_wrangler import merge_meta_data


class Recognizer:
    def __init__(self, _cand_):
        self.search_config = _cand_.search_config

        self.model_list = list(self.search_config.keys())
        self.model_name = self.model_list[0]
        self.search_space = self.search_config[self.model_name]

    def get_test_metadata(self, data_train):
        self.collector_dataset = DatasetFeatures()

        md_dataset = self.collector_dataset.collect(data_train)
        md_model = self._features_from_model()

        X_test = merge_meta_data(md_dataset, md_model)

        return X_test

    def _features_from_model(self):
        keys, values = zip(*self.search_space.items())
        meta_reg_input = [dict(zip(keys, v)) for v in itertools.product(*values)]

        md_model = pd.DataFrame(meta_reg_input)

        return md_model

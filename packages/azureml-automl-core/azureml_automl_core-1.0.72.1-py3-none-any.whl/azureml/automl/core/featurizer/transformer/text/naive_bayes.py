# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Wrapper for sklearn Multinomial Naive Bayes."""
from typing import List, Optional
import logging

import numpy as np
from sklearn.naive_bayes import MultinomialNB

from automl.client.core.common.logging_utilities import function_debug_log_wrapped
from automl.client.core.runtime.model_wrappers import _AbstractModelWrapper
from automl.client.core.runtime.types import DataSingleColumnInputType, DataInputType
from azureml.automl.core.constants import SupportedTransformersInternal as _SupportedTransformersInternal
from automl.client.core.runtime import memory_utilities
from ..automltransformer import AutoMLTransformer

# TODO Make this cross-validate in the right way to avoid overfitting


class NaiveBayes(AutoMLTransformer, _AbstractModelWrapper):
    """Wrapper for sklearn Multinomial Naive Bayes."""

    def __init__(self, logger: Optional[logging.Logger] = None):
        """Construct the Naive Bayes transformer.

        :param logger: Logger to be injected to usage in this class.
        """
        super().__init__()
        self.model = MultinomialNB()
        self._init_logger(logger)
        self._transformer_name = _SupportedTransformersInternal.NaiveBayes

    def _get_transformer_name(self) -> str:
        return self._transformer_name

    @function_debug_log_wrapped
    def fit(self, x, y=None):
        """
        Naive Bayes transform to learn conditional probablities for textual data.

        :param x: The data to transform.
        :type x: numpy.ndarray or pandas.series
        :param y: Target values.
        :type y: numpy.ndarray
        :return: The instance object: self.
        """
        self.model.fit(x, y)
        return self

    @function_debug_log_wrapped
    def transform(self, x):
        """
        Transform data x.

        :param x: The data to transform.
        :type x: numpy.ndarray or pandas.series
        :return: Prediction probability values from Naive Bayes model.
        """
        return self.model.predict_proba(x)

    def get_model(self):
        """
        Return inner NB model.

        :return: NaiveBayes model.
        """
        return self.model

    def get_memory_footprint(self, X: DataInputType, y: DataSingleColumnInputType) -> int:
        """
        Obtain memory footprint estimate for this transformer.

        :param X: Input data.
        :param y: Input label.
        :return: Amount of memory taken.
        """
        num_rows = len(X)
        n_classes = len(np.unique(y))
        f_size = memory_utilities.get_data_memory_size(float)
        return num_rows * n_classes * f_size

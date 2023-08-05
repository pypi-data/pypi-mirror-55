# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

"""Defines a dataset wrapper for the performance testing framework
   to test on different model/dataset permutations.
"""

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from tempeh.perf_utilities.munge import munge  # noqa


class BasePerformanceDatasetWrapper(object):
    """Base dataset wrapper."""

    task = None
    data_type = None
    size = None

    def __init__(self, dataset, targets, nrows=None, data_t=None):
        """Initialize base dataset wrapper.

        :param dataset: A matrix of feature vector examples
        :type dataset: numpy.array or pandas.DataFrame or pandas.Series
        :param targets: An array of target values
        :type targets: numpy.array or pandas.Series
        :param nrows: Num of rows (optional)
        :type nrows: int
        :param data_t: array specifying continuous or nominal attributes
        :type data_t: array
        """
        self.features = None
        self.target_names = None
        self.data_t = data_t

        self.dataset = dataset
        self.targets = targets

        dataset_is_df = isinstance(dataset, pd.DataFrame)
        dataset_is_series = isinstance(dataset, pd.Series)
        if dataset_is_df or dataset_is_series:
            self.features = dataset.columns.values.tolist()
            self.dataset = dataset.values

        targets_is_df = isinstance(targets, pd.DataFrame)
        targets_is_series = isinstance(targets, pd.Series)
        if targets_is_df or targets_is_series:
            self.targets = targets.values

        self.nrows = nrows

        self._sample()
        self._training_split()

    def _sample(self, prob=.8, local_var=1):
        """Samples up or down depending on self.nrows."""
        if self.nrows is not None and self.nrows != self.dataset.shape[0]:
            # Set random seed to insure consistency across runs
            np.random.seed(219)

            # Creates random indices for sampling
            # We need to replace if self.nrows > self.dataset.shape[0]
            size = abs(self.nrows - self.dataset.shape[0])
            index = np.random.choice(self.dataset.shape[0], size=size,
                                     replace=self.nrows > self.dataset.shape[0])

            if self.nrows > self.dataset.shape[0]:
                T = np.hstack((self.dataset, np.array([self.targets]).T))
                # Combining the target column to actual dataset
                # Values for probability and local variance taken from github
                new_data = munge(T, self.nrows // T.shape[0],
                                 prob, local_var, self.data_t)
                # Produces a new data set with size equal to an integer multiple of the original
                self.dataset = new_data[:, :-1]
                self.targets = new_data[:, -1:]
            else:
                self.dataset = np.delete(self.dataset, index, 0)
                self.targets = np.delete(self.targets, index, 0)
        else:
            self.nrows = self.dataset.shape[0]

    def _training_split(self):
        """Creates a training split."""
        self.X_train, self.X_test, self.y_train, self.y_test = \
            train_test_split(self.dataset, self.targets, test_size=0.33, random_state=123)

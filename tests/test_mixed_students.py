import numpy as np
from sklearn.model_selection import train_test_split

from mercs import Mercs
from tests.evaluation import compute_scores


def test_students():
    # initialize the models
    mercs = Mercs(
        selection_algorithm="base",
        inference_algorithm="base",
        prediction_algorithm="it",
        max_depth=4,
        nb_targets=2,
        nb_iterations=1,
        n_jobs=1,
        verbose=1,
        max_steps=8,
    )

    mercs_mixed = Mercs(
        selection_algorithm="base",
        inference_algorithm="base",
        prediction_algorithm="it",
        mixed_algorithm="morfist",
        max_depth=7,
        nb_targets=2,
        nb_iterations=1,
        n_jobs=1,
        verbose=1,
        max_steps=8,
    )

    # load the data
    data = np.loadtxt("./data/student-por.csv", delimiter=",", skiprows=1)

    # split the data into training and testing
    x_train, x_test = train_test_split(data, test_size=0.25)

    # ids of the nominal variables
    nominal_ids = {0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 29, 21, 22, 23, 24, 25, 26, 27,
                   28}

    # fit the models
    mercs.fit(x_train, nominal_attributes=nominal_ids)
    mercs_mixed.fit(x_train, nominal_attributes=nominal_ids)

    # create the query code for the prediction
    q_code = np.zeros(x_train.shape[1], dtype=np.int8)
    targets = [1, 21, 31]
    q_code[targets] = 1
    print(q_code)

    # get real values of target variables
    y_test = x_test[:, targets]

    # predict target values
    y_pred = mercs.predict(x_test, q_code=q_code)
    y_pred_mixed = mercs_mixed.predict(x_test, q_code=q_code)

    scores = compute_scores(y_test, y_pred, [0, 1])
    scores_mixed = compute_scores(y_test, y_pred_mixed, [0, 1])

    print(scores)
    print(scores_mixed)

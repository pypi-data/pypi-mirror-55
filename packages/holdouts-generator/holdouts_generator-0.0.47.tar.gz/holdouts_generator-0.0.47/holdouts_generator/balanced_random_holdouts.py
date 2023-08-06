from typing import Callable, List, Tuple, Dict
import itertools
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import numpy as np
from .utils import odd_even_split


def balanced_random_holdout(test_size: float, random_state: int, hyper_parameters: Dict) -> [Callable, str, Tuple[float, int]]:
    """Return a function to create an holdout with given test_size and random_state and the path where to store it.
        test_size:float, float from 0 to 1, representing how many datapoints should be reserved to the test set.
        random_state:int, random state to reproduce experiment.
        hyper_parameters:Dict, additional hyper-parameters used to create the holdout.
    """
    def holdout(dataset: Tuple):
        """
            dataset, the dataset to split. It must finish with an array containing the classes.
        """
        results = []
        rnd = np.random.RandomState(seed=random_state)
        for row in np.array([
            train_test_split(*[d[dataset[-1] == label] for d in dataset],
                             test_size=test_size, random_state=random_state)
            for label in np.unique(dataset[-1])
        ]).T:
            array = np.array(list(itertools.chain.from_iterable(row)))
            results.append(array)
        train, test = odd_even_split(results)
        train = shuffle(*train, random_state=random_state)
        test = shuffle(*test, random_state=random_state)
        return sum(
            ((e1, e2) for e1, e2 in zip(train, test)), tuple()
        )

    return holdout, {
        "test_size": test_size,
        "random_state": random_state
    }


def balanced_random_holdouts(test_sizes: List[float], quantities: List[int], random_state: int = 42, hyper_parameters: Dict = None) -> List[Tuple[Callable, str, List]]:
    """Return a Generator of functions to create an holdouts with given test_sizes.
        test_sizes:List[float], floats from 0 to 1, representing how many datapoints should be reserved to the test set.
        quantities:List[int], quantities of holdouts for each test_size.
        random_state:int=42, random state to reproduce experiment.
        hyper_parameters:Dict, additional hyper-parameters used to create the holdout.
    """
    if len(test_sizes) > 1:
        return [
            (
                *balanced_random_holdout(test_sizes[0], random_state+i, hyper_parameters),
                balanced_random_holdouts(
                    test_sizes[1:], quantities[1:], random_state+i, hyper_parameters)
            ) for i in range(quantities[0])
        ]
    return [(*balanced_random_holdout(test_sizes[0], random_state+i, hyper_parameters), None) for i in range(quantities[0])]

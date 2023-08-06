import numbers

import numpy as np


FLOAT_DTYPES = (np.float64, np.float32, np.float16)


def _check_sample_weight(sample_weight, X, dtype=None):
    """Validate sample weights.
    Note that passing sample_weight=None will output an array of ones.
    Therefore, in some cases, you may want to protect the call with:
    if sample_weight is not None:
        sample_weight = _check_sample_weight(...)
    Parameters
    ----------
    sample_weight : {ndarray, Number or None}, shape (n_samples,)
       Input sample weights.
    X : nd-array, list or sparse matrix
        Input data.
    dtype: dtype
       dtype of the validated `sample_weight`.
       If None, and the input `sample_weight` is an array, the dtype of the
       input is preserved; otherwise an array with the default numpy dtype
       is be allocated.  If `dtype` is not one of `float32`, `float64`,
       `None`, the output will be of dtype `float64`.
    Returns
    -------
    sample_weight : ndarray, shape (n_samples,)
       Validated sample weight. It is guaranteed to be "C" contiguous.
    """
    n_samples = _num_samples(X)

    if dtype is not None and dtype not in [np.float32, np.float64]:
        dtype = np.float64

    if sample_weight is None or isinstance(sample_weight, numbers.Number):
        if sample_weight is None:
            sample_weight = np.ones(n_samples, dtype=dtype)
        else:
            sample_weight = np.full(n_samples, sample_weight,
                                    dtype=dtype)
    else:
        if dtype is None:
            dtype = [np.float64, np.float32]

        sample_weight = check_array(sample_weight, dtype=dtype)

        if sample_weight.ndim != 1:
            raise ValueError("Sample weights must be 1D array or scalar")

        if sample_weight.shape != (n_samples,):
            raise ValueError("sample_weight.shape == {}, expected {}!"
                             .format(sample_weight.shape, (n_samples,)))
    return sample_weight


def check_random_state(seed):
    """Turn seed into a np.random.RandomState instance
    Parameters
    ----------
    seed : None | int | instance of RandomState
        If seed is None, return the RandomState singleton used by np.random.
        If seed is an int, return a new RandomState instance seeded with seed.
        If seed is already a RandomState instance, return it.
        Otherwise raise ValueError.
    """
    if seed is None or seed is np.random:
        return np.random.mtrand._rand
    if isinstance(seed, numbers.Integral):
        return np.random.RandomState(seed)
    if isinstance(seed, np.random.RandomState):
        return seed
    raise ValueError('%r cannot be used to seed a numpy.random.RandomState'
                     ' instance' % seed)


def _num_samples(x):
    """Return number of samples in array-like x."""
    message = 'Expected sequence or array-like, got %s' % type(x)
    if hasattr(x, 'fit') and callable(x.fit):
        # Don't get num_samples from an ensembles length!
        raise TypeError(message)

    if not hasattr(x, '__len') and not hasattr(x, 'shape'):
        if hasattr(x, '__array__'):
            x = np.asarray(x)
        else:
            raise TypeError(message)

    if hasattr(x, 'shape') and x.shape is not None:
        if len(x.shape) == 0:
            raise TypeError("Singleton array %r cannot be considered"
                            " a valid collection." % x)
        # Check that shape is returning an integer or default to len
        # Dask dataframes may not return numeric shape[0] value
        if isinstance(x.shape[0], numbers.Integral):
            return x.shape[0]

    try:
        return len(x)
    except TypeError:
        raise TypeError(message)


def check_array(array, dtype="numeric"):
    """Input validation on an array, list, sparse matrix or similar.
        By default, the input is checked to be a non-empty 2D array containing
        only finite values. If the dtype of the array is object, attempt
        converting to float, raising on failure.
        Parameters
        ----------
        array : object
            Input object to check / convert.
        dtype : string, type, list of types or None (default="numeric")
            Data type of result. If None, the dtype of the input is preserved.
            If "numeric", dtype is preserved unless array.dtype is object.
        Returns
        -------
        array_converted : object
            The converted and validated array.
        """

    # store reference to original array to check if copy is needed when
    # function returns
    array_orig = array

    # store whether originally we wanted numeric dtype
    dtype_numeric = isinstance(dtype, str) and dtype == "numeric"

    dtype_orig = getattr(array, "dtype", None)
    if not hasattr(dtype_orig, 'kind'):
        # not a data type (e.g. a column named dtype in a pandas DataFrame)
        dtype_orig = None

    # check if the object contains several dtypes (typically a pandas
    # DataFrame), and store them. If not, store None.
    dtypes_orig = None
    if hasattr(array, "dtypes") and hasattr(array.dtypes, '__array__'):
        dtypes_orig = np.array(array.dtypes)
        if all(isinstance(dtype, np.dtype) for dtype in dtypes_orig):
            dtype_orig = np.result_type(*array.dtypes)

    if dtype_numeric:
        if dtype_orig is not None and dtype_orig.kind == "O":
            # if input is object, convert to float.
            dtype = np.float64
        else:
            dtype = None

    if isinstance(dtype, (list, tuple)):
        if dtype_orig is not None and dtype_orig in dtype:
            # no dtype conversion required
            dtype = None
        else:
            # dtype conversion required. Let's select the first element of the
            # list of accepted types.
            dtype = dtype[0]

    if dtype is not None and np.dtype(dtype).kind in 'iu':
        # Conversion float -> int should not contain NaN or
        # inf (numpy#14412). We cannot use casting='safe' because
        # then conversion float -> int would be disallowed.
        array = np.asarray(array)
        array = array.astype(dtype, casting="unsafe", copy=False)
    else:
        array = np.asarray(array, dtype=dtype)

    return array



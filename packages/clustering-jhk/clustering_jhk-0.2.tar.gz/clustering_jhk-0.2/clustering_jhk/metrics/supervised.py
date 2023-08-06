from math import log

import numpy as np
from scipy import sparse as sp


def homogeneity_score(labels_true, labels_pred):
    """Homogeneity metric of a cluster labeling given a ground truth.
    A clustering result satisfies homogeneity if all of its clusters
    contain only data points which are members of a single class.
    This metric is independent of the absolute values of the labels:
    a permutation of the class or cluster label values won't change the
    score value in any way.
    This metric is not symmetric: switching ``label_true`` with ``label_pred``
    will return the :func:`completeness_score` which will be different in
    general.
    Read more in the :ref:`User Guide <homogeneity_completeness>`.
    Parameters
    ----------
    labels_true : int array, shape = [n_samples]
        ground truth class labels to be used as a reference
    labels_pred : array-like of shape (n_samples,)
        cluster labels to evaluate
    Returns
    -------
    homogeneity : float
       score between 0.0 and 1.0. 1.0 stands for perfectly homogeneous labeling
    References
    ----------
    .. [1] `Andrew Rosenberg and Julia Hirschberg, 2007. V-Measure: A
       conditional entropy-based external cluster evaluation measure
       <https://aclweb.org/anthology/D/D07/D07-1043.pdf>`_
    See also
    --------
    completeness_score
    v_measure_score
    Examples
    --------
    Perfect labelings are homogeneous::
      >>> from sklearn.metrics.cluster import homogeneity_score
      >>> homogeneity_score([0, 0, 1, 1], [1, 1, 0, 0])
      1.0
    Non-perfect labelings that further split classes into more clusters can be
    perfectly homogeneous::
      >>> print("%.6f" % homogeneity_score([0, 0, 1, 1], [0, 0, 1, 2]))
      1.000000
      >>> print("%.6f" % homogeneity_score([0, 0, 1, 1], [0, 1, 2, 3]))
      1.000000
    Clusters that include samples from different classes do not make for an
    homogeneous labeling::
      >>> print("%.6f" % homogeneity_score([0, 0, 1, 1], [0, 1, 0, 1]))
      0.0...
      >>> print("%.6f" % homogeneity_score([0, 0, 1, 1], [0, 0, 0, 0]))
      0.0...
    """
    return homogeneity_completeness_v_measure(labels_true, labels_pred)[0]


def v_measure_score(labels_true, labels_pred, beta=1.0):
    """V-measure cluster labeling given a ground truth.
    This score is identical to :func:`normalized_mutual_info_score` with
    the ``'arithmetic'`` option for averaging.
    The V-measure is the harmonic mean between homogeneity and completeness::
        v = (1 + beta) * homogeneity * completeness
             / (beta * homogeneity + completeness)
    This metric is independent of the absolute values of the labels:
    a permutation of the class or cluster label values won't change the
    score value in any way.
    This metric is furthermore symmetric: switching ``label_true`` with
    ``label_pred`` will return the same score value. This can be useful to
    measure the agreement of two independent label assignments strategies
    on the same dataset when the real ground truth is not known.
    Read more in the :ref:`User Guide <homogeneity_completeness>`.
    Parameters
    ----------
    labels_true : int array, shape = [n_samples]
        ground truth class labels to be used as a reference
    labels_pred : array-like of shape (n_samples,)
        cluster labels to evaluate
    beta : float
        Ratio of weight attributed to ``homogeneity`` vs ``completeness``.
        If ``beta`` is greater than 1, ``completeness`` is weighted more
        strongly in the calculation. If ``beta`` is less than 1,
        ``homogeneity`` is weighted more strongly.
    Returns
    -------
    v_measure : float
       score between 0.0 and 1.0. 1.0 stands for perfectly complete labeling
    References
    ----------
    .. [1] `Andrew Rosenberg and Julia Hirschberg, 2007. V-Measure: A
       conditional entropy-based external cluster evaluation measure
       <https://aclweb.org/anthology/D/D07/D07-1043.pdf>`_
    See also
    --------
    homogeneity_score
    completeness_score
    normalized_mutual_info_score
    Examples
    --------
    Perfect labelings are both homogeneous and complete, hence have score 1.0::
      >>> from sklearn.metrics.cluster import v_measure_score
      >>> v_measure_score([0, 0, 1, 1], [0, 0, 1, 1])
      1.0
      >>> v_measure_score([0, 0, 1, 1], [1, 1, 0, 0])
      1.0
    Labelings that assign all classes members to the same clusters
    are complete be not homogeneous, hence penalized::
      >>> print("%.6f" % v_measure_score([0, 0, 1, 2], [0, 0, 1, 1]))
      0.8...
      >>> print("%.6f" % v_measure_score([0, 1, 2, 3], [0, 0, 1, 1]))
      0.66...
    Labelings that have pure clusters with members coming from the same
    classes are homogeneous but un-necessary splits harms completeness
    and thus penalize V-measure as well::
      >>> print("%.6f" % v_measure_score([0, 0, 1, 1], [0, 0, 1, 2]))
      0.8...
      >>> print("%.6f" % v_measure_score([0, 0, 1, 1], [0, 1, 2, 3]))
      0.66...
    If classes members are completely split across different clusters,
    the assignment is totally incomplete, hence the V-Measure is null::
      >>> print("%.6f" % v_measure_score([0, 0, 0, 0], [0, 1, 2, 3]))
      0.0...
    Clusters that include samples from totally different classes totally
    destroy the homogeneity of the labeling, hence::
      >>> print("%.6f" % v_measure_score([0, 0, 1, 1], [0, 0, 0, 0]))
      0.0...
    """
    return homogeneity_completeness_v_measure(labels_true, labels_pred,
                                              beta=beta)[2]


def homogeneity_completeness_v_measure(labels_true, labels_pred, beta=1.0):
    """Compute the homogeneity and completeness and V-Measure scores at once.
    Those metrics are based on normalized conditional entropy measures of
    the clustering labeling to evaluate given the knowledge of a Ground
    Truth class labels of the same samples.
    A clustering result satisfies homogeneity if all of its clusters
    contain only data points which are members of a single class.
    A clustering result satisfies completeness if all the data points
    that are members of a given class are elements of the same cluster.
    Both scores have positive values between 0.0 and 1.0, larger values
    being desirable.
    Those 3 metrics are independent of the absolute values of the labels:
    a permutation of the class or cluster label values won't change the
    score values in any way.
    V-Measure is furthermore symmetric: swapping ``labels_true`` and
    ``label_pred`` will give the same score. This does not hold for
    homogeneity and completeness. V-Measure is identical to
    :func:`normalized_mutual_info_score` with the arithmetic averaging
    method.
    Read more in the :ref:`User Guide <homogeneity_completeness>`.
    Parameters
    ----------
    labels_true : int array, shape = [n_samples]
        ground truth class labels to be used as a reference
    labels_pred : array-like of shape (n_samples,)
        cluster labels to evaluate
    beta : float
        Ratio of weight attributed to ``homogeneity`` vs ``completeness``.
        If ``beta`` is greater than 1, ``completeness`` is weighted more
        strongly in the calculation. If ``beta`` is less than 1,
        ``homogeneity`` is weighted more strongly.
    Returns
    -------
    homogeneity : float
       score between 0.0 and 1.0. 1.0 stands for perfectly homogeneous labeling
    completeness : float
       score between 0.0 and 1.0. 1.0 stands for perfectly complete labeling
    v_measure : float
        harmonic mean of the first two
    See also
    --------
    homogeneity_score
    completeness_score
    v_measure_score
    """
    labels_true, labels_pred = check_clusterings(labels_true, labels_pred)

    if len(labels_true) == 0:
        return 1.0, 1.0, 1.0

    entropy_C = entropy(labels_true)
    entropy_K = entropy(labels_pred)

    contingency = contingency_matrix(labels_true, labels_pred, sparse=True)
    MI = mutual_info_score(None, None, contingency=contingency)

    homogeneity = MI / (entropy_C) if entropy_C else 1.0
    completeness = MI / (entropy_K) if entropy_K else 1.0

    if homogeneity + completeness == 0.0:
        v_measure_score = 0.0
    else:
        v_measure_score = ((1 + beta) * homogeneity * completeness
                           / (beta * homogeneity + completeness))

    return homogeneity, completeness, v_measure_score


def contingency_matrix(labels_true, labels_pred, eps=None, sparse=False):
    """Build a contingency matrix describing the relationship between labels.
    Parameters
    ----------
    labels_true : int array, shape = [n_samples]
        Ground truth class labels to be used as a reference
    labels_pred : array-like of shape (n_samples,)
        Cluster labels to evaluate
    eps : None or float, optional.
        If a float, that value is added to all values in the contingency
        matrix. This helps to stop NaN propagation.
        If ``None``, nothing is adjusted.
    sparse : boolean, optional.
        If True, return a sparse CSR continency matrix. If ``eps is not None``,
        and ``sparse is True``, will throw ValueError.
        .. versionadded:: 0.18
    Returns
    -------
    contingency : {array-like, sparse}, shape=[n_classes_true, n_classes_pred]
        Matrix :math:`C` such that :math:`C_{i, j}` is the number of samples in
        true class :math:`i` and in predicted class :math:`j`. If
        ``eps is None``, the dtype of this array will be integer. If ``eps`` is
        given, the dtype will be float.
        Will be a ``scipy.sparse.csr_matrix`` if ``sparse=True``.
    """

    if eps is not None and sparse:
        raise ValueError("Cannot set 'eps' when sparse=True")

    classes, class_idx = np.unique(labels_true, return_inverse=True)
    clusters, cluster_idx = np.unique(labels_pred, return_inverse=True)
    n_classes = classes.shape[0]
    n_clusters = clusters.shape[0]
    # Using coo_matrix to accelerate simple histogram calculation,
    # i.e. bins are consecutive integers
    # Currently, coo_matrix is faster than histogram2d for simple cases
    contingency = sp.coo_matrix((np.ones(class_idx.shape[0]),
                                 (class_idx, cluster_idx)),
                                shape=(n_classes, n_clusters),
                                dtype=np.int)
    if sparse:
        contingency = contingency.tocsr()
        contingency.sum_duplicates()
    else:
        contingency = contingency.toarray()
        if eps is not None:
            # don't use += as contingency is integer
            contingency = contingency + eps
    return contingency


def check_clusterings(labels_true, labels_pred):
    """Check that the labels arrays are 1D and of same dimension.
    Parameters
    ----------
    labels_true : array-like of shape (n_samples,)
        The true labels.
    labels_pred : array-like of shape (n_samples,)
        The predicted labels.
    """

    # input checks
    if labels_true.ndim != 1:
        raise ValueError(
            "labels_true must be 1D: shape is %r" % (labels_true.shape,))
    if labels_pred.ndim != 1:
        raise ValueError(
            "labels_pred must be 1D: shape is %r" % (labels_pred.shape,))

    return labels_true, labels_pred


def mutual_info_score(labels_true, labels_pred, contingency=None):
    """Mutual Information between two clusterings.
    The Mutual Information is a measure of the similarity between two labels of
    the same data. Where :math:`|U_i|` is the number of the samples
    in cluster :math:`U_i` and :math:`|V_j|` is the number of the
    samples in cluster :math:`V_j`, the Mutual Information
    between clusterings :math:`U` and :math:`V` is given as:
    .. math::
        MI(U,V)=\\sum_{i=1}^{|U|} \\sum_{j=1}^{|V|} \\frac{|U_i\\cap V_j|}{N}
        \\log\\frac{N|U_i \\cap V_j|}{|U_i||V_j|}
    This metric is independent of the absolute values of the labels:
    a permutation of the class or cluster label values won't change the
    score value in any way.
    This metric is furthermore symmetric: switching ``label_true`` with
    ``label_pred`` will return the same score value. This can be useful to
    measure the agreement of two independent label assignments strategies
    on the same dataset when the real ground truth is not known.
    Read more in the :ref:`User Guide <mutual_info_score>`.
    Parameters
    ----------
    labels_true : int array, shape = [n_samples]
        A clustering of the data into disjoint subsets.
    labels_pred : int array-like of shape (n_samples,)
        A clustering of the data into disjoint subsets.
    contingency : {None, array, sparse matrix}, \
                  shape = [n_classes_true, n_classes_pred]
        A contingency matrix given by the :func:`contingency_matrix` function.
        If value is ``None``, it will be computed, otherwise the given value is
        used, with ``labels_true`` and ``labels_pred`` ignored.
    Returns
    -------
    mi : float
       Mutual information, a non-negative value
    Notes
    -----
    The logarithm used is the natural logarithm (base-e).
    See also
    --------
    adjusted_mutual_info_score: Adjusted against chance Mutual Information
    normalized_mutual_info_score: Normalized Mutual Information
    """
    if contingency is None:
        labels_true, labels_pred = check_clusterings(labels_true, labels_pred)
        contingency = contingency_matrix(labels_true, labels_pred, sparse=True)

    if isinstance(contingency, np.ndarray):
        # For an array
        nzx, nzy = np.nonzero(contingency)
        nz_val = contingency[nzx, nzy]
    elif sp.issparse(contingency):
        # For a sparse matrix
        nzx, nzy, nz_val = sp.find(contingency)
    else:
        raise ValueError("Unsupported type for 'contingency': %s" %
                         type(contingency))

    contingency_sum = contingency.sum()
    pi = np.ravel(contingency.sum(axis=1))
    pj = np.ravel(contingency.sum(axis=0))
    log_contingency_nm = np.log(nz_val)
    contingency_nm = nz_val / contingency_sum
    # Don't need to calculate the full outer product, just for non-zeroes
    outer = (pi.take(nzx).astype(np.int64, copy=False)
             * pj.take(nzy).astype(np.int64, copy=False))
    log_outer = -np.log(outer) + log(pi.sum()) + log(pj.sum())
    mi = (contingency_nm * (log_contingency_nm - log(contingency_sum)) +
          contingency_nm * log_outer)
    return mi.sum()


def entropy(labels):
    """Calculates the entropy for a labeling.
    Parameters
    ----------
    labels : int array, shape = [n_samples]
        The labels
    Notes
    -----
    The logarithm used is the natural logarithm (base-e).
    """
    if len(labels) == 0:
        return 1.0
    label_idx = np.unique(labels, return_inverse=True)[1]
    pi = np.bincount(label_idx).astype(np.float64)
    pi = pi[pi > 0]
    pi_sum = np.sum(pi)
    # log(a / b) should be calculated as log(a) - log(b) for
    # possible loss of precision
    return -np.sum((pi / pi_sum) * (np.log(pi) - log(pi_sum)))
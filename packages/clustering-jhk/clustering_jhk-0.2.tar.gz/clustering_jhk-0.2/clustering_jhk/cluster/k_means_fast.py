import numpy as np


def _centers_dense(X,
                   sample_weight,
                   labels, n_clusters,
                   distances):
    """M step of the K-means EM algorithm
    Computation of cluster centers / means.
    Parameters
    ----------
    X : array-like, shape (n_samples, n_features)
    sample_weight : array-like, shape (n_samples,)
        The weights for each observation in X.
    labels : array of integers, shape (n_samples)
        Current label assignment
    n_clusters : int
        Number of desired clusters
    distances : array-like, shape (n_samples)
        Distance to closest cluster for each sample.
    Returns
    -------
    centers : array, shape (n_clusters, n_features)
        The resulting centers
    """
    ## TODO: add support for CSR input
    n_samples = X.shape[0]
    n_features = X.shape[1]

    centers = np.zeros((n_clusters, n_features))
    weight_in_cluster = np.zeros((n_clusters,))

    for i in range(n_samples):
        c = labels[i]
        weight_in_cluster[c] += sample_weight[i]
    empty_clusters = np.where(weight_in_cluster == 0)[0]
    # maybe also relocate small clusters?

    if len(empty_clusters):
        # find points to reassign empty clusters to
        far_from_centers = distances.argsort()[::-1]

        for i, cluster_id in enumerate(empty_clusters):
            # XXX two relocated clusters could be close to each other
            far_index = far_from_centers[i]
            new_center = X[far_index] * sample_weight[far_index]
            centers[cluster_id] = new_center
            weight_in_cluster[cluster_id] = sample_weight[far_index]

    for i in range(n_samples):
        for j in range(n_features):
            centers[labels[i], j] += X[i, j] * sample_weight[i]

    centers /= weight_in_cluster[:, np.newaxis]

    return centers


def assign_rows_csr(X,
                    X_rows,
                    out_rows,
                    out):
    """Densify selected rows of a CSR matrix into a preallocated array.
    Like out[out_rows] = X[X_rows].toarray() but without copying.
    No-copy supported for both dtype=np.float32 and dtype=np.float64.
    Parameters
    ----------
    X : scipy.sparse.csr_matrix, shape=(n_samples, n_features)
    X_rows : array, dtype=np.intp, shape=n_rows
    out_rows : array, dtype=np.intp, shape=n_rows
    out : array, shape=(arbitrary, n_features)
    """
    data = X.data
    indices = X.indices, indptr = X.indptr

    if X_rows.shape[0] != out_rows.shape[0]:
        raise ValueError("cannot assign %d rows to %d"
                         % (X_rows.shape[0], out_rows.shape[0]))

    out[out_rows] = 0.
    for i in range(X_rows.shape[0]):
        rX = X_rows[i]
        for ind in range(indptr[rX], indptr[rX + 1]):
            j = indices[ind]
            out[out_rows[i], j] = data[ind]


def _centers_sparse(X, sample_weight,
                    labels, n_clusters,
                    distances):
    """M step of the K-means EM algorithm
    Computation of cluster centers / means.
    Parameters
    ----------
    X : scipy.sparse.csr_matrix, shape (n_samples, n_features)
    sample_weight : array-like, shape (n_samples,)
        The weights for each observation in X.
    labels : array of integers, shape (n_samples)
        Current label assignment
    n_clusters : int
        Number of desired clusters
    distances : array-like, shape (n_samples)
        Distance to closest cluster for each sample.
    Returns
    -------
    centers : array, shape (n_clusters, n_features)
        The resulting centers
    """
    n_samples = X.shape[0]
    n_features = X.shape[1]

    data = X.data
    indices = X.indices
    indptr = X.indptr

    centers = np.zeros((n_clusters, n_features))
    weight_in_cluster = np.zeros((n_clusters,))
    for i in range(n_samples):
        c = labels[i]
        weight_in_cluster[c] += sample_weight[i]
    empty_clusters = np.where(weight_in_cluster == 0)[0]
    n_empty_clusters = empty_clusters.shape[0]

    # maybe also relocate small clusters?

    if n_empty_clusters > 0:
        # find points to reassign empty clusters to
        far_from_centers = distances.argsort()[::-1][:n_empty_clusters]

        # XXX two relocated clusters could be close to each other
        assign_rows_csr(X, far_from_centers, empty_clusters, centers)

        for i in range(n_empty_clusters):
            weight_in_cluster[empty_clusters[i]] = 1

    for i in range(labels.shape[0]):
        curr_label = labels[i]
        for ind in range(indptr[i], indptr[i + 1]):
            j = indices[ind]
            centers[curr_label, j] += data[ind] * sample_weight[i]

    centers /= weight_in_cluster[:, np.newaxis]

    return centers
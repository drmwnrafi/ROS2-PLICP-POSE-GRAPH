import numpy as np
import scipy


class PLICP:
    def __init__(
        self, max_iterations=80, outliers_threshold=10, error_convergence=1e-1
    ):
        self.max_iterations = max_iterations
        self.outliers_threshold = outliers_threshold
        self.error_convergence = error_convergence

    def rot(self, theta):
        return np.array(
            [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]]
        ).reshape(2, 2)

    def cauchy_kernel(self, error):
        dist = np.linalg.norm(error, axis=1)
        mask = dist < self.outliers_threshold
        result = np.zeros_like(dist)
        result[mask] = np.log(1.0 + (dist[mask] / self.outliers_threshold**2))
        return result

    def compute_normals(self, points, step=1):
        shifted_plus = np.roll(points, -step, axis=1)
        shifted_minus = np.roll(points, step, axis=1)
        dx = shifted_plus[0] - shifted_minus[0]
        dy = shifted_plus[1] - shifted_minus[1]
        normals = np.stack([-dy, dx], axis=0)
        norms = np.linalg.norm(normals, axis=0)
        normals = normals / norms
        normals[:, 0] = np.array([0, 0])
        normals[:, -1] = np.array([0, 0])
        return normals.T[:, None, :]

    def compute_error(
        self, state, source, target, correspondences, target_normals, kernel_func
    ):
        target_normals_corr = target_normals[correspondences]
        error = np.einsum(
            "ijk,ki->ij",
            target_normals_corr,
            (
                self.rot(state[2]) @ source
                + state[0:2].reshape((2, 1))
                - target[:, correspondences]
            ),
        )
        weight = kernel_func(error)
        normals_x = target_normals_corr[:, 0, 0]
        normals_y = target_normals_corr[:, 0, 1]
        third_component = normals_x * (
            (-source[0, :] * np.sin(state[2])) + (source[1, :] * -np.cos(state[2]))
        ) + normals_y * (
            (source[0, :] * np.cos(state[2])) + (source[1, :] * -np.sin(state[2]))
        )
        J = np.stack((normals_x, normals_y, third_component), axis=-1)[:, np.newaxis, :]
        H = np.sum(
            weight
            * np.einsum(
                "ijk,kjl->ilk",
                J.T,
                J,
            ),
            axis=2,
        )
        g = np.sum(
            weight
            * np.einsum(
                "ijk,kj->ijk",
                J.T,
                error,
            ),
            axis=2,
        )
        chi = (error**2).sum()
        return H, g, chi, error

    def homogeneous_transform(self, state):
        homogeneous_matrix = np.eye(3)
        homogeneous_matrix[:2, :2] = self.rot(state[2])
        homogeneous_matrix[:2, 2] = state[0:2].flatten()
        return homogeneous_matrix

    def run(self, source, target, init_state=None):
        r"""
        Running Iterative Closest Point with point-to-line error metric (PLICP). The algortihm finds the optimal
        transformation given 2 pointclouds (target and source) that minimize the error function :

        \underset{R_{\theta}, t}{\operatorname{arg\,min}} \sum_i \| n_i \cdot (R_{\theta}p_i+t-q_j)\|^2

        where R_{\theta} is a rotation matrix with theta angle, p_i is a point of source pointcloud,
        q_j is a point of target pointcloud.

        Algorithm consist of following steps:
        1. Find the correspondences for each point in source w.r.t target point by using KDTree.
        2. Calculate hessian, gradient, chi^2, and error.
        3. Solve least square problem using Gauss-Newton.
        4. Algorithm iterate until convergence.

        Parameters
        ----------
        source :  array-like with shape (2, N)
                Pointcloud that want to matching
        target : array-like with shape (2, N)
                Pointcloud as a reference for source to matching.
        init_state (optional) : array with shape (3, 1)
                Initial state to transform source points.
        """
        state = np.zeros((3, 1))
        if init_state is not None:
            state = init_state
        source_latest = source
        target_normals = self.compute_normals(target)
        nn = scipy.spatial.cKDTree(target.T)
        for i in range(self.max_iterations):
            # print(f' +++++ Iteration : {i} +++++ ')
            dist, correspondences = nn.query(source_latest.T, k=1)
            H, g, chi, error = self.compute_error(
                state,
                source,
                target,
                correspondences,
                target_normals,
                self.cauchy_kernel,
            )
            delta_state = scipy.linalg.lstsq(
                H, -g, lapack_driver="gelsy", check_finite=False
            )[0]
            state += delta_state
            state[2] = np.arctan2(np.sin(state[2]), np.cos(state[2]))
            rotation = self.rot(state[2])
            source_latest = rotation @ (source) + state[0:2]
            if chi < self.error_convergence:
                break
        return state, correspondences, source_latest

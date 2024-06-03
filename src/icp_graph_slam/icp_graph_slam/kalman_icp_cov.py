import numpy as np

class KalmanICPCov():
    def __init__(self) -> None:
        pass

    def compute_error(self, source, reference, rot, trans, corresp):
        """
        \sigma_m^2 = \frac{1}{N} \Sigma_{i=1}^N ||p_{s,i} - Rp_{r,\phi(i)}-t||^2
        """
        N = len(source[0])
        sum_error = 0
        for i in range(N):
          source_point = np.array([source[0][i], source[1][i]])
          reference_point = np.array([reference[0][corresp[-1][i][1]], reference[1][corresp[-1][i][1]]])
          transformed_ref_point = rot.dot(reference_point) - trans
          sum_error += np.linalg.norm((source_point - transformed_ref_point) ** 2)
        return sum_error / N

    def compute_normal(self, source, coressp):
        """
        n = \frac{p_{s,i}-p_{r,\phi(i)}}{||p_{s,i}-p_{r,\phi(i)}||}
        """
        n = (source - coressp) / np.linalg.norm(source - coressp)
        return n

    def run(self, source, reference, rot, trans, corresp):
        """
        Input :
        source : 2d point cloud
        refernece : target for alignment 2d source pointcoud, format : [[x_1, x_2, x_3, ..., x_n][y_1, y_2, y_3, ..., y_n]
        rot : rotation matrix
        trans : translation vector
        corresp : correspondences in format (reference_point )
        """
        P = np.eye(3) * 1e6
        error = self.compute_error(source, reference, rot, trans, corresp)
        N = len(source[0])
        for i in range(N):
          source_point = np.array([source[0][i], source[1][i]])
          reference_point = np.array([reference[0][corresp[-1][i][1]], reference[1][corresp[-1][i][1]]])
          n = self.compute_normal(source_point, reference_point)
          v = rot.dot(reference_point)
          d_r = np.array([[0, -1], [1, 0]]).dot(v)
          n_x = n[0]
          n_y = n[1]
          H = np.array([[n_x, n_y, d_r @ n]])
          S = H.dot(P).dot(H.T) + error
          K = P.dot(H.T).dot(np.linalg.inv(S))
          P = (np.identity(3) - K.dot(H)).dot(P)
        return P

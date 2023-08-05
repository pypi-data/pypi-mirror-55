import numpy as np


class pyAQN:
    @staticmethod
    def normalize(M):
        nans = np.isnan(M)
        jitteredM = M + np.random.rand(M.shape[0], M.shape[1]) * 0.1
        prctiles = np.nanpercentile(jitteredM, range(0, 100), axis=0)
        binassignments = np.asarray(
            [np.digitize(x, y) for x, y in zip(jitteredM.transpose(), prctiles.transpose())]).transpose()
        qM = np.zeros(M.shape)
        for p in range(0, 100):
            inP = binassignments == p
            qM[inP] = np.nanmedian(jitteredM[inP])
        qM[nans] = np.nan
        return qM, binassignments


"""
class yieldEstimator
    def __init__(data dir)
        weights and volumes saved in dicts with filename as key
        self.weights = load weights from file
        self.volumes = empty {}

    def estimateYield()
        for point cloud file in data_dir
            pointcloud = load point cloud file
            estimateVolume(pointcloud)
        put total volume through model
        return predicted weight

    def estimateVolume(pointcloud)
        remove ground trench points
        bound point cloud
        other data processing...
        estimate volume
        add to self.volumes



"""

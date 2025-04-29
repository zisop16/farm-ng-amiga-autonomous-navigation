import depthai as dai

COLOR = True  # Use color camera of mono camera

# DEPTH CONFIG
lrcheck = True  # Better handling for occlusions
extended = True  # Closer-in minimum depth, disparity range is doubled
subpixel = False  # Better accuracy for longer distance, fractional disparity 32-levels
confidence_threshold = 100  # 0-255, 255 = low confidence, 0 = high confidence
min_range = 10  # mm
max_range = 100  # mm

# Median filter
# Options: MEDIAN_OFF, KERNEL_3x3, KERNEL_5x5, KERNEL_7x7
median = dai.StereoDepthProperties.MedianFilter.KERNEL_7x7

# CALIBRATION
calibration_data_dir = (
    "calibration_data"  # Path to camera extrinsics relative to main.py
)

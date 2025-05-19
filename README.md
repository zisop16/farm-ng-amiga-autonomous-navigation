## 3D Scanning System for Amiga Farm Robot
##     Technical Report

##     Summary
This report documents the development of a 3D scanning system for the Amiga farm robot platform. The system utilizes multiple OAK-D cameras to create aligned 3D point clouds that can be used for crop monitoring, measurement, and analysis. The system integrates with the Amiga's existing track following capabilities to enable automated data collection along predefined paths.

Over the course of development, we created a prototype with basic track following using the track follower and filter services for the Amiga robot. This prototype included the ability to create arbitrary tracks, save them to a directory on the Amiga brain, and then load them to be followed. Additionally, our prototype included a DepthAI camera pipeline that allowed for the capturing and combining of point clouds generated on our cameras.

In subsequent iterations, we implemented a line following feature that allows the robot to walk in straight lines, turn, and walk back, so that it can traverse a field of crops with an arbitrary number of rows. The system provides the ability for the robot to capture images only while it is moving along a given row, and for those point cloud images to be saved to ordered directories. The volume of these captures can then be estimated using an Open3D script and converted to a mass estimate which is displayed on a dedicated page in the app.

System Architecture
Hardware Components
Amiga Farm Robot: Base mobility platform
OAK-D ToF Cameras: Multiple depth cameras positioned at different angles for comprehensive scene capture
Camera Network: Cameras configured with fixed IP addresses (10.95.76.11, 10.95.76.12, 10.95.76.13)
Camera Mounts: Custom mounts to maintain fixed camera positions for consistent image capture
Software Architecture
The system follows a client-server architecture:

Backend (Python):
Camera management and control
Point cloud processing and fusion
Path planning and robot control interface
REST API endpoints for frontend communication
Line following and crop row navigation
Frontend (React):
Track creation and management interface
Camera feeds visualization
Robot control interface
Point cloud alignment and visualization tools
Crop yield estimation display
Key Components
Camera Backend:
Camera class: Manages individual OAK-D cameras, handles camera initialization, depth data processing, and point cloud generation
PointCloudFusion: Aligns and merges point clouds from multiple cameras
OakManager: Coordinates multiple camera operations
Track Management:
Standard track recording and playback system
Line track creation for crop row navigation
Path planning and following functions
Integration with Amiga's control systems
Data Processing Pipeline:
Depth data capture from ToF sensors
RGB data capture from camera modules
Point cloud generation with color information
Multi-camera point cloud registration and fusion
Data storage and export functions
Crop yield estimation from point cloud volume
Technical Implementation Details
Camera Management
The system initializes cameras using the DepthAI API, configuring ToF sensors for optimal depth sensing. Each camera:

Streams RGB video at 5 FPS over HTTP
Captures depth information from the ToF sensor
Processes RGBD data into colored point clouds
Applies calibration data for spatial alignment
python
# Camera pipeline creation
def _create_pipeline(self):
    pipeline = dai.Pipeline()
    
    # Video encoder for streaming
    videoEnc = pipeline.create(dai.node.VideoEncoder)
    videoEnc.setDefaultProfilePreset(FPS, dai.VideoEncoderProperties.Profile.MJPEG)
    
    # ToF depth sensing
    tof = pipeline.create(dai.node.ToF)
    tofConfig = tof.initialConfig.get()
    tofConfig.enableOpticalCorrection = True
    tofConfig.enablePhaseShuffleTemporalFilter = True
    
    # RGB camera setup
    cam_rgb = pipeline.createColorCamera()
    cam_rgb.setBoardSocket(dai.CameraBoardSocket.CAM_C)
    cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_800_P)
    cam_rgb.setFps(FPS)
The camera component was rewritten to run processing directly on the cameras themselves, with streaming servers running as threads instead of processes to improve performance. Camera calibration ensures that point clouds from multiple cameras are properly aligned when combined.

Point Cloud Processing
Point clouds from multiple cameras are processed and aligned using the Open3D library:

python
def align_point_clouds(self):
    voxel_radius = [0.04, 0.02, 0.01]
    max_iter = [50, 30, 14]
    
    master_point_cloud = self.cameras[0].point_cloud
    
    # Align each camera's point cloud to the master
    for camera in self.cameras[1:]:
        for iter, radius in zip(max_iter, voxel_radius):
            # Point cloud downsampling and normal estimation
            target_down = master_point_cloud.voxel_down_sample(radius)
            target_down.estimate_normals(
                o3d.geometry.KDTreeSearchParamHybrid(radius=radius * 2, max_nn=30)
            )
            
            # ICP registration with color information
            result_icp = o3d.pipelines.registration.registration_colored_icp(
                source_down, target_down, radius, camera.point_cloud_alignment,
                o3d.pipelines.registration.TransformationEstimationForColoredICP(),
                o3d.pipelines.registration.ICPConvergenceCriteria(
                    relative_fitness=1e-6, relative_rmse=1e-6, max_iteration=iter
                )
            )
            
            camera.point_cloud_alignment = result_icp.transformation
Robot Movement and Path Planning
The system implements specialized functions for path planning and robot control:

python
def walk_towards(current_pose: Pose3F64, target_position: np.array, goal_counter: int) -> tuple[list[Pose3F64], int]:
    # Calculates a list of poses required to turn the robot in the direction of a target point, 
    # then walk in a perfectly straight line toward that point
    # Returns as a tuple: the list of PoseF364 objects, and the index as an int where the robot STARTS moving straight
    
def create_straight_segment(previous_pose: Pose3F64, distance: float, next_frame_b: str, spacing: float = 0.1) -> list[Pose3F64]:
    # Creates a list of poses in which the robot walks in a direct straight line for a specified distance
    
def create_turn_segment(previous_pose: Pose3F64, angle: float, next_frame_b: str, spacing: float = 0.1) -> list[Pose3F64]:
    # Creates a list of poses in which the robot turns for a specified, signed angle
Line Following for Crop Rows
The line following feature allows the robot to navigate crop rows systematically:

python
# Capturing images during line following
async def handle_image_capture(vars: StateVars, camera_msg_queue: Queue, client: EventClient, 
                               line_name: str, row_indices: list[tuple[int, int]]):
    # Background task that runs while the robot is following a line track
    # Calculates when the robot should stop and take a picture based on its position and waypoint index
    
async def capture_image(camera_msg_queue: Queue, line_name: str, row_number: int, capture_number: int):
    # Informs the camera backend to capture a combined pointcloud image
    # Pauses robot movement for 3 seconds to ensure stable image capture
API Interface
The system provides a comprehensive REST API for frontend communication:

Camera and Point Cloud Management:
/pointcloud/save: Saves the current fused point cloud to disk
/pointcloud/align: Triggers point cloud alignment
/pointcloud/reset: Resets camera alignment parameters
/get_yield/{line_name}: Returns estimated crop yield for the given line track
Track Management:
/list_tracks: Lists available predefined paths
/get_track/{track_name}: Retrieves track data
/delete_track/{track_name}: Deletes a track
/edit_track: Renames a track
Standard Track Recording & Following:
/record/start/{track_name}: Starts recording a new track
/record/stop: Stops the current recording
/follow/start/{track_name}: Begins following a track
/follow/pause: Pauses track following
/follow/stop: Stops track following
Line Following for Crop Rows:
/line/record/start/{track_name}: Begins recording a line track
/line/record/stop: Stops recording a line track
/line/calibrate_turn/start: Begins turn calibration
/line/calibrate_turn/segment: Adds a turn segment
/line/calibrate_turn/end: Completes turn calibration
/line/follow/{line_name}: Follows a line track with specified parameters
Takes JSON body with num_rows and first_turn_right parameters
Data Streaming:
WebSocket /filter_data: Streams live robot position data to the frontend
Frontend User Interface
The React-based UI provides a comprehensive interface organized across multiple components:

Navigation:
Home.tsx: Main application dashboard with navigation options
BackButton.tsx: Navigation control for returning to previous screens
ExitButton.tsx: Application exit control
Track Management:
TrackSelect.tsx: Main interface for track operations
TrackSelectMenu.tsx: Interface for selecting and managing tracks
TrackCreateMenu.tsx: Interface for creating new tracks
TrackRunMenu.tsx: Interface for executing track following operations
Camera Visualization:
CameraFeed.tsx: Displays real-time video from selected camera
Crop Yield Analysis:
ViewCropYield.tsx: Displays crop yield data from scans
TrackYieldInfo.tsx: Detailed yield information display
TrackYieldSelect.tsx: Interface for selecting which yield data to view
User Input:
KeyboardContext.tsx: Provides on-screen keyboard functionality
Calibration & Alignment
The system implements several calibration methods:

Camera Intrinsic Calibration:
Uses factory-calibrated camera parameters from OAK-D
Loads calibration data from device or from stored files
Extrinsic Calibration:
Custom calibration files stored in calibration_data/ directory
Contains transformation matrices as 4x4 numpy arrays
Defines relative positions of cameras in 3D space
ICP-based Point Cloud Registration:
Iterative Closest Point algorithm with color information
Multi-resolution approach for robust alignment
Turn Calibration for Line Following:
Records turn distance for consistent row navigation
Stores calibration in line track configuration files
Data Storage
The system implements a structured data management plan across multiple directories:

Point Cloud Data:
pointclouds/{line_name}/row_{row_number}/capture_{capture_number}/:
Contains combined.ply (fused point cloud from all cameras)
Individual point cloud files per camera
Used for crop volume and yield estimation
Track Data:
tracks/: Standard track files stored as JSON
lines/: Line track files with start/end points and turn parameters
Example: {"start": [-189.05, -7.88], "end": [-189.36, -15.23], "turn_length": 3.15}
Calibration Data:
calibration_data/: Camera calibration matrices
Stores extrinsic parameters for each camera
The point cloud data storage design enables systematic analysis of crop data by organizing captures by line, row, and sequence number.

Deployment
The application is packaged for deployment on the Amiga system:

Python dependencies specified in requirements.txt
React frontend built using Vite
Installation scripts for system integration
Manifest file for Amiga app registration
Performance Considerations
Process-based parallelization for camera management
Downsampling of point clouds for efficient alignment
Optimized ToF sensor configuration for accuracy/performance balance
Streaming servers run as threads instead of processes for improved performance
Asynchronous API for responsive user interface
Crop Yield Analysis
The system includes a complete pipeline for crop yield estimation:

Image capture during line following at specific row positions
Point cloud generation and storage in organized directory structure
Volume estimation from point cloud data using Open3D
Conversion of volume estimates to mass/yield values
Display of yield data in dedicated frontend UI
Key Achievements
Successfully integrated multiple OAK-D cameras with calibrated alignment
Implemented intelligent line following for systematic crop row navigation
Created a comprehensive point cloud capture and processing pipeline
Developed a data storage structure optimized for agricultural analysis
Built a fully functional user interface for robot control and data visualization
Integrated crop yield estimation from point cloud volume measurements
Future Enhancements
Enhanced crop analysis algorithms for species identification
Improved point cloud visualization directly in the frontend
Enhanced calibration workflows with guided procedures
Higher resolution point cloud capture options
Integration with farm management systems for data exchange
Extended yield prediction models based on historical data
Conclusion
The 3D scanning system successfully integrates multiple OAK-D cameras with the Amiga robot platform, providing a comprehensive solution for automated field scanning and crop analysis. The system offers systematic row navigation, precise point cloud capture, and yield estimation capabilities. The modular architecture allows for future extensions and improvements while maintaining compatibility with the existing Amiga ecosystem.

Repository
The complete project code is available at: https://github.com/zisop16/farm-ng-amiga-autonomous-navigation/


#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import torch
import cv2
import numpy as np
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
import tf
from tf.transformations import quaternion_from_euler, euler_from_quaternion
import time
import math
import sys
import pickle

# Initialize ROS node
rospy.init_node('yolo_3d_localization', anonymous=True)
robot = sys.argv[1]

# Initialize CvBridge to convert ROS Image messages to OpenCV images
bridge = CvBridge()

# Load YOLOv5 model (you can use different YOLO model versions)
model = torch.hub.load('ultralytics/yolov5', 'yolov5n')  # Use yolov5x for better accuracy

# Initialize publisher for 3D markers
marker_pub = rospy.Publisher('yolo_3d_marker', Marker, queue_size=10)
t = tf.TransformListener()
# Initialize TF broadcaster
tf_broadcaster = tf.TransformBroadcaster()

# Global depth image
depth_img = None

# Camera intrinsic parameters (example values; adjust as per your setup)
fx = 1206.89
fy = 1206.89
cx = 960.5
cy = 540.5
max_depth_threshold = 10.0  # Maximum depth threshold (in meters)
database = {}


def rgb_callback(msg):
    rgb_image = bridge.imgmsg_to_cv2(msg, "rgb8")
    process_rgb_image(rgb_image)
    time.sleep(1)

def depth_callback(msg):
    global depth_img
    depth_img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
    time.sleep(1)

def process_rgb_image(rgb_image):
    # Use YOLO to process the RGB image
    results = model(rgb_image)
    results.print()
    boxes = results.xyxy[0].cpu().numpy()  # Get bounding boxes in xyxy format
    process_bounding_boxes(boxes)

def process_bounding_boxes(boxes):
    if depth_img is None:
        rospy.logwarn("Depth image not received yet.")
        return

    marker_id = 0  # Unique marker ID for RViz
    for box in boxes:
        x1, y1, x2, y2 = box[:4]
        #print(box)
        class_id = int(box[5])  # Class ID for the detected object
        label = model.names[class_id]  # Get the label for the object
        if label != "fire hydrant" and label != "table":
            continue
        depth_value = get_average_depth(x1, y1, x2, y2)
        if depth_value is None:
            continue
        xyz = get_3d_coordinates((x1 + x2) / 2, (y1 + y2) / 2, depth_value)
        if xyz is None:
            continue
        #publish_3d_marker(xyz, label, marker_id)
        publish_tf(xyz, label, marker_id)
        marker_id += 1  # Increment marker ID

def get_average_depth(x1, y1, x2, y2):
    if depth_img is None:
        rospy.logwarn("Depth image not available for depth calculation.")
        return None

    # Extract depth values for the bounding box
    depth_region = depth_img[int(y1):int(y2), int(x1):int(x2)]
    avg_depth = np.nanmean(depth_region)  # Handle NaN values

    # Validate depth
    if np.isnan(avg_depth) or avg_depth <= 0 or avg_depth > max_depth_threshold:
        rospy.logwarn(f"Invalid depth value: {avg_depth}")
        return None
    return avg_depth

def get_3d_coordinates(x, y, depth):
    try:
        X = (x - cx) * depth / fx
        Y = (y - cy) * depth / fy
        Z = depth
        return (X, Y, Z)
    except Exception as e:
        rospy.logerr(f"Error computing 3D coordinates: {e}")
        return None

def publish_3d_marker(xyz, label, marker_id):
    marker = Marker()
    marker.header.frame_id = f"/{robot}_tf/camera_link"
    marker.header.stamp = rospy.Time.now()
    marker.ns = "yolo_3d_localization"
    marker.id = marker_id  # Assign unique ID
    marker.type = Marker.SPHERE
    marker.action = Marker.ADD
    marker.pose.position = Point(xyz[0], xyz[1], xyz[2])
    marker.scale.x = 0.1
    marker.scale.y = 0.1
    marker.scale.z = 0.1
    marker.color.a = 1.0
    marker.color.r = 1.0
    marker.color.g = 0.0
    marker.color.b = 0.0

    rospy.loginfo(f"Publishing marker at {xyz} for {label}")
    marker_pub.publish(marker)

def publish_tf(xyz, label, marker_id):
    x, y, z = xyz

    # Frame name must not contain invalid characters
    object_frame = f"{label}_frame"
    
    
#    print(x, y, z)
#    print(f"distance: {xyz}, yaw: {yaw}")
#    x = z*math.cos(yaw)
#    y = z*math.sin(yaw)
#    z = 0

    # Define rotation (identity quaternion)
    rotation = quaternion_from_euler(0, 0, 0)

    # Publish the transform for the object
    tf_broadcaster.sendTransform(
        (z, -x, -y),   # Position
        rotation,    # Rotation
        rospy.Time.now(),
        object_frame,  # Name of the child frame
        f"/{robot}_tf/camera_link"  # Parent frame
    )
    coords = t.lookupTransform(f"/{robot}_tf/map", f"{label}_frame", rospy.Time())[0]
    if label in database:
        database[label].append([coords[0], coords[1]])
    else:
        database[label] = []
        database[label].append([coords[0], coords[1]])
    with open(f"/home/adhi/catkin_ws/src/multiple_turtlebot3/{robot}", "wb") as f:
        pickle.dump(database, f)

#    rospy.loginfo(f"Published transform for {label} at ({z}, {y}, {x})")

def main():
    rospy.Subscriber(f'/{robot}/camera/rgb/image_raw', Image, rgb_callback)
    rospy.Subscriber(f'/{robot}/camera/depth/image_raw', Image, depth_callback)

    rospy.loginfo("YOLO 3D localization node started.")
    rospy.spin()

if __name__ == '__main__':
    main()


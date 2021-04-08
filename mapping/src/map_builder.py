#! /usr/bin/env python

import rospy
import numpy
import math
import tf
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import PoseWithCovarianceStamped

# initialize node
rospy.init_node('laser_to_occupancy_grid_node')

# Initialize occupancy grid message
map_msg = OccupancyGrid()
map_msg.header.frame_id = 'map'
resolution = 0.01
width = 500
height = 500

# Actual laser
laser_msg = LaserScan()

# Initialize turtle pose relative to world
init_pos, init_quat = None, None
position, quaternion = None, None

# square size of the turtle footprint [m]
footprint = 0.1

# Map update rate (defaulted to 5 Hz)
rate = 5.0

# Range data
turtle_range = None

def callback_range(msg):
    # callback for lidar range
    global turtle_range, laser_msg

    clean_ranges = [(None, None)] * len(msg.ranges)

    for i, r in enumerate(msg.ranges):
        if msg.range_min < r < msg.range_max:
            angle = msg.angle_min + i * msg.angle_increment
            clean_ranges[i] = (angle, msg.ranges[i])

    turtle_range = clean_ranges

    # Build shifted laser.
    laser_msg = msg
    ranges = [0] * len(laser_msg.ranges)
    for i in range(len(laser_msg.ranges)):
        angle = msg.angle_min + i * msg.angle_increment
        ranges[i] = laser_msg.ranges[i]

    laser_msg.ranges = tuple(ranges)
    laser_msg.angle_min += math.pi/2
    laser_msg.header.frame_id = "actual_laser"


def callback_pos(msg):
    # callback for position estimation using ekf
    global position, quaternion

    position = msg.pose.pose.position
    quaternion = msg.pose.pose.orientation

def callback_init(msg):
    global init_pos, init_quat

    init_pos = msg.pose.pose.position
    init_quat = msg.pose.pose.orientation

def set_obstacle_cells(grid, position, orientation, turtle_range):
    global resolution

    if position is not None and orientation is not None:
        off_x = position.x // resolution + width  // 2 + init_pos.x
        off_y = position.y // resolution + height // 2 + init_pos.y

        explicit_quat = [orientation.x, orientation.y, orientation.z, orientation.w]
        _, _, yaw = tf.transformations.euler_from_quaternion(explicit_quat)
        _, _, yaw_init = tf.transformations.euler_from_quaternion([init_quat.x, init_quat.y, init_quat.z, init_quat.w])

        if turtle_range is not None:
            for angle_offset, r in turtle_range:
                if r is not None:
                    theta = yaw + angle_offset + yaw_init

                    obstacle_x = (r / resolution) * numpy.cos(theta) + off_x
                    obstacle_y = (r / resolution) * numpy.sin(theta) + off_y
                    obstacle = numpy.array([obstacle_x, obstacle_y])

                    # rospy.loginfo("FOUND OBSTACLE AT: x:%f y:%f", obstacle[0], obstacle[1])

                    # set probability of occupancy to 100 and neighbour cells to 50
                    grid[int(obstacle[0]), int(obstacle[1])] = int(100)
                    if  grid[int(obstacle[0]+1), int(obstacle[1])]   < int(1):
                        grid[int(obstacle[0]+1), int(obstacle[1])]   = int(50)
                    if  grid[int(obstacle[0]), 	 int(obstacle[1]+1)] < int(1):
                        grid[int(obstacle[0]),   int(obstacle[1]+1)] = int(50)
                    if  grid[int(obstacle[0]-1), int(obstacle[1])]   < int(1):
                        grid[int(obstacle[0]-1), int(obstacle[1])]   = int(50)
                    if  grid[int(obstacle[0]),   int(obstacle[1]-1)] < int(1):
                        grid[int(obstacle[0]),   int(obstacle[1]-1)] = int(50)

                    decrement = 0.01
                    free_x = ((r - decrement) / resolution) * numpy.cos(theta) + off_x
                    free_y = ((r - decrement) / resolution) * numpy.sin(theta) + off_y
                    free_cell = numpy.array([free_x, free_y])

                    while r >= decrement and grid[int(free_cell[0]), int(free_cell[1])] != int(1):
                        grid[int(free_cell[0]), int(free_cell[1])] = int(0)
                        free_x = ((r - decrement) / resolution) * numpy.cos(theta) + off_x
                        free_y = ((r - decrement) / resolution) * numpy.sin(theta) + off_y
                        free_cell = numpy.array([free_x, free_y])
                        decrement += 0.01


# Subscribers
range_sub = rospy.Subscriber("/scan", LaserScan, callback_range)
pos_ekf_sub = rospy.Subscriber("/robot_pose_ekf/odom_combined", PoseWithCovarianceStamped, callback_pos)
init_pos = rospy.Subscriber("/initialpose", PoseWithCovarianceStamped, callback_init)

# Publishers
occ_pub = rospy.Publisher("/map", OccupancyGrid, queue_size = 10)
actual_laser = rospy.Publisher("/actual_laser", LaserScan, queue_size = 10)


# main function
if __name__ == '__main__':
    # set grid parameters
    if rospy.has_param("occupancy_rate"):
        rate = rospy.get_param("occupancy_rate")

    if rospy.has_param("grid_resolution"):
        resolution = rospy.get_param("grid_resolution")

    if rospy.has_param("grid_width"):
        width = rospy.get_param("grid_width")

    if rospy.has_param("grid_height"):
        height = rospy.get_param("grid_height")

    # fill map_msg with the parameters from launchfile
    map_msg.info.resolution = resolution
    map_msg.info.width = width
    map_msg.info.height = height
    map_msg.data = [None] * (width*height)

    # initialize grid with -1 (unknown)
    grid = numpy.ndarray((width, height), buffer=numpy.zeros((width, height), dtype=numpy.int),
             dtype=numpy.int)
    grid.fill(-1)

    # set map origin [meters]
    map_msg.info.origin.position.x = - width // 2 * resolution
    map_msg.info.origin.position.y = - height // 2 * resolution

    loop_rate = rospy.Rate(rate)

    while not rospy.is_shutdown():
        if init_pos is None or init_quat is None:
            continue

        set_obstacle_cells(grid, position, quaternion, turtle_range)

        # stamp current ros time to the message
        map_msg.header.stamp = rospy.Time.now()

        # build ros map message and publish
        for i in range(width*height):
            map_msg.data[i] = grid.flat[i]

        occ_pub.publish(map_msg)
        actual_laser.publish(laser_msg)

        loop_rate.sleep()

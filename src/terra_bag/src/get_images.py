#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2016 Massachusetts Institute of Technology

"""Extract images from a rosbag.
"""

import argparse
import os

import pudb

import cv2
import rosbag
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from tf.transformations import euler_from_quaternion


def main():
    """Extract a folder of images from a rosbag.
    """
    parser = argparse.ArgumentParser(description="Extract images from a ROS bag.")
    parser.add_argument("bag_file", help="Input ROS bag.")
    parser.add_argument("output_dir", help="Output directory.")
    parser.add_argument("image_topic", help="Image topic.")
    parser.add_argument("odom_topic", help="Odom topic yo")

    args = parser.parse_args()

    print("Extract images from %s on topic %s into %s" % (args.bag_file,
                                                          args.image_topic, args.output_dir))

    bag = rosbag.Bag(args.bag_file, "r")
    bridge = CvBridge()
    file_count = 0
    flag = 0
    count = 0
    #read_messages unfortunately does not give you the msg-topics at the same time, you have to iterate to get the next messages, so thats why this is spaghetti
    #This part gets the image data and then odom data on the next pass and saves everything in a format for the topological map stuff
    for topic, msg, t in bag.read_messages(topics=[args.odom_topic, args.image_topic]):
        if topic != args.odom_topic:
            flag = 1#Get next odom
            cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
            cv_img = cv2.resize(cv_img, dsize=(64, 64), interpolation=cv2.INTER_CUBIC)

            cv2.imwrite(os.path.join(args.output_dir, "%05i.tiff" % count), cv_img)
            print("Wrote image %i" % count)

            count += 1
            continue
        if flag == 1:
            position = msg.pose.pose.position
            #orientation is quaternion
            orientation = msg.pose.pose.orientation
            #euler in form of RPY
            euler_rotation = euler_from_quaternion([orientation.x, orientation.y, orientation.z, orientation.w])
            yaw = euler_rotation[2]
            print_string = "heading: " + str(yaw) + "\npos:\n" + "- " + str(position.x) + "\n- " + str(position.y)
            file_name = str(file_count).zfill(5) + ".yaml"
            file_count += 1
            f = open(os.path.join(args.output_dir, file_name), 'w')
            f.write(print_string)
            f.close()
            flag = 0

    bag.close()

    return

if __name__ == '__main__':
    main()

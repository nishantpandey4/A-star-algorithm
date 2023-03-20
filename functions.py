#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENPM 661
Project 3-a

@authors: Rishikesh Jadhav (UID: 119256534) and Nishant Pandey (UID: 119247556)

"""
# ---------------------------------------------------------------------------------
# IMPORTING PACKAGES
# ---------------------------------------------------------------------------------

import numpy as np
from queue import PriorityQueue
import cv2
from cv2 import VideoWriter, VideoWriter_fourcc 
import Node
import math

# ---------------------------------------------------------------------------------
# FUNCTION DEFINITIONS
# ---------------------------------------------------------------------------------

def line(p1, p2, x, y, t):
    """
    Constructs a line passing through two points and calculates the distance of a given point from the line. 

    Parameters
    ----------
    p1 : Array
        Coordinates of point 1.
    p2 : Array
        Coordinates of point 2.
    x : double
        x-coordinate of point of interest.
    y : double
        y-coordinate of point of interest..
    t : double
        offset from line for provided clearance.

    Returns
    -------
    d : double
        Distance of point from line along with the sign indicating direction.

    """
    
    m = (p2[1] - p1[1]) / ( p2[0] - p1[0])
    d = m * (x - p1[0]) + (p1[1] + (t * math.sqrt((m ** 2) + 1)) - y)

    
    return d



#Edit this according to map

def isObstacle(point,c,r):
    """
    Checks whether the point collides with an obstacle.

    Parameters
    ----------
    point : Array
        Point coordinates.
    c: int
        Clearance.
    r: int
        Robot radius.    

    Returns
    -------
    flag : bool
        True if point coincides with an obstacle, false otherwise.

    """
    
    flag = False

    t = r + c                                   # Total clearance
    i = point[0]
    j = point[1]
    
    # Hexagonal Obastacle
    if (i > (235.05-t) and i < (364.95+t) and line((235.05,87.5),(300,50),i,j,t) < 0 
        and line((300,50),(364.95,87.5),i,j,t) < 0 
        and line((235.05,162.5),(300,200),i,j,t) > 0 
        and line((300,200),(364.95,162.5),i,j,t) > 0):
        flag = True

    # lower rectangle obstacle
    if (i > (100-t) and i < (150+t) and line((100,150),(150,150),i,j,t) < 0 
        and line((100,250),(150,250),i,j,t) > 0):
        flag = True
                
    

    # upper rectangle obstacle
    if (i > (100-t) and i < (150+t) and line((100,0),(150,0),i,j,t) < 0 
        and line((100,100),(150,100),i,j,t) > 0):
        flag = True

    # Iscoceles triangle obstacle
    if (i>(460-t)and i<(510+t)and j>(25) and j< (225+2*t) and line((460,225),(510,125),i,j,t) > 0
        and line((460,25),(510,125),i,j,t) < 0):
        flag = True


    # Boundaries condition of the map extremities so that obstacles are not there.
    if (i > 0 and i < c):
        flag = True
    if (i < 600 and i > (600-c)):
        flag = True
    if (j > 0 and j < t):
        flag = True
    if (j < 250 and j >(250 - c)):
        flag = True    

    return flag

def create_map(c,r):
    """
    Creates the given map in a numpy array.

    Parameters
    ----------
    c : int
        Clearance.
    r : int
        Robot radius.

    Returns
    -------
    map: 2D Array
        Created map.

    """
    map_ = np.zeros((250,600))
   
    for i in range(map_.shape[1]):
        for j in range(map_.shape[0]):
            if isObstacle((i,j), c, r):
                map_[j][i] = 1    
    
    return map_
def s_node(c,r):
    # """
    # Gets the start node from the user.

    # Returns
    # -------
    # start_node : Array
    #     Coordinates of start node.

    # """
    
    flag = False
    while not flag:
        start_node = [int(item) for item in input("\n Please enter the start node: ").split(',')]
        start_node[1] = 250 - start_node[1]

        if (start_node[2] > 360):
            start_node[2] = start_node[2] % 360

        # check 1 - range of map
        if (len(start_node) == 3 and (0 <= start_node[0] <= 600) and (0 <= start_node[1] <= 250)):
        # check 2 - obstacle collision?
            if not isObstacle(start_node,c,r):
                flag = True
            else:   
                print("Start node collides with obstacle \n")
        else:
            print("The input node location does not exist in the map, please enter a valid start node.\n")
            flag = False
      
    return start_node


def g_node(c,r):
    """
    Gets the goal node from the user.

    Returns
    -------
    goal_node : Array
        Coordinates of goal node.

    """
    
    flag = False
    while not flag:
        goal_node = [int(item) for item in input("\n Please enter the goal node: ").split(',')]
        goal_node[1] = 250 - goal_node[1]
        
        # check 1 - angle out of range?  
        if (goal_node[2] > 360):
            goal_node[2] = goal_node[2] % 360

        # check 1 - range of map       
        if (len(goal_node) == 3 and (0 <= goal_node[0] <= 600) and (0 <= goal_node[1] <= 250)):
        # check 2 - obstacle collision?
            if not isObstacle(goal_node,c,r):
                flag = True
            else:
                print("Goal node collides with obstacle \n")
        else:
            print("The input node location does not exist in the map, please enter a valid goal node.\n")
            flag = False
        
    return goal_node
def take_input():
    """
    Takes the required parameter data from user.

    Returns
    -------
    clearance : int
        Clearance.
    radius : int
        Robot radius.
    StepSize : int
        Stride.
    angle : int
        Angle step-size.

    """
    
    clearance, radius = [int(item) for item in input("\n Please enter the clearance and robot radius (comma seperated values): ").split(',')]
    flag = False
    while not flag:     
        StepSize = int(input("\n Please enter the step size: "))
        if (1 <= StepSize <= 10):
            flag = True
        else:
            print("\n Enter step size in range [1,10].")
    angle = int(input("\n Please enter angle between movements: "))
    
    return clearance, radius, StepSize, angle


def cal_dis(current, goal):
    """
    Calculates Euclidian diatance between two nodes.

    Parameters
    ----------
    current : Array
        Source node.
    goal : Array
        Destination node.

    Returns
    -------
    cost : double
        Distance between the two nodes.

    """
    
    cost=0.0
    if current is not None:
        cost=np.sqrt((current[0]-goal[0])**2 + (current[1]-goal[1])**2)
    
    return cost
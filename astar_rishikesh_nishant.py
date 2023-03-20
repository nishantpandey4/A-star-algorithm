#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENPM 661
Project 3-a

@authors: Rishikesh Jadhav (UID: 119256534) and Nishant Pandey (UID: 119247556)
github link: https://github.com/nishantpandey4/project3a_nishant_rishikesh.git
"""

from functions import *


user_guide()

clearance, radius, StepSize, angle = take_input()

map_ = create_map(clearance, radius)

start_node = s_node(clearance, radius)
goal_node = g_node(clearance, radius)

# nodes = Dijkstra(start_node, goal_node, map)

nodes = algorithm(start_node, goal_node, map_, clearance, radius, StepSize, angle)

node_objects, path = backtracking(nodes, goal_node)

make_video(node_objects, path, map_)


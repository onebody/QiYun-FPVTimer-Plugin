"""RotorHazard FPVTimer Data server script"""

RELEASE_VERSION = "0.3"  # Public release version code
SERVER_API = 10  # Server API version
JSON_API = 3  # JSON API version
MIN_PYTHON_MAJOR_VERSION = 3  # minimum python version (3.8)
MIN_PYTHON_MINOR_VERSION = 8

import logging
import log
from datetime import datetime
from time import monotonic
import socket
import random
import string
import json

import io
import os
import sys
import base64

APP = Flask(__name__, static_url_path="/static")


# author by:onebody
# author_uri: "https://github.com/onebody",
# 
@APP.route("/runone/node/<int:node_id>")
def render_runone_node(node_id):
    """比赛时单独节点 显示页面"""
    frequencies = [node.frequency for node in RaceContext.interface.nodes]
    nodes = []
    for idx, freq in enumerate(frequencies):
        if freq:
            nodes.append({"freq": freq, "index": idx})

    return render_template(
        "runone.html",
        serverInfo=RaceContext.serverstate.template_info_dict,
        getOption=RaceContext.rhdata.get_option,
        __=__,
        led_enabled=(
            RaceContext.led_manager.isEnabled()
            or (RaceContext.cluster and RaceContext.cluster.hasRecEventsSecondaries())
        ),
        vrx_enabled=RaceContext.vrx_manager.isEnabled(),
        num_nodes=RaceContext.race.num_nodes,
        nodes=nodes,
        node_id=node_id - 1,
        cluster_has_secondaries=(
            RaceContext.cluster and RaceContext.cluster.hasSecondaries()
        ),
    )

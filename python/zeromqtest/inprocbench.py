# -*- coding: utf-8 -*-

import zmq
from zmq.devices import ThreadDevice

inproc_transport = "inproc://test"

cxt = ThreadDevice.context_factory()
td = ThreadDevice(zmq.QUEUE, zmq.REP, zmq.REQ)
td.bind_in(inproc_transport)
td.connect_out(inproc_transport)
td.start()


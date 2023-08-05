#!/usr/bin/env python3

"""
picast - a simple wireless display receiver for Raspberry Pi

    Copyright (C) 2019 Hiroshi Miura
    Copyright (C) 2018 Hsun-Wei Cho

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import errno
import fcntl
import os
import re
import socket
from logging import getLogger
from time import sleep

from .discovery import ServiceDiscovery
from .player import GstPlayer
from .settings import Settings
from .video import WfdVideoParameters


class PiCast:

    def __init__(self, window):
        self.logger = getLogger("PiCast")
        self.window = window
        self.player = GstPlayer()
        self.watchdog = 0
        self.csnum = 0

    def rtsp_response_header(self, cmd=None, url=None, res=None, seq=None, others=None):
        if cmd is not None:
            msg = "{0:s} {1:s} RTSP/1.0".format(cmd, url)
        else:
            msg = "RTSP/1.0"
        if res is not None:
            msg += ' {0:s}\r\nCSeq: {1:d}\r\n'.format(res, seq)
        else:
            msg += '\r\nCSeq: {0:d}\r\n'.format(seq)
        if others is not None:
            for k, v in others:
                msg += '{}: {}\r\n'.format(k, v)
        msg += '\r\n'
        return msg

    def cast_seq_m1(self, sock):
        logger = getLogger("PiCast.m1")
        data = (sock.recv(1000))  # RTSP OPTIONS message
        logger.debug("<-{}".format(data))
        s_data = self.rtsp_response_header(seq=1, others=[("Public", "org.wfs.wfd1.0, SET_PARAMETER, GET_PARAMETER")])
        logger.debug("->{}".format(s_data))
        sock.sendall(s_data.encode("UTF-8"))

    def cast_seq_m2(self, sock):
        logger = getLogger("PiCast.m2")
        s_data = self.rtsp_response_header(seq=100, others=[('Require', 'org.wfs.wfd1.0')])
        logger.debug("<-{}".format(s_data))
        sock.sendall(s_data.encode("UTF-8"))
        data = (sock.recv(1000))
        logger.debug("->{}".format(data))

    def cast_seq_m3(self, sock):
        logger = getLogger("PiCast.m3")
        data = (sock.recv(1000))
        logger.debug("->{}".format(data))
        msg = "wfd_client_rtp_ports: RTP/AVP/UDP;unicast {} 0 mode=play\r\n".format(Settings.rtp_port)\
              + WfdVideoParameters().get_video_parameter()
        m3resp = self.rtsp_response_header(seq=2,
                                           others=[('Content-Type', 'text/parameters'),
                                                   ('Content-Length', len(msg))
                                                   ])
        m3resp += msg
        logger.debug("<-{}".format(m3resp))
        sock.sendall(m3resp.encode("UTF-8"))

    def cast_seq_m4(self, sock):
        logger = getLogger("PiCast.m4")
        data = (sock.recv(1000)).decode("UTF-8")
        logger.debug("->{}".format(data))
        s_data = self.rtsp_response_header(res="200 OK", seq=3)
        logger.debug("<-{}".format(s_data))
        sock.sendall(s_data.encode("UTF-8"))

    def cast_seq_m5(self, sock):
        logger = getLogger("PiCast.m5")
        data = (sock.recv(1000))
        logger.debug("->{}".format(data))  # wfd-triggered-method
        s_data = self.rtsp_response_header(res="200 OK", seq=4)
        logger.debug("<-{}".format(s_data))
        sock.sendall(s_data.encode("UTF-8"))

    def cast_seq_m6(self, sock):
        logger = getLogger("PiCast.m6")
        m6req = self.rtsp_response_header(cmd="SETUP",
                                          url="rtsp://{0:s}/wfd1.0/streamid=0".format(Settings.peeraddress),
                                          seq=101,
                                          others=[
                                              ('Transport',
                                               'RTP/AVP/UDP;unicast;client_port={0:d}'.format(Settings.rtp_port))
                                          ])
        logger.debug("<-{}".format(m6req))
        sock.sendall(m6req.encode("UTF-8"))
        data = (sock.recv(1000))
        logger.debug("->{}".format(data))
        paralist = data.decode("UTF-8").split(';')
        serverport = [x for x in paralist if 'server_port=' in x]
        logger.debug("server port {}".format(serverport))
        serverport = serverport[-1]
        serverport = serverport[12:17]
        logger.debug("server port {}".format(serverport))
        paralist = data.decode("UTF-8").split()
        position = paralist.index('Session:') + 1
        sessionid = paralist[position]
        return sessionid

    def cast_seq_m7(self, sock, sessionid):
        logger = getLogger("PiCast.m7")
        m7req = self.rtsp_response_header(cmd='PLAY',
                                          url='rtsp://{0:s}/wfd1.0/streamid=0 RTSP/1.0'.format(Settings.peeraddress),
                                          seq=102,
                                          others=[('Session', sessionid)])
        logger.debug("<-{}".format(m7req))
        sock.sendall(m7req.encode("UTF-8"))
        data = (sock.recv(1000))
        logger.debug("->{}".format(data))

    def handle_recv_err(self, e, sock, idrsock, csnum):
        logger = getLogger("PiCast.daemon.error")
        err = e.args[0]
        if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
            try:
                (idrsock.recv(1000))
            except socket.error as e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    sleep(0.01)
                    self.watchdog += 1
                    if self.watchdog >= 70 / 0.01:
                        self.player.stop()
                        sleep(1)
                else:
                    logger.debug("socket error.")
            else:
                csnum = csnum + 1
                msg = 'wfd-idr-request\r\n'
                idrreq = self.rtsp_response_header(seq=csnum,
                                                   cmd="SET_PARAMETER", url="rtsp://localhost/wfd1.0",
                                                   others=[
                                                       ('Content-Length', len(msg)),
                                                       ('Content-Type', 'text/parameters')
                                                   ])
                idrreq += msg
                logger.debug("idreq: {}".format(idrreq))
                sock.sendall(idrreq.encode("UTF-8"))
        else:
            logger.debug("Exit becuase of socket error.")
        return csnum

    def negotiate(self, conn):
        logger = getLogger("Picast.daemon")
        logger.debug("---- Start negotiation ----")
        self.cast_seq_m1(conn)
        self.cast_seq_m2(conn)
        self.cast_seq_m3(conn)
        self.cast_seq_m4(conn)
        self.cast_seq_m5(conn)
        sessionid = self.cast_seq_m6(conn)
        self.cast_seq_m7(conn, sessionid)
        logger.debug("---- Negotiation successful ----")
        return True

    def rtspsrv(self, conn, idrsock):
        logger = getLogger("PiCast.rtspsrv")
        fcntl.fcntl(conn, fcntl.F_SETFL, os.O_NONBLOCK)
        fcntl.fcntl(idrsock, fcntl.F_SETFL, os.O_NONBLOCK)
        csnum = 102
        while True:
            try:
                data = (conn.recv(1000)).decode("UTF-8")
            except socket.error as e:
                watchdog, csnum = self.handle_recv_err(e, conn, idrsock, csnum)
            else:
                logger.debug("->{}".format(data))
                self.watchdog = 0
                if len(data) == 0 or 'wfd_trigger_method: TEARDOWN' in data:
                    self.player.stop()
                    sleep(1)
                    break
                elif 'wfd_video_formats' in data:
                    logger.info('start player')
                    self.player.start()
                messagelist = data.splitlines()
                singlemessagelist = [x for x in messagelist if ('GET_PARAMETER' in x or 'SET_PARAMETER' in x)]
                logger.debug(singlemessagelist)
                for singlemessage in singlemessagelist:
                    entrylist = singlemessage.splitlines()
                    for entry in entrylist:
                        if re.match(r'CSeq:', entry):
                            cseq = entry.rstrip()
                            resp = self.rtsp_response_header(seq=cseq, res="200 OK")
                            logger.debug("<-{}".format(resp))
                            conn.sendall(resp.encode("UTF-8"))
                            continue

    def connect(self, sock, remote, port):
        max_trial = 1000
        for _ in range(max_trial):
            try:
                sock.connect(remote, port)
            except Exception:
                pass
            else:
                return True
        return False

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sd = ServiceDiscovery()
            sd.register()
            while self.connect(sock, Settings.peeraddress, Settings.rtsp_port):
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as idrsock:
                    idrsock_address = ('127.0.0.1', 0)
                    idrsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    idrsock.bind(idrsock_address)
                    addr, idrsockport = idrsock.getsockname()
                    self.idrsockport = str(idrsockport)
                    if self.negotiate(sock):
                        self.rtspsrv(sock, idrsock)

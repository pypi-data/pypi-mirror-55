#!/usr/bin/python3
"""Fix stdlib asyncio streams to support half-closed Gnutls transports"""
#TODO: report the bug to bpo

import warnings

import asyncio.streams

_ORIG = "_aio_gnutls_transport_orig_connection_made"

def connection_made(self, transport):
    getattr(self, _ORIG)(transport)
    self._over_ssl = not transport.can_write_eof()

def _patch(name):
    cls = getattr(asyncio.streams, name, None)
    if cls is None or hasattr(cls, _ORIG):
        return
    setattr(cls, _ORIG, getattr(cls, "connection_made"))
    setattr(cls, "connection_made", connection_made)

_patch("StreamReaderProtocol")
_patch("_BaseStreamProtocol")


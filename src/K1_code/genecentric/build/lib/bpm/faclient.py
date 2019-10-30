"""
A client class for the FuncAssociate web service at

http://llama.mshri.on.ca/cgi/funcassociate/serv

The documentation of the FuncAssociate API may be found at

http://llama.mshri.on.ca/funcassociate/doc


COPYRIGHT AND LICENSE

Copyright (c) 2010, President and Fellows of Harvard College and
Gabriel Berriz gberriz@hms.harvard.edu.  All rights reserved.

This module is distributed as "The Program" under the Harvard
University End-User License Agreement.
http://llama.mshri.on.ca/license.html.
"""

# -*- mode: python -*-
################################################################
# funcassociate/client.py
#
# Copyright (c) 2010 President and Fellows of Harvard College
# and Gabriel F. Berriz (gberriz@hms.harvard.edu).  All rights
# reserved.
################################################################

import re
import signal
import socket
from inspect import getargspec

import httplib

import json

# -----------------------------------------------------------------------------

DEFAULT_SERVICE_HOST = 'http://llama.mshri.on.ca'
DEFAULT_SERVICE_URL = '/cgi/funcassociate/serv'

# -----------------------------------------------------------------------------

class ServiceError(Exception):
    """
    Exception raised when the response from server includes a non-null
    error.
    """

class NetworkError(ServiceError):
    """
    Exception raised when server fails to respond to a ping request.
    """
    
class TimeoutError(ServiceError):
    """
    Exception raised when response from the server fails to arrive
    within the prescribed time interval.
    """

class InputError(Exception):
    """
    Exception raised by functionate method upon detecting bad inputs
    from user.
    """

class _fc(object):
    host = DEFAULT_SERVICE_HOST
    url = DEFAULT_SERVICE_URL
    headers = {
     'Content-type': 'application/json',
    }
    timeout = 180

    def __init__(self, host=host, url=url, timeout=None):
        self.host = re.sub("\Ahttps?://", "", host)
        self.url = re.sub("\Ahttps?://[^/]+/", "", url)

        self.timeout = 30
        try:
            if self.ping() != "OK":
                raise ValueError()
        except (socket.gaierror, ValueError):
            raise NetworkError("No response from %s%s" % (host, url))

        if timeout is None:
            timeout = _fc.timeout

        try:
            self.timeout = int(timeout)
            assert self.timeout > 0
        except:
            raise ValueError("timeout parameter must be a positive number")

        return

    @staticmethod
    def _timeout(signo, frame):
        raise TimeoutError()
    
    def _make_request(self, method, params=[]):
        """
        Make a request to the Funcassociate web service.

        @return: result
        """
        conn = httplib.HTTPConnection(self.host)
        payload = json.dumps({'method': method, 'params': params, 'id': 0})

        conn.request("POST", self.url, body=payload,
                     headers=_fc.headers)

        hold = signal.signal(signal.SIGALRM, _fc._timeout)
        if self.timeout > 0:
            signal.alarm(self.timeout)
        try:
            try:
                response = conn.getresponse()
                signal.alarm(0)
            except TimeoutError:
                signal.alarm(0)
                raise TimeoutError("Request to %s timed out" % self.host)
        finally:
            signal.signal(signal.SIGALRM, hold)

        conn.close()
        response_data = response.read()
        decoded_response = json.loads(response_data)
            
        if decoded_response['error']:
            raise ServiceError(str(decoded_response['error']['message']))
        return decoded_response['result']

    @staticmethod
    def _check_args(f, given):
        spec = getargspec(f)
        formals = spec[0]
        defaults = spec[3]
        # we disregard the first argument, self; hence the decrement
        # by 1 below
        max_ = len(formals) - 1
        if defaults is None:
            min_ = max_
        else:
            min_ = max_ - len(defaults)
        qual = None

        if given < min_:
            if max_ > min_:
                qual = "at least %d" % min_
            else:
                qual = "exactly %d" % min_
            if min_ > 1:
                s = "s"
            else:
                s = ""
        elif given > max_:
            if max_ > min_:
                qual = "at most %d" % max_
            elif max_ > 0:
                qual = "exactly %d" % max_
            else:
                qual = "no"
            if max_ == 1:
                s = ""
            else:
                s = "s"
        
        if qual is not None:
            raise TypeError("%s() takes %s "
                            "argument%s (%d given)" %
                            (f.__name__, qual, s, given))

    def _decorate(f):
        def wrapper(self, *args):
            _fc._check_args(f, len(args))
            return self._make_request(f.__name__, args)
        return wrapper

    @_decorate
    def available_species(self):
        """
        @return: List of species supported by Funcassociate.
        service.
        """

    @_decorate
    def available_namespaces(self, species):
        """
        @return: List of namespaces supported by Funcassociate for the
        given species.
        """

    @_decorate
    def go_associations(self, species, namespace, support=None):
        """
        @return: List of GO associations used by Funcassociate
        for the specified species, namespace, and support
        """

    @_decorate
    def go_attrib_dict(self):
        """
        @return: Dictionary whose keys are GO attribute IDs and whose
        values are their corresponding human-readable names.
        """

    @_decorate
    def version(self):
        """
        @return: Version of Funcassociate server.
        """

    @_decorate
    def ping(self):
        """
        @return: The string "OK".
        """

    @_decorate
    def fail(self):
        """
        @return: nothing.
        """

    def functionate(self, query=None, associations=None,
                    attrib_dict=None, species=None, namespace=None,
                    genespace=None, mode=None, which=None,
                    cutoff=None, reps=None):
        """
        @return: functionate results structure
        """
        params = locals()
        del params['self']
        keys = params.keys()
        for k in keys:
            if params[k] is None:
                del params[k]
        result = self._make_request('functionate', [params])

        if result.has_key("input_error"):
            raise InputError(result["input_error"])

        return result

FuncassociateClient = _fc

if '__main__' == __name__:
    c = _fc()
    response = c.functionate(query=("YBL071W-A", "YCL055W", "YCR094W",
                                    "YDL127W", "YFL029C", "YGR271C-A",
                                    "YHR099W", "YJR066W", "YKL203C",
                                    "YNL289W"),
                             species="Saccharomyces cerevisiae",
                             namespace="sgd_systematic")

    print "OVERREPRESENTED ATTRIBUTES"

    headers = ("N", "X", "LOD", "P", "P_adj", "attrib ID", "attrib name")
    print "\t".join(headers)

    info = response["request_info"]
    reps = info["reps"]
    below_detection_threshhold = "< %f" % (1.0/float(reps))

    for row in response["over"]:
        row.pop(1)
        if row[4] is 0:
            row[4] = below_detection_threshhold
        print "\t".join(map(str, row))

    print "\nREQUEST INFO"
    for k in info.keys():
        print "%s: %s" % (k, info[k])


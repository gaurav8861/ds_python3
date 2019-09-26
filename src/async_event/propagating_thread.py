# Copyright 2019 Cray Inc. All Rights Reserved.

"""
A thread specialization for propagating unhandled exceptions out to the
main thread.
"""

import threading


class PropagatingThread(threading.Thread):
    """
    A thread type that can propagate exceptions out to the main thread.
    """

    def __init__(self, target=None, name=None, args=None, kwargs=None):
        """
        Provide an instance variable to hold an exception object.
        """
        if not args:
            args = ()
        if not kwargs:
            kwargs = {}
        super(PropagatingThread, self).__init__(target=target, name=name,
                                                args=args, kwargs=kwargs)
        self.exc = None

    def run(self):
        """
        Run the thread, wrapping it in an exception handler.  Add a new
        instance variable to hold the exception.
        """

        try:
            super(PropagatingThread, self).run()
        except BaseException as ex:  # pylint: disable=W0703
            self.exc = ex

    def join(self, timeout=None):
        """
        Join the thread.  If it has thrown an exception then re-raise it.
        """

        super(PropagatingThread, self).join(timeout)
        if self.exc:
            raise self.exc

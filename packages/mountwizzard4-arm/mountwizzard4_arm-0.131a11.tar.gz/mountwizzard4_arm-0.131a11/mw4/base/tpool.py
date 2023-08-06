############################################################
# -*- coding: utf-8 -*-
#
#       #   #  #   #   #    #
#      ##  ##  #  ##  #    #
#     # # # #  # # # #    #  #
#    #  ##  #  ##  ##    ######
#   #   #   #  #   #       #
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.7.4
#
# Michael Würtenberger
# (c) 2019
#
# Licence APL2.0
#
###########################################################
# standard libraries
import logging
import sys
# external packages
import PyQt5
# local imports


__all__ = ['Worker',
           ]


class WorkerSignals(PyQt5.QtCore.QObject):
    """
    The WorkerSignals class offers a list of signals to be used and instantiated by the Worker
    class to get signals for error, finished and result to be transferred to the caller back
    """

    __all__ = ['WorkerSignals']
    version = '1.0.0'

    finished = PyQt5.QtCore.pyqtSignal()
    error = PyQt5.QtCore.pyqtSignal(object)
    result = PyQt5.QtCore.pyqtSignal(object)


class Worker(PyQt5.QtCore.QRunnable):
    """
    The Worker class offers a generic interface to allow any function to be executed as
    a thread in an threadpool
    """

    __all__ = ['Worker',
               'run']
    version = '1.0.0'
    logger = logging.getLogger(__name__)

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        # the worker signal must not be a class variable, but instance otherwise
        # we get trouble when having multiple threads running
        self.signals = WorkerSignals()

    @PyQt5.QtCore.pyqtSlot()
    def run(self):
        """
        runs an arbitrary methods with it's parameters and catches the result

        :return: nothing, but sends results and status as signals
        """

        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception:
            # as we want to send a clear message to the log file
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb = exc_traceback

            # moving toward the end of the trace
            while tb.tb_next is not None:
                tb = tb.tb_next

            # getting data out for processing
            file = tb.tb_frame.f_code.co_filename
            line = tb.tb_frame.f_lineno

            errorString = f'{file}, line {line} {exc_value}'
            self.logger.error(errorString)
            self.signals.error.emit(errorString)
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()

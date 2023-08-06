#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# Processes
import threading
import multiprocessing

def isMainThreadInAPythonProcess():
	'''

	Used to determine if the code is being run as a main thread in a Python process.

	Returns
	-------
	bool
		`True` if running as a main thread under a Python process, `False` if running as a child thread under a Python process.


	.. warning::

		While this will return `True` when run as the Polycephaly main process, it will also return `True` if it's a process running in
		:any:`multiprocessing mode <polycephaly.core.application.setup.Extend.addProcess>` under Polycephaly.

		To determine if this is the Polycephaly main process, use :any:`isApplicationMainThread() <polycephaly.functions.threading.isApplicationMainThread>`.

	'''

	return True if ( threading.current_thread() is threading.main_thread() ) else False

	pass # END FUNCTION : Is this the Main Thread?

def isApplicationMainThread( cls=None ):
	'''

	Determines if code is running in a process as the :any:`application's main thread <polycephaly.core.application.Application>` or something else
	(e.g. a child thread of the main process or as a sub-process).

	Parameters
	----------
	cls : :obj:`class`, optional
		Process class when setting up a process (usually ``self``).

	Returns
	-------
	bool
		`True` if running as the application's main process, `False` if running as anything else.


	.. warning::

		For most of the time, this is a nearly identical result as :any:`isMainThreadInAPythonProcess() <polycephaly.functions.threading.isMainThreadInAPythonProcess>`,
		but the difference is that it can be used when setting up a process (e.g. :any:`Process._setupFilters() <polycephaly.core.process.Process._setupFilters>` located in
		the :any:`Process class <polycephaly.core.process.Process>`, which would otherwise register as a *false positive*).

	'''

	if cls:
		return True if ( ( cls.name == cls.nameMain ) and isMainThreadInAPythonProcess() ) else False
		pass # END IF

	elif (
		isMainThreadInAPythonProcess()
		and
		not isProcessThreaded()
		and
		not isProcessForked()
	):
		return True
		pass # END ELIF

	else:
		return False
		pass # END ELSE

	pass # END FUNCTION : Is this the Application thread?

def isProcessThreaded():
	'''

	Determines if a process is forked via `Python Multiprocessing <https://docs.python.org/3/library/threading.html>`_ or not.
	This covers both manually creating a threaded process, or a Polycephaly process' :any:`mode <polycephaly.core.application.setup.Extend.addProcess>` set to Threading.

	Returns
	-------
	bool
		`True` if threaded, `False` if not.

	'''

	return True if ( not isMainThreadInAPythonProcess() and not isProcessForked() ) else False

	pass # END FUNCTION : Is this process threaded?

def isProcessForked():
	'''

	Determines if a process is forked via `Python Multiprocessing <https://docs.python.org/3/library/multiprocessing.html>`_ or not.
	This covers both manually creating a forked process, or a Polycephaly process' :any:`mode <polycephaly.core.application.setup.Extend.addProcess>` set to Multiprocessing.

	Returns
	-------
	bool
		`True` if forked, `False` if not.


	.. seealso::

		Discussion on a Stack Overflow question, "`How to determine if running current process is parent? <https://stackoverflow.com/questions/42283265/how-to-determine-if-running-current-process-is-parent>`_".

	'''

	return False if ( multiprocessing.current_process().name == 'MainProcess' ) else True

	pass # END FUNCTION : Is this process forked?

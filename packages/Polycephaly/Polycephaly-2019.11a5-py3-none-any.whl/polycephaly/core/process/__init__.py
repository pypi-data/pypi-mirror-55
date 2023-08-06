#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# System
import sys
import os

# Reflection / Debugging
import functools

# Pattern matching
import glob

# Polycephaly
import polycephaly.functions.threading

# Formatting
from pprint import pformat as pf

# Logging
from logbook import Logger
from polycephaly.log import logger_group
logger = Logger( __loader__.name )
logger_group.add_logger( logger )

#------------------------------------------------------------ IMPORT ALL MODULES
currDir	=	os.path.dirname( __file__ )

# https://stackoverflow.com/questions/1057431/how-to-load-all-modules-in-a-folder
modules	=	glob.glob( f"{currDir}/*.py" )
__all__	=	[ os.path.basename(f)[:-3] for f in modules if os.path.isfile( f ) and not f.endswith('__init__.py') ]

# Add sub-modules
__all__	+=	[ d for d in os.listdir( currDir ) if (
				os.path.isdir( os.path.join( currDir, d ) )
				and
				os.path.isfile( os.path.join( currDir, d, '__init__.py' ) )
			) ]

from . import *
#------------------------------------------------------------/IMPORT ALL MODULES

class Process(
	actions.Extend,
	events.Extend,
	info.Extend,
	locking.Extend,
	messaging.Extend,
	setup.Extend,
	signals.Extend,
	threading.Extend,
	timing.Extend,
):
	'''
    The process class provides the basis for any Process (Main or sub-process) that you want to run.

    The overall archiecture is:

    .. code-block:: python
        :linenos:
        :name: example-process

        class Process( polycephaly.core.Process ):

            def birth( self ):

                # Set-up is performed here.

                pass # END METHOD : Birth

            def life( self ):

                # Looping is performed here.

                pass # END METHOD : Life

            def death( self ):

                # Tear-down is performed here.

                pass # END METHOD : Death

            pass # END CLASS : PROCESS : Main

    `Arguments` and `Keyword Arguments` are passed in from :any:`Application.addProcess() <polycephaly.core.application.setup.Extend.addProcess>` which :any:`Process.__init__() <Process.__init__>` is responsible for handling.

    Parameters
    ----------

    *args
        Variable length argument list passed directly to the process, and accessible as :any:`self.args <polycephaly.core.process.Process.args>` from within the process.

    **kwargs
        Arbitrary keyword arguments passed directly to the process, and accessible as :any:`self.kwargs <polycephaly.core.process.Process.kwargs>` from within the process.
	'''

	# Core
	nameMain		=	None	#: String that represents the *friendly* name of the Application's primary process.
	name			=	None	#: String that represents the *friendly* name of a (sub-)process inheriting from this class.
	paths			=	None	#: Object comprised of namespaces representing the various paths used by the application.
	_runtime		=	None	#: Dictionary of a process' run-time variables, such as `frequency`, accessible by :any:`getParameter() <polycephaly.core.process.info.Extend.getParameter>`.
	_ppill			=	None	#: String (by default, a UUID) that represents a *Poison Pill*.  When a process receives a message with this unique value as the subject line, the process will invoke its :any:`die() <polycephaly.core.process.actions.Extend.die>` method.  Also see :any:`ebrake() <polycephaly.core.process.actions.Extend.ebrake>` which allows any sub-process to request the Main process to shut down the entire application.
	_messenger		=	None	#: Instance of :any:`Polycephaly\'s Messenger <polycephaly.comms.messenger>` class, and wrapped by methods defined in the :any:`process.messaging <polycephaly.core.process.messaging>` package.
	_application	=	None	#: Instance of the :any:`Application class <polycephaly.core.application.Application>` used by :any:`Process.getApp() <polycephaly.core.process.info.Extend.getApp>`.

	# Local variables
	args			=	None	#: Tuple of Arguments that are passed to the sub-process by :any:`Application.addProcess() <polycephaly.core.application.setup.Extend.addProcess>`.
	kwargs			=	None	#: Dictionary of Keyword Arguments that are passed to the sub-process by :any:`Application.addProcess() <polycephaly.core.application.setup.Extend.addProcess>`.

	# Events
	_callbacks		=	None
	'''

	Dictionary of callbacks registered (`key` is the event name, and `value` is the callback method) with :any:`Process.registerCallbacks() <polycephaly.core.process.events.Extend.registerCallbacks>` that are called by :any:`Process.callbackEvent() <polycephaly.core.process.events.Extend.callbackEvent>` when a specified event occurs.

	An example use case is when specific USB hardware tracked by a Manufacturer ID and/or Model ID (which Polycephaly matches from all a list of all connected USB devices queried from the Operating System) experiences one or more of the following events:

	* **connected** - device plugged in.
	* **disconnected** - device unplugged.
	* **pong** - responds to a ping sent by a child thread (any method starting with `_thread` can be automatically launched by :any:`Process.launchThreads() <polycephaly.core.process.threading.Extend.launchThreads>` in the :any:`Process.birth() <polycephaly.core.process.events.Extend.birth>` method of a process) of a sub-process.
	* **commsError** - if the device responds to a message with an error letting us know that something went wrong.
	* **deviceError** - if the device itself experiences an error.

	'''

	# Process state

	_locks			=	None
	'''

	Dictionary of atomic locks for a sub-process to use, which are set by :any:`Process.addLocks() <polycephaly.core.process.locking.Extend.addLocks>` and queried by :any:`Process.getLocks() <polycephaly.core.process.locking.Extend.getLocks>`.

	.. seealso:: :any:`Process._setupEvents() <polycephaly.core.process.Process._setupEvents>` is used to setup a lock for each process that's :any:`added <polycephaly.core.application.setup.Extend.addProcess>` into an application.

	'''
	_active			=	False	#: Boolean whose status is retrieved (and set) by :any:`Process.isActive() <polycephaly.core.process.info.Extend.isActive>`, determines if :any:`Process.life() <polycephaly.core.process.events.Extend.life>` will continue running in :any:`Process.main() <polycephaly.core.process.setup.Extend.main>`'s loop, and can also be referred to by any child threads that a process spins up (please see :any:`Thread Spinner <../examples/threadSpinner/launch>` for an example).
	_runLevel		=	None	#: Integer that indicates the process' current run level (and a poor copy of how Linux does it) which is retrieved (and set) by :any:`Process.runLevel() <polycephaly.core.process.info.Extend.runLevel>`
	_threads		=	None	#: Dictionary of child threads (`key` is the name, and `value` is the thread object representing a dedicated method) that a process may spin up.  This is used extensively by the methods in the :any:`Process.Threading <polycephaly.core.process.threading>` package.
	_currFrame		=	None	#: Integer used for tracking the progress of frames per second via :any:`Process.currentFrame() <polycephaly.core.process.timing.Extend.currentFrame>` within the span of 1 second for a process' execution of :any:`Process.life() <polycephaly.core.process.events.Extend.life>` from the :any:`Process.main() <polycephaly.core.process.setup.Extend.main>` loop.
	_ranMailman		=	False	#: Boolean that's used for tracking if :any:`Process.mailman() <polycephaly.core.process.messaging.actions.Extend.mailman>` was run in :any:`Process.life() <polycephaly.core.process.events.Extend.life>` or not.  If not, then :any:`Process.mailman() <polycephaly.core.process.messaging.actions.Extend.mailman>` will automatically be executed for this cycle and to ensure that the :any:`Poison Pill <polycephaly.core.process.Process._ppill>` is received if sent from another process.

	# Signals
	_signalsBak		=	None	#: Dictionary used by :any:`Process.backupSignals() <polycephaly.core.process.signals.Extend.backupSignals>` and :any:`Process.restoreSignals() <polycephaly.core.process.signals.Extend.restoreSignals>` where `key` is the name (e.g. `SIGINT`) and `value` is the handler (e.g. `<built-in function default_int_handler>`).
	_signalsUsed	=	False	#: Boolean used by :any:`Process.signalsUsed() <polycephaly.core.process.signals.Extend.signalsUsed>` for tracking if any signals have been bound to a callback method with :any:`Process.signals() <polycephaly.core.process.signals.Extend.signals>`.
	signalEnd		=	None	#: If a Signal is received, an integer representing the Signal event responsible for the shutdown (e.g. 2 for SIGINT, 15 for SIGTERM, etc.).  Please note, you can pass this value to :any:`Process.signalsDict() <polycephaly.core.process.signals.Extend.signalsDict>` to obtain the string equivalent.

	def _setupVariables( self, args, kwargs ):
		'''

		Sets the :any:`Process <polycephaly.core.process.Process>` variables for use by an instantiated process.

		'''

		# e.g. main
		self.nameMain		=	kwargs.pop( 'nameMain' )

		# e.g. helloworld
		self.name			=	kwargs.pop( 'name' )

		# e.g. self.paths.base=/opt/helloWorld, self.paths.program=/opt/helloWorld/launch.py
		self.paths			=	kwargs.pop( 'paths' )

		# Prevent incompatibility with names
		if self.name in self.paths.__dict__.keys():
			raise KeyError( f"Process named '{ self.name }' conflicts with a stored path value." )
			pass # END IF

		# Add path to current process *after* inheritance.
		setattr(
			self.paths,
			self.name,
			os.path.abspath( sys.modules[ self.__class__.__module__ ].__file__ )
		)

		# e.g. {'autostart': True, 'daemon': True, 'depends': [], 'frequency': 30, 'forceStop': True, 'mode': 'T'}
		self._runtime		=	kwargs.pop( 'runtime' )

		# e.g. 038ad5eb-5aee-4f70-9c93-1a522991c5a0
		self._ppill			=	kwargs.pop( 'ppill' )

		# e.g. Polycephaly Messenger object.
		self._messenger		=	kwargs.pop( 'messenger' )

		# Store local variables for this process' other methods to use.
		self.args			=	args
		logger.debug( f"{ self.name }.args = { pf( self.args ) }" )
		self.kwargs			=	kwargs
		logger.debug( f"{ self.name }.kwargs = { pf( self.kwargs ) }" )

		# Dictionary of callbacks for message filters used by a specific process.
		self._callbacks		=	{}

		# Dictionary of threads used by a specific process.
		self._threads		=	{}

		# Dictionary of locks used by a specific process.
		self._locks			=	{}

		# Primarily used by the Main process for backing up signals, but can also be used by sub-processes loaded as multiprocessing.
		self._signalsBak	=	{}

		pass # END METHOD : Setup variables

	def _setupEvents( self ):
		'''

		Used to setup the process for running.  Actions taken:

		#. Sets the process' :any:`active flag <Process._active>` to true.

		#. Adds a lock for the process' message queue, which is most often used by :any:`Process.waitForReply() <polycephaly.core.process.messaging.actions.Extend.waitForReply>`.

		'''

		self.isActive( True )

		self.addLocks(
			'queue'		# Used by self.getQueue() to lock access to the message queue in case we want threads to also deal with this queue.
		)

		pass # END METHOD : Setup events

	def _setupFilters( self ):
		'''

		Responsible for adding core message filters to be used by all processes:

		* **Main process** (determined by :any:`isApplicationMainThread() <polycephaly.functions.threading.isApplicationMainThread>`)

			* **Emergency Brake** - when a process calls :any:`Process.ebrake() <polycephaly.core.process.actions.Extend.ebrake>`, a message is sent to the Main process requesting that the entire application be shutdown immediately.
				* **Callback**: :any:`Process.die() <polycephaly.core.process.actions.Extend.die>`
				* **Message parameters**:

					* **Subject**: ``EBRAKE`` (case insensitive)

			* **Process Info** - responds to sub-processes asking the Main process for information about other processes.
				* **Callback**: :any:`Process.Main.__subProcInfo() <polycephaly.core.process.main.callbacks.Extend._Extend__subProcInfo>` - this method is `monkey-patched <https://stackoverflow.com/questions/5626193/what-is-monkey-patching>`_ into the Main process.
				* **Message parameters**:

					* **Subject**: ``PROCINFO`` (case insensitive)

		* **All processes**

			* **Poison pill** - when a process receives this, it will die.  To resurrect a dead process, :any:`Application.start() <polycephaly.core.application.actions.Extend.start>` or :any:`Application.restart() <polycephaly.core.application.actions.Extend.restart>` is needed, which the Main process can access via :any:`Process.getApp() <polycephaly.core.process.info.Extend.getApp>`.
				* **Callback**: :any:`Process.die() <polycephaly.core.process.actions.Extend.die>`
				* **Message parameters**:

					* **Subject**: :any:`Process._ppill <polycephaly.core.process.Process._ppill>` `(case insensitive)`

		'''

		# Shutdown the entire application.
		if polycephaly.functions.threading.isApplicationMainThread( self ):

			self.addFilter(
				id			=	'e-brake',
				description	=	'Emergency brake : shut the entire application down.',
				recipient	=	fr'(?i)^{ self.nameMain }$',
				subject		=	r'(?i)^EBRAKE$',
				callback	=	self.die,
			)

			# Monkey-patching : add `__subProcInfo` callback for filter to use.
			monkeyMethodSubProcInfo				=	functools.partial( main.Extend._Extend__subProcInfo, self )
			monkeyMethodSubProcInfo.__name__	=	'_Process__subProcInfo'
			monkeyMethodSubProcInfo.__doc__		=	"Queries methods in the application's side and returns them back across the wire to a process that's asking for the information."
			setattr(
				self,
				'_Process__subProcInfo',
				monkeyMethodSubProcInfo
			)
			del monkeyMethodSubProcInfo

			self.addFilter(
				id			=	'proc-info',
				description	=	'Returns results to sub-processes asking the main process for information.',
				recipient	=	fr'(?i)^{ self.nameMain }$',
				subject		=	r'(?i)^PROCINFO$',
				callback	=	self.__subProcInfo,
			)

			pass # END IF

		# Shutdown process.
		self.addFilter(
			id			=	'ppill',
			description	=	'Poison pill.',
			recipient	=	fr'(?i)^{ self.name }$',
			subject		=	fr'(?i)^{ self._ppill }$',
			callback	=	self.die,
		)

		pass # END METHOD : Setup events

	def __init__( self, *args, **kwargs ):
		'''

		This is the constructor of the :any:`Process class <Process>`, which executes private methods in the following order for helping prepare a process to run:

		#. :any:`Process._setupVariables( args, kwargs ) <Process._setupVariables>`

		#. :any:`Process._setupEvents() <Process._setupEvents>`

		#. :any:`Process._setupFilters() <Process._setupFilters>`

		Parameters
		----------

		*args
			Variable length argument list passed directly to the process, and accessible as :any:`self.args <polycephaly.core.process.Process.args>` from within the process.

		**kwargs
			Arbitrary keyword arguments passed directly to the process, and accessible as :any:`self.kwargs <polycephaly.core.process.Process.kwargs>` from within the process.

		'''

		# Setup environments variables.
		self._setupVariables( args, kwargs )

		# Active and initialization of locks.
		self._setupEvents()

		# Adds basic filters, such as shutdown.
		self._setupFilters()

		pass # END METHOD : Constructor

	pass # END CLASS : Polycephaly Process

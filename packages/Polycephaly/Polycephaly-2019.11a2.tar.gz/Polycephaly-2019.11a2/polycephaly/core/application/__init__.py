#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# System
import sys
import os

# Types
import collections
import types
import uuid

# Pattern matching
import glob

# Polycephaly
from polycephaly.comms.messenger import Messenger as PCM
import polycephaly.processes

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

class Application(
	actions.Extend,
	events.Extend,
	info.Extend,
	setup.Extend,
	timing.Extend,
):
	'''
    The application class is used within the *Launcher* that sets up and runs the entire Polycephaly application.

    The overall archiecture is:


    .. code-block:: python
        :linenos:
        :caption: **launch.py**
        :name: example-application

        class Application( polycephaly.core.Application ):

            def build( self ):

                # Application parameters and processes can go here.

                pass # END METHOD : Build

            pass # END CLASS : Application

        if __name__ == '__main__':

            Application(

                processes.main,
                # Additional parameters for your main process can go here.

            ).run()

            pass # END MAIN

    .. seealso::

        * The :any:`Examples <../examples/index>` directory with several applications and their reciprocal launchers.

        * :any:`Application.build() <polycephaly.core.application.events.Extend.build>` and methods to use inside of it:

            * :any:`Application.globalFrequency() <polycephaly.core.application.timing.Extend.globalFrequency>`

            * :any:`Application.addProcess() <polycephaly.core.application.setup.Extend.addProcess>`

	'''

	# Application variables
	name			=	None	#: Name of the main process.
	ppill			=	None	#: Poison Pill value.
	threadsTimeout	=	None	#: Time to wait before giving up on a threaded process shutting down.

	# Process skeleton
	_skel		=	types.SimpleNamespace(

						runtime		=	collections.defaultdict(
											lambda			:	None,	# Default return.
											mode			=	'T',	# [A]syncIO, [T]hread, Forked [P]rocess, or [E]xternal Program.
											autostart		=	True,	# Autostart.
											depends			=	[],		# Dependencies - change order based on needs.
											frequency		=	None,	# Frequency - None is a placeholder. See below in __init__() and polycephaly.core.application.setup._setDefaultFreqs()
											boundShutdown	=	True,	# If true, Process exit when Main does.
											forceStop		=	True,	# If true, Process' death() method can be interrupted.
										),

					)	#: Skeleton values for a new process.

	# Process information
	_procs		=	types.SimpleNamespace(
						objects		=	{},
						threads		=	{},
					)
	'''

	**Process tables**:

		* **Objects** - Initialized class instances.

		* **Threads** - Used for Threaded (and Forked) Processes.

	'''


	# System paths
	paths		=	types.SimpleNamespace(
						program		=	os.path.abspath( sys.argv[ 0 ] ),
						base		=	os.path.abspath( os.path.dirname( sys.argv[ 0 ] ) ),
						processes	=	types.SimpleNamespace(
											internal	=	os.path.abspath( os.path.dirname( polycephaly.processes.__file__ ) ),
											external	=	os.path.join( os.path.abspath( os.path.dirname( sys.argv[ 0 ] ) ), 'processes' ),
										),
					)
	'''

	**Path tables**:

		* **Program** - Path to the application launcher.

		* **Base** - Directory to the application launcher.

		* **Processes** - Polycephaly has 2 types of processes:

			* **Internal** - Path to built-in processes (e.g. Unix Domain Socketfile, MQTT, XMPP, et al.) that you can use and/or inherit from.

			* **External** - Your application's specific processes that you've created.

		* **Each process' path is also added to this table.**

	'''

	# Polycephaly Messaging
	pcm			=	None	#: :any:`Polycephaly Messenger <polycephaly.comms.messenger>` instance.

	def __init__( self, mainProcess=None, *args, **kwargs ):
		'''

		This is the constructor for the Application class, and handles the preliminary setup, with the remainder of the setup handled by :any:`Application.run() <polycephaly.core.application.setup.Extend.run>`.

		Parameters
		----------
		mainProcess : :obj:`Module` or :obj:`Class`, optional
			Can accept a Python `Module` if the module contains a `Process` class, otherwise you'll need to pass the direct `Class` to use.

		*args
			Variable length argument list passed directly to the main process (if created here, instead of via :any:`Application.addProcess() <polycephaly.core.application.setup.Extend.addProcess>`).

		**kwargs
			Arbitrary keyword arguments passed directly to the main process (if created here, instead of via :any:`Application.addProcess() <polycephaly.core.application.setup.Extend.addProcess>`).

			Please note, there are reserved keywords that are used by the constructor:

			* **name** (:obj:`str`, optional, default: `main`) - Name of the main process.

			* **ppill** (:obj:`str`, optional, default: `UUID <https://en.wikipedia.org/wiki/Universally_unique_identifier>`_) - Poison Pill that's used to shutdown any process.

				.. warning::

					Should you choose to override the default, please take care and don't use a common value that may erroneously trigger a process (or the entire application) to shutdown.

			* **threadsTimeout** (:obj:`int`, optional, default: `30`) - Time to wait before giving up on a threaded process shutting down.

			* **queueSize** (:obj:`int`, optional, default: `50`) - Maximum number of messages to keep in queue, 0 for unlimited (which is inadvisable).

			* **queueType** (:obj:`str`, optional, default: `FIFO`) - Type of message queue to use.

				* `FIFO` - First In, First Out.

				* `Priority` - Allows higher priority messages (such as shutdown) to be moved to the front of the queue.

				.. todo::

					* Priority isn't implemented yet, since the Python implementation only supports processes operating in threaded mode.

			* **mode** (:obj:`str`) - *Reserved for internal use.*

			* **autostart** (:obj:`bool`) - *Reserved for internal use.*

		'''

		# Update application variables
		self.name			=	kwargs.pop( 'name', 'main' ).lower()
		self.ppill			=	kwargs.pop( 'ppill', str( uuid.uuid4() ) )
		self.threadsTimeout	=	kwargs.pop( 'threadsTimeout', 30 )

		# Remove conflicting keywords that we'll set below.
		[ kwargs.pop( k, None ) for k in [ 'mode', 'autostart', ] ]

		# Polycephaly's shared Messaging platform.
		self.pcm	=	PCM(
							nameMain	=	self.name,								# Used for tracking the main process name.
							queueSize	=	kwargs.pop( 'queueSize', 50 ),			# Number of messages to keep in queue.
							queueType	=	kwargs.pop( 'queueType', 'FIFO' ),		# [F]IFO or [P]riority queue.
						)

		# Application parameters and processes are generally set here.
		self.build()

		# Create an entry for the Main Process if a reference was passed in.
		if mainProcess and ( self.name not in self.listProcessInstances() ):

			self.addProcess(
				mainProcess,
				name		=	self.name,
				mode		=	'Process',
				autostart	=	False,
				*args,
				**kwargs,
			)

			pass # END IF

		# User didn't set a default frequency, so we'll set one for them.
		if not self.globalFrequency():
			self.globalFrequency( 30 )
			pass # END IF

		pass # END CONSTRUCTOR

	pass # END CLASS : Polycephaly Application

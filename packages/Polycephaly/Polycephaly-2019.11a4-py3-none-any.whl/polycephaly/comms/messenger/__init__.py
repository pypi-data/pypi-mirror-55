#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# System
import os

# Types
import collections

# Pattern matching
import glob

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

class Messenger(
	actions.Extend,
	filters.Extend,
	info.Extend,
	setup.Extend,
):
	'''

	This class serves as a messenger which is wrapped by :any:`Process.messaging <polycephaly.core.process.messaging>`,
	and can also be used in an entirely separate application (e.g. a `Kivy application <https://kivy.org/>`_).

	.. note::

		Outside of Polycephaly, at the Python (and Operating System) level, there's a lot that's happening behind the scenes for messaging to work so well.
		Some of the most useful discussions that I've encountered for tackling this implementation have come from reading:

			* `Stack Overflow : multiprocessing.Queue and Queue.Queue are different? <https://stackoverflow.com/questions/30294571/multiprocessing-queue-and-queue-queue-are-different>`_

			* `Stack Overflow : Multiprocessing - Pipe vs Queue <https://stackoverflow.com/questions/8463008/multiprocessing-pipe-vs-queue>`_

		TL;DR: Python Threads use in-memory queues under the same process, Python (forked, ahem, `multi`) Processes use pipes.

	.. seealso::

		* `Threading.Queue <https://docs.python.org/3/library/queue.html#queue.Queue>`_

			* `Threading.Queue.PriorityQueue <https://docs.python.org/3/library/queue.html#queue.PriorityQueue>`_

		* `Multiprocessing.Queue <https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue>`_

			* `Brandon Wamboldt : How Linux pipes work under the hood <https://brandonwamboldt.ca/how-linux-pipes-work-under-the-hood-1518/>`_

	.. todo::

		* Adding priority queue capabilities in for all sub-processes, regardless of their mode.  `Python only supports priority queues for threads <https://stackoverflow.com/questions/25324560/strange-queue-priorityqueue-behaviour-with-multiprocessing-in-python-2-7-6>`_, which is where this difficulty lies.

	'''

	# Parameters
	nameMain		=	None	#: Main process name.

	# Defaults
	_defSize		=	None	#: Default size for message queues.
	_defCaller		=	None	#: Default caller.
	_defRoute		=	None	#: Default route.
	_defType		=	None	#: Default queue type.

	# Message filters
	_filters		=	collections.defaultdict(
							lambda	:	collections.defaultdict(
											lambda	:	list()
										)
						)		#: Message filters.

	# Message Queues - e.g. a dictionary with keys, 'main', 'ocm', 'ros', and 'uds'
	_queues			=	{}		#: Message queues.

	def __init__( self, **kwargs ):
		'''

		Initial setup for Polycephaly Messenger.

		Parameters
		----------

		*kwargs
			Arbitrary keyword arguments used for configuring messenger:

				* **nameMain** (:obj:`str`) - Name of the main process.

				* **queueSize** (:obj:`int`, optional, default: ``0``) - Maximum number of messages to keep in a queue, or ``0`` for unlimited.

				* **defaultCaller** (:obj:`str`, optional, default: :obj:`None`) - A caller identifies which process is using the messenger.  With normal Polycephaly usage, each process is a separate caller.

				* **defaultRoute** (:obj:`str`, optional, default: :obj:`None`) - Routes are used for filtering, and allow you to separate filters for buses (e.g. internal and another for Unix Domain Socketfile).

				* **queueType** (:obj:`str`, optional, default: ``FIFO``) - Different queue types offer features to suit your needs.

		'''

		# Parameters

		self.nameMain	=	kwargs.pop( 'nameMain' ).lower()
		logger.debug( f"Main process name : { self.nameMain }" )

		# Set defaults

		self._defSize	=	kwargs.get( 'queueSize', 0 )			# 0 for unlimited
		logger.debug( f"Default message size : { self._defSize }" )

		self._defCaller	=	kwargs.get( 'defaultCaller' )			#
		logger.debug( f"Default caller : { self._defCaller }" )

		self._defRoute	=	kwargs.get( 'defaultRoute' )			#
		logger.debug( f"Default route : { self._defRoute }" )

		self._defType	=	kwargs.get( 'queueType', 'FIFO' )		# FIFO or Priority
		if self._defType[ 0 ] not in [ 'F', 'P' ]:
			raise ValueError( 'Invalid queue type.' )
			pass # END IF
		logger.debug( f"Default message type : { self._defType }" )

		pass # END METHOD : Constructor

	pass # END CLASS : Polycephaly Messenger

#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# Message Queues
from queue import Queue as queueThread
from multiprocessing import Queue as queueProcess

# Polycephaly
import polycephaly.functions.utilities

# Logging
from logbook import Logger
from polycephaly.log import logger_group
logger = Logger( __loader__.name )
logger_group.add_logger( logger )

class Extend( object ):

	def addQueue( self, name, queueType, **kwargs ):
		'''

		Add message queue to table.

		Parameters
		----------
		name : :obj:`str`
			Name of message queue to add.

		queueType : :obj:`str`
			Related entirely to what the process type is:

				* `Threading` (internal message queue)

				* `Multiprocessing` (pipes)

		**kwargs

			* **size** (:obj:`int`, optional, default: :any:`default size <polycephaly.comms.messenger.Messenger._defSize>`) - maximum number of messages that can be placed in queue.

		'''

		logger.debug( f"Adding message queue (type: '{ queueType }') for '{ name }'." )

		if name in self._queues:
			raise KeyError( 'Message queue already exists.' )
			pass # END IF

		queueSize	=	kwargs.get( 'size', self._defSize )

		for case in polycephaly.functions.utilities.switch( queueType[ 0 ].upper() ):

			# AsyncIO
			if case( 'A' ):
				self._queues[ name ]	=	queueProcess( queueSize )
				break # END CASE

			# Thread
			if case( 'T' ):
				self._queues[ name ]	=	queueThread( queueSize )
				break # END CASE

			# Multiprocessing
			if case( 'M' ):
				self._queues[ name ]	=	queueProcess( queueSize )
				break # END CASE

			# Subprocess
			if case( 'P' ):
				self._queues[ name ]	=	queueProcess( queueSize )
				break # END CASE

			pass # END SWITCH

		return self._queues[ name ]

		pass # END METHOD : Add queue

	pass # END CLASS : Polycephaly Messenger

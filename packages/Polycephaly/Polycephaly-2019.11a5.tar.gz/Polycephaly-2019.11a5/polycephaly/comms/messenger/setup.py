#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# Message Queues
from queue import Queue as queueThread
from multiprocessing import Queue as queueProcess
from multiprocessing.queues import Queue as queueProcessType

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

		Returns
		-------
		:obj:`Queue`
			Message queue that was just created.

		'''

		name	=	name.lower()

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

			if case():
				raise ValueError( f"Unknown queue mode : '{ queueType[ 0 ].upper() }'." )
				break # END CASE

			pass # END SWITCH

		return self._queues[ name ]

		pass # END METHOD : Add queue

	def addQueues( self, queueType, *names, **kwargs ):
		'''

		Wrapper for :any:`Messenger.addQueue() <polycephaly.comms.messenger.setup.Extend.addQueue>` that allows you to add multiple message queues.

		Parameters
		----------
		queueType : :obj:`str`
			Type of queue to add, please see :any:`Messenger.addQueue() <polycephaly.comms.messenger.setup.Extend.addQueue>` for available options.

		*names : :obj:`str`
			Arbitrary number of queues to add.

		**kwargs : optional
			Additional settings for queue, please see :any:`Messenger.addQueue() <polycephaly.comms.messenger.setup.Extend.addQueue>` for available options.

		Returns
		-------
		:obj:`Dictionary`
			Message queues that were just created, where `keys` are the names created and `values` are the queues that were created.

		'''

		r	=	{}

		for name in names:

			r[ name ]	=	self.addQueue(
								name,
								queueType,
								**kwargs
							)

			pass # END FOR

		return r

		pass # END METHOD : Add queues

	def removeQueues( self, *names ):
		'''

		Used for removing one or more queues by flushing and then deleting them.

		Parameters
		----------
		*names : :obj:`str`
			Arbitrary number of queues to remove.

		Returns
		-------
		:obj:`Dictionary`
			Keys are name of targeted queue(s), values are :obj:`bool` or :obj:`None` indicating status of removal:

				* `True` - Queue successfully flushed and removed.

				* `False` - Unknown queue type (couldn't flush), but removed anyways.

				* `None` - Nothing with that name exists.

		'''

		r	=	{}
		for name in names:

			name	=	name.lower()

			# Doesn't exist
			if name not in self._queues:
				r[ name ]	=	None
				continue
				pass # END IF

			q	=	self._queues[ name ]

			# Purge valid queue for threads.
			if type( q ) == queueThread:

				with q.mutex:
					q.queue.clear()

				r[ name ]	=	True

				pass # END IF : Threading

			# Purge valid queue for forked processes.
			elif type( q ) == queueProcessType:

				while not q.empty():
					q.get()

				r[ name ]	=	True

				pass # END ELIF : Multiprocessing

			# Invalid queue, nothing to purge.
			else:

				r[ name ]	=	False

				pass # END ELSE

			del self._queues[ name ]

			pass # END FOR

		return r

		pass # END METHOD : Remove queues

	def removeQueue( self, name ):
		'''

		Wrapper for :any:`Messenger.removeQueues() <polycephaly.comms.messenger.setup.Extend.removeQueues>` that allows you to remove a single message queue, and will return its result.

		Parameters
		----------
		name : :obj:`str`
			Name of queue to remove.

		Returns
		-------
		return
			Singular entry for queue, with result passed directly from :any:`Messenger.removeQueues() <polycephaly.comms.messenger.setup.Extend.removeQueues>`.

		'''

		return self.removeQueues( name )[ name.lower() ]

		pass # END METHOD : Remove queue

	pass # END CLASS : Polycephaly Messenger

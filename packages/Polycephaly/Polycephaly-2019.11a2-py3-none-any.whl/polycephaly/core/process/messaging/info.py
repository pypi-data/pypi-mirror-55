#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# Logging
from logbook import Logger
from polycephaly.log import logger_group
logger = Logger( __loader__.name )
logger_group.add_logger( logger )

class Extend( object ):

	def getQueue( self, *args, **kwargs ):
		'''

		Used for accessing a message queue that's stored in Polycephaly Messenger's table.

		This method wraps :any:`Messenger.getQueue() <polycephaly.comms.messenger.info.Extend.getQueue>`.

		Parameters
		----------
		name : :obj:`str`
			Name of message queue to retrieve.

		retType : :obj:`str`, optional, default: ``V``
			* ``K`` - returns the name of the queue, useful when needing to query if a queue exists.
			* ``V`` - returns the message queue.

		**kwargs
			* **ignoreLock** (:obj:`bool`, optional, default: `False`) – Message queues are normally locked when they're worked with, in order to avoid race conditions with methods such as :any:`Process.waitForReply() <polycephaly.core.process.messaging.actions.Extend.waitForReply>`.  You'll probably never use this.

		Returns
		-------
		str, queue, or None
			* :obj:`str` if return type ``K`` is used.
			* :obj:`queue` if return type ``V`` is used.
			* :obj:`None` if no matches were found.

		'''

		name		=	args[ 0 ]
		ignoreLock	=	True if kwargs.get( 'ignoreLock' ) else False

		# With lock
		if name == self.name and not ignoreLock:

			with self.getLocks( 'queue' ):
				return self._messenger.getQueue( *args )
				pass # END LOCK

			pass # END IF : WITH LOCK

		# Without lock
		else:
			return self._messenger.getQueue( *args )
			pass # END ELSE

		pass # END METHOD : Get queue

	pass # END CLASS : Extend

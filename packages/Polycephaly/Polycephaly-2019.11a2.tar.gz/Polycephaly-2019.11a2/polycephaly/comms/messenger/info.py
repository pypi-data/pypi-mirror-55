#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# Logging
from logbook import Logger
from polycephaly.log import logger_group
logger = Logger( __loader__.name )
logger_group.add_logger( logger )

class Extend( object ):

	def getQueues( self, *args ):
		'''

		Used for accessing message queues.

		Parameters
		----------
		*args
			Variable number of queues to retrieve.

		Returns
		-------
		:obj:`dict`
			Key is name, value is message queues.

		'''

		# All
		if not len( args ):
			return self._queues
			pass # END IF

		# Select
		r	=	{}
		for qk, qv in self._queues.items():

			for a in args:

				if qk.upper() == a.upper():

					r.update({ qk : qv })

					pass # END IF

				pass # END FOR : Arguments

			pass # END FOR : Queues

		return r

		pass # END METHOD : Get queues

	def getQueue( self, name, retType='V' ):
		'''

		Used for accessing a single message queue.

		Parameters
		----------
		name : :obj:`str`
			Name of message queue to retrieve.

		retType : :obj:`str`, optional, default: ``V``
			* ``K`` - returns the name of the queue, useful when needing to query if a queue exists.
			* ``V`` - returns the message queue.

		'''

		name	=	name.lower()
		q		=	self.getQueues( name )
		return next( iter( q.keys() if ( retType[ 0 ].upper() == 'K' ) else q.values() ) ) if q else None

		pass # END METHOD : Get queue

	def listQueues( self ):
		'''

		Returns names of all message queues.

		Returns
		-------
		list
			Names of all message queues.

		'''

		return list( self._queues.keys() )

		pass # END METHOD : List queues

	pass # END CLASS : Polycephaly Messenger

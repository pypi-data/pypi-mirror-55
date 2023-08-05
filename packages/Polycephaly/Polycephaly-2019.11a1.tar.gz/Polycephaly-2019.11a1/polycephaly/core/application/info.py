#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# Logging
from logbook import Logger
from polycephaly.log import logger_group
logger = Logger( __loader__.name )
logger_group.add_logger( logger )

class Extend( object ):

	def activeSubProcesses( self ):
		'''

		Returns list of Processes (both threaded and forked) that are still running.

		'''

		return [ threadName for threadName, threadAttr in self._procs.threads.items() if threadAttr.is_alive() ]

		pass # END METHOD : Active Sub-processes

	def listProcessInstances( self ):
		'''

		Lists process instances.

		Returns
		-------
		list
			Process(es) whose classes have been instantiated.

		'''

		return list( self._procs.objects.keys() )
		pass # END METHOD : List process instances

	def listRecipients( self ):
		'''

		Lists message queues that have been setup in :any:`Polycephaly's Messenger <polycephaly.comms.messenger>`.

		Returns
		-------
		list
			Process(es) whose classes have been instantiated.

		'''

		return self.pcm.listQueues()
		pass # END METHOD : List recipients

	def getProcess( self, name ):
		'''

		Used to retrieve the instance of a process.

		Returns
		-------
		object
			Instance of a class that you can inspect (and if you know what you're doing, modify).

		'''

		return self._procs.objects[ name ] if ( name in self._procs.objects ) else None
		pass # END METHOD : Get process instance

	pass # END CLASS : EXTEND

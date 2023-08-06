#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# Types
import types

# Processes
import threading

# Python
import polycephaly.functions.utilities

# Logging
from logbook import Logger
from polycephaly.log import logger_group
logger = Logger( __loader__.name )
logger_group.add_logger( logger )

class Extend( object ):

	def launchThreads( self ):
		'''

        Locates any methods in the process whose name begins with `_thread_`, and then uses :any:`Process.addChildThread() <polycephaly.core.process.threading.Extend.addChildThread>` to add each of these methods as a reciprocal thread, then daemonize and start each thread.

        An example for automatically launching threads:

        .. code-block:: python

            def _thread_Hello( self ):
                while self.isActive():
                    print( 'Hello' )
                    self.freqSleep()
                    pass # END WHILE LOOP
                pass # END METHOD : Hello

            def _thread_World( self ):
                while self.isActive():
                    print( 'World' )
                    self.freqSleep()
                    pass # END WHILE LOOP
                pass # END METHOD : World

            def birth( self ):
                self.launchThreads()
                pass # END METHOD : Birth


        .. seealso::

            :any:`Examples <../examples/index>` making use of this method:

                * :any:`Locking <../examples/locking/launch>`

                * :any:`Thread Spinner <../examples/threadSpinner/launch>`

		'''

		# Search attributes for threads
		for sk in dir( self ):

			# Not valid
			if not ( sk.startswith( '_thread_' ) and callable( getattr( self, sk ) ) ):
				continue
				pass # END IF

			# Everything after `_thread_`
			skName	=	sk[ 8: ].lower()

			args	=	[
							skName,					# Name
							getattr( self, sk ),	# Method
						]

			# This is probably a dynamically created method, such as the case of examples/threadSpinner/.
			if isinstance( getattr( self, sk ), types.FunctionType ):
				args.append( self )
				pass # END IF

			self.addChildThread(
				*args,
				daemon	=	True,
				start	=	True,
			)

			args.clear()

			pass # END FOR

		pass # END METHOD : Launch threads

	def addChildThread( self, name, method, *args, **kwargs ):
		'''

		Simplifies creating (and by default, starting) a child thread running under a process with its index created in :any:`Process._threads <polycephaly.core.process.Process._threads>`.

		Parameters
		----------
		name : :obj:`str`
			Name of thread that can be used in conjunction with thread-related methods.

		method : :obj:`method` or :obj:`function`
			Callable that should be run as the thread.

		*args
			Variable length argument list passed directly to the child thread.

		**kwargs
			Arbitrary keyword arguments passed directly to the child thread.

			Please note, there are reserved keywords that are used by this method:

			* **daemon** (:obj:`bool`, optional, default: `True`) - Binds thread to process, so when the process exits, the thread does too.  You'll almost always want this turned on.

			* **start** (:obj:`bool`, optional, default: `True`) - Start the thread after it's been setup.  Otherwise, you can manually start the thread by using :any:`getChildThread() <polycephaly.core.process.threading.Extend.getChildThread>` to get the instance, and then execute `start()` on that instance:

				.. code-block:: python

					self.getChildThread( 'hello' ).start()

		'''

		daemon	=	kwargs.pop( 'daemon', True )
		start	=	kwargs.pop( 'start', True )

		logger.debug( f"Setting up thread for '{ name }' (daemon={ daemon }, start={ start })." )

		self._threads.update({

			str( name )	:	threading.Thread(
								target	=	method,
								args	=	args,
								kwargs	=	kwargs,
							),

		})

		self._threads[ name ].daemon	=	daemon

		if start:
			self._threads[ name ].start()
			pass # END IF

		pass # END METHOD : Add child thread

	def removeChildThreads( self, *args ):
		'''

		Used for removing stopped child threads from the process' :any:`child threads index <polycephaly.core.process.Process._threads>`.

		Parameters
		----------
		*args : :obj:`str`
			Variable length of stopped child threads to remove from the process.

		Returns
		-------
		dict
			Key is the name of the child thread(s) to remove with a value indicating the status of removal from the index:

			#. `True` - child thread successfully removed.

			#. `False` - child thread couldn't be removed since it's still active.

			#. `None` - child thread either doesn't exist or an error was experienced in removing it.

		'''

		r	=	{}

		for a in args:

			a	=	str( a )

			# Not found.
			if a not in self._threads:
				logger.warning( f"Cannot remove { self.name }.{ a }, it doesn't exist." )
				r[ a ]	=	None
				pass # END IF

			# This doesn't stop the thread, you're responsible for that.
			elif (
				a in self._threads
				and
				self._threads[ a ].is_alive()
			):
				logger.error( f"Cannot remove { self.name }.{ a }, it's still active." )
				r[ a ]	=	False
				pass # END ELIF

			# Finally, success.
			elif ( a in self._threads ):
				logger.debug( f"Removed thread '{ a }' from '{ self.name }' process." )
				del self._threads[ a ]
				r[ a ]	=	True
				pass # END ELIF

			# Unexpected.
			else:
				logger.error( 'An unknown error has occurred.' )
				r[ a ]	=	None
				pass # END ELSE

			pass # END FOR

		return r

		pass # END METHOD : Remove thread entry

	def getChildThreads( self, *args ):
		'''

		Obtain child thread instance(s) based on queried names.

		Parameters
		----------
		*args : :obj:`str`
			Variable length argument list of child threads to return from the index located at :any:`Process._threads <polycephaly.core.process.Process._threads>`.

		Returns
		-------
		dict
			Name of the thread :obj:`String` as the key, and the value is :obj:`Thread` if found in the index or :obj:`None` if not found in the index.

		'''

		# Return all threads
		if not args:
			return self._threads
			pass # END IF

		return {
			str( threadName ) : (							# Key
				self._threads[ str( threadName ) ]			# Value is Thread instance if...
				if ( str( threadName ) in self._threads )	# Thread's name is in the index
				else None									# Otherwise, None.
			) for threadName in args
		}

		pass # END METHOD : Get threads

	def getChildThread( self, threadName ):
		'''

		Obtains a single instance from Process.getChildThreads().

		Parameters
		----------
		threadName : :obj:`str`
			Name of thread to look up.

		Returns
		-------
		Thread or None
			If a thread is found, :obj:`Thread` is returned, otherwise :obj:`None` is.

		'''

		return self.getChildThreads( threadName )[ threadName ]

		pass # END METHOD : Get child thread

	def listChildThreadsLives( self, *args ):
		'''

		Lists status of life for child thread instance(s) based on queried names.

		Parameters
		----------
		*args : :obj:`str`
			Variable length argument list of child threads to return from the index.

		Returns
		-------
		dict
			Will return :obj:`Boolean` if found in the index, or :obj:`None` if not found in the index.

		'''

		searches	=	[]
		threadNames	=	[]

		for a in args:

			# Search criteria : Boolean or None.
			if ( polycephaly.functions.utilities.getType( a ).upper() in [ 'BOOL', 'NONETYPE' ] ):
				searches.append( a )
				pass # END IF

			# Thread name
			else:
				threadNames.append( str( a ) )
				pass # END ELSE

			pass # END FOR : Iterate arguments

		r	=	{
					threadName : (																	# Key
						threadInstance.isAlive()													# Thread's life if...
						if isinstance( threadInstance, threading.Thread )							# Thread's name is in the index
						else None																	# Otherwise, None.
					)																				#
					for threadName, threadInstance in self.getChildThreads( *threadNames ).items()	# In thread names list.
				}

		# If search criteria has been given, match on that.  Otherwise, return the entire dictionary.
		return { threadName : threadStatus for threadName, threadStatus in r.items() if threadStatus in searches } if searches else r

		pass # END METHOD : List child thread lives

	def childThreadJanitor( self ):
		'''

		Automatically removes child threads that are stopped or non-existent, and can be used idempotently in :any:`life() <polycephaly.core.process.events.Extend.life>`.

		'''

		self.removeChildThreads(
			*self.listChildThreadsLives( False, None ).keys()
		)

		pass # END METHOD : Child Thread Janitor

	def joinChildThreads( self ):
		'''

		Used in :any:`Process.main() <polycephaly.core.process.setup.Extend.main>` and run immediately before :any:`Process.death() <polycephaly.core.process.events.Extend.death>`, this attempts to join each of the process' child threads that are still active.

		'''

		logger.debug( f"{ self.name }.joinChildThreads()" )

		# Attempt to join threads
		for threadName in self.listChildThreadsLives( True ).keys():

			logger.debug( f"Attaching to '{ self.name }' child thread '{ threadName }' and waiting for it to finish..." )
			self.getChildThread( threadName ).join()

			pass # END FOR

		pass # END METHOD : Join children to parent process

	pass # END CLASS : EXTEND

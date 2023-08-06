#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# System
import sys
import time

# Reflection / Debugging
import inspect

# Polycephaly
import polycephaly.functions.threading

# Logging
from logbook import Logger
from polycephaly.log import logger_group
logger = Logger( __loader__.name )
logger_group.add_logger( logger )

class Extend( object ):

	def cleanup( self ):
		'''

		Used by the Main process during its run of :any:`Process.die() <Extend.die>` to send the :any:`Poison Pill <polycephaly.core.process.Process._ppill>` to sub-processes that :any:`Process.activeSubProcesses() <polycephaly.core.process.info.Extend.activeSubProcesses>` reports as still active.

		'''

		# Frame info.
		curframe	=	inspect.currentframe()
		calframe	=	inspect.getouterframes( curframe, 2 )
		logger.debug( f"{ self.name }.{ calframe[ 0 ][ 3 ] }() called by { self.name }.{ calframe[ 1 ][ 3 ] }()" )

		# Send shutdown request to remaining processes.
		currProcessName	=	None	# Current process
		currMessage		=	None	# Message sent
		currReply		=	None	# Reply received

		for currProcessName in self.activeSubProcesses():

			logger.debug( f"{ self.name }.{ calframe[ 0 ][ 3 ] }() sending poison pill to '{ currProcessName }'." )

			# Send poison pill to sub-process.
			currMessage		=	self.send(
									recipient	=	currProcessName,
									subject		=	self._ppill,
									ppill		=	self._ppill,
									currMethod	=	[
														calframe[ 0 ][ 3 ],
														calframe[ 0 ][ 1 ],
													],
									callMethod	=	[
														calframe[ 1 ][ 3 ],
														calframe[ 1 ][ 1 ],
													],
								)

			# Wait for response from sub-process to confirm poison pill.
			currReply		=	self.waitForReply(
									currMessage,
									timeout		=	10,
								)

			if 'ppill' not in currReply:

				if currMessage[ 'recipient' ] in self.activeSubProcesses():
					logger.warning( f"'{ currMessage[ 'recipient' ] }' failed to respond in time, but is showing that it's still active." )
					pass # END IF

				else:
					logger.warning( f"'{ currMessage[ 'recipient' ] }' failed to respond in time, but is showing that it's now inactive." )
					pass # END ELSE

				pass # END IF

			elif currMessage[ 'ppill' ] == currReply[ 'ppill' ]:
				logger.info( f"Response to '{ self.name }' : { currMessage[ 'recipient' ] }.{ currReply[ 'callMethod' ][ 0 ] }() -> { currMessage[ 'recipient' ] }.{ currReply[ 'currMethod' ][ 0 ] }() is complete." )
				pass # END ELIF

			pass # END FOR : Shutdown each of the active processes.
		del currProcessName, currMessage, currReply

		pass # END METHOD : Clean-up

	def ebrake( self, reason=None ):
		'''

		Used by a process to request that the entire application be shutdown, which is usually caused by a process encountering an unrecoverable error.

		Parameters
		----------
		reason : :obj:`str`, optional
			Provides an explanation for why a process is requesting that the entire application be shutdown.

		'''

		# Frame info.
		curframe	=	inspect.currentframe()
		calframe	=	inspect.getouterframes( curframe, 2 )
		logger.critical( f"{ self.name }.{ calframe[ 0 ][ 3 ] }( reason='{ reason }' ) called by { self.name }.{ calframe[ 1 ][ 3 ] }()" )

		if self.name == self.nameMain:

			self.die( reason=reason )

			pass # END IF

		else:

			self.send(
				recipient=self.nameMain,
				subject='EBRAKE',
				reason=reason,
			)

			pass # END ELSE

		pass # END METHOD : Emergency Brake

	def die( self, message=None, **kwargs ):
		'''

		Commonly used as a callback that can detect internal events (Polycephaly messages) and external events (Signals), this is used by a process to shut itself down.

		Parameters
		----------
		message : :obj:`dict`, optional
			If called by a :any:`Polycephaly's Messenger <polycephaly.comms.messenger>` event, this variable will be populated with the message which allows for a reason to explain the shutdown and optionally responding to the sender to confirm the shutdown sequence.

		**kwargs

			Allows for other events to pass information for shutdown, which can include but are not limited to:

				* Signals
					* sigNum : (:obj:`int`, optional) - Signal Integer (e.g. 2 for SIGINT, 15 for SIGTERM, etc.)

				* Information
					* currFrame : (:obj:`frame`, optional) - Python `stack frame <https://stackoverflow.com/questions/23848391/what-is-the-difference-between-a-stack-and-a-frame>`_ information.
					* reason : (:obj:`str`, optional) - why this process is being shutdown.

		Returns
		-------
		bool
			True if successful, False if something went wrong.

		'''

		# Frame info.
		curframe	=	inspect.currentframe()
		calframe	=	inspect.getouterframes( curframe, 2 )
		logger.debug( f"{ self.name }.{ calframe[ 0 ][ 3 ] }() called by { self.name }.{ calframe[ 1 ][ 3 ] }()" )

		# Signals
		sigNum		=	kwargs.get( 'sigNum' )
		sigName		=	self.signalsDict( sigNum )

		# Debugging info.
		currFrame	=	kwargs.get( 'currFrame' )

		runLevel	=	self.runLevel()

		# Given a run level range, this is a normal shutdown.
		if ( runLevel is not None ) and ( 0 < runLevel < 7 ):

			reason	=	kwargs.get(
							'reason',											# Simple
							( message.get( 'reason' ) if message else None )	# Elaborate
						)
			reason	=	reason if reason else f"{ self.name }.{ calframe[ 1 ][ 3 ] }()"

			verboseInfo		=	f"{ self.name }.die():\n"

			# External (e.g. Operating System)
			if sigNum:

				verboseInfo		+=	"Triggered by an external event.\n"
				verboseInfo		+=	f"Signal { sigNum } ({ sigName }).\n"
				verboseInfo		+=	f"Current frame : { currFrame }" if currFrame else ""

				pass # END IF

			# Internal (e.g. Main or sub-process).
			else:

				verboseInfo		+=	"Triggered by an internal event.\n"
				verboseInfo		+=	f"Reason received: '{ reason }'"

				pass # END

			del reason

			if polycephaly.functions.threading.isApplicationMainThread():
				logger.critical( verboseInfo )
				pass # END IF

			else:
				logger.notice( verboseInfo )
				pass # END ELSE

			self.runLevel( 'CLEANUP' )

			# If this is the main process, activate clean-up (e.g. requesting sub-processes to shutdown).
			if polycephaly.functions.threading.isApplicationMainThread():
				self.cleanup()
				pass # END IF

			self.signalEnd	=	sigNum

			pass # END IF : A normal shutdown.

		# Something is wrong, but we've been asked to shutdown, so we're going to!
		else:

			if ( self.name == self.nameMain ) and self._runtime.forceStop:

				tempMessage	=	f"{ self.name } emergency exit via '{ sigName }'"
				tempMessage	+=	f", skipping shutdown procedures for remaining processes: { ', '.join( self.activeSubProcesses() ) }." if self.activeSubProcesses() else "."
				logger.critical( tempMessage )

				sys.exit()

				pass # END IF

			elif self._runtime.forceStop:
				logger.critical( f"{ self.name } : received '{ sigName }' while already shutting down, and is making an emergency exit." )
				sys.exit()
				pass # END ELSE IF

			else:
				logger.critical( f"{ self.name } : ignoring '{ sigName }', stop already in progress." )
				return False
				pass # END ELSE

			pass # END ELSE : An abnormal shutdown.

		self.isActive( False )

		# Respond to message
		if message:

			logger.debug( f"{ self.name }.{ calframe[ 0 ][ 3 ] }() replying to '{ message[ 'sender' ] }'." )

			self.reply(
				message,
				halting		=	True,
				currMethod	=	[
									calframe[ 0 ][ 3 ],
									calframe[ 0 ][ 1 ],
								],
				callMethod	=	[
									calframe[ 1 ][ 3 ],
									calframe[ 1 ][ 1 ],
								],
			)

			pass # END IF : MESSAGE

		return True

		pass # END METHOD : Die

	pass # END CLASS : EXTEND

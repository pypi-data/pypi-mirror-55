#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# System
import time

# Reflection / Debugging
import inspect

# Message Queues
from queue import Empty as queueEmpty

# Polycephaly
import polycephaly.functions.threading

# Logging
from logbook import Logger
from polycephaly.log import logger_group
logger = Logger( __loader__.name )
logger_group.add_logger( logger )

class Extend( object ):

	def getQueueMessage( self, mailboxQueue=None, **kwargs ):
		'''

		Retrieves a message from a message queue.

		Parameters
		----------
		mailboxQueue : :obj:`Threading.Queue` or :obj:`Multiprocessing.Queue`, optional
			Message queue to check.

		**kwargs
			Arbitrary keyword arguments passed directly to :any:`Messenger.getQueueMessage() <polycephaly.comms.messenger.actions.Extend.getQueueMessage>`.

		Returns
		-------
		return
			Directly passed from :any:`Messenger.getQueueMessage() <polycephaly.comms.messenger.actions.Extend.getQueueMessage>`.

		'''

		return self._messenger.getQueueMessage(
			caller			=	self.name,
			mailboxQueue	=	mailboxQueue,
			**kwargs
		)

		pass # END METHOD : Get Queue Message

	def mailman( self, route=None, message=None ):
		'''

		Retrieves the next message from the queue, and runs any associated callbacks tied to the process' :any:`message filters <polycephaly.core.process.messaging.filters>`.

		Parameters
		----------
		route : :obj:`str`, optional
			Allows for you to use separate routes, which filters and their reciprocal callbacks may exist on.

		message : :obj:`dict`, optional
			Allows for you to pass separate messages in from other buses (e.g. Unix Domain Socketfiles or MQTT).

		Returns
		-------
		return
			Directly passed from :any:`Messenger.mailman() <polycephaly.comms.messenger.actions.Extend.mailman>`.


		.. note::
			If you fail to include this method in :any:`Process.life() <polycephaly.core.process.events.Extend.life>`, it will be automatically run via its
			:any:`run flag <polycephaly.core.process.Process._ranMailman>`.  This is to ensure that each and every process receives critical messages
			such as the :any:`Poison Pill <polycephaly.core.process.Process._ppill>` if it's emitted as part of the shutdown process.

		'''

		self._ranMailman	=	True

		# Default use, when not being used to process messages from ROS, UDS, MQTT, et al.
		if route is None:
			route		=	self.name
			message		=	self.getQueueMessage( mailboxQueue=self.getQueue( self.name ) ) if ( message is None ) else message
			pass # END IF

		return self._messenger.mailman(
			caller		=	self.name,
			route		=	route,
			message		=	message,
		)

		pass # END METHOD : Mailman

	def send( self, **kwargs ):
		'''

		Sends a message to another process.

		Parameters
		----------
		**kwargs
			Arbitrary keyword arguments passed directly to :any:`Messenger.send() <polycephaly.comms.messenger.actions.Extend.send>` to form a message including adding in additional headers.

		Returns
		-------
		return
			Directly passed from :any:`Messenger.send() <polycephaly.comms.messenger.actions.Extend.send>`.

		'''

		curframe = inspect.currentframe()
		calframe = inspect.getouterframes( curframe, 2 )

		logger.debug( f"{ self.name }.{ calframe[ 0 ][ 3 ] }() called by { self.name }.{ calframe[ 1 ][ 3 ] }() in { calframe[ 1 ][ 1 ] }" )

		return self._messenger.send( caller=self.name, **kwargs )

		pass # END METHOD : Send

	def waitForReply( self, message, **kwargs ):
		'''

		Blocking event that's used for receiving a reply from a process that was just messaged.

		Parameters
		----------
		message : :obj:`dict`
			The message that was sent to another process, and what we are waiting for a reply to.

		**kwargs
			* **timeout** (:obj:`int`, optional, default: `5`) - Number of seconds to wait before giving up and returning :obj:`None`.

			* **ignoreLock** (:obj:`bool`, optional, default: `False`) - Normally, the internal message queue is locked when an operation is performed on it.  Specifically, to avoid a race condition that allows this method to sequentially refill the queue with any messages that aren't a reply to what we're waiting for.  You'll almost never want to disable this.

		Returns
		-------
		:obj:`dict` or :obj:`None`
			Message as a dictionary if successful, :obj:`None` if timed out or an error was experienced.

		'''

		# Frame info.
		curframe	=	inspect.currentframe()
		calframe	=	inspect.getouterframes( curframe, 2 )
		logger.debug( f"{ self.name }.{ calframe[ 0 ][ 3 ] }() called by { self.name }.{ calframe[ 1 ][ 3 ] }()" )

		reply		=	None
		q			=	self.getQueue( self.name )
		end			=	time.time() + kwargs.get( 'timeout', 5 )
		ignoreLock	=	True if kwargs.get( 'ignoreLock' ) else False

		if not ignoreLock:
			self.getLocks( 'queue' ).acquire()
			pass # END IF

		messages	=	[]

		while time.time() < end:

			try:

				reply	=	self.getQueueMessage( mailboxQueue = q )
				logger.debug( f"{ self.name }.{ calframe[ 0 ][ 3 ] }() : reply for '{ self.name }' queue : { reply }" )

				# Nothing has come through yet.
				if not reply:
					time.sleep( 1 )
					continue
					pass # END IF

				# Reply found.
				elif (
					message[ 'threadid' ] == reply[ 'threadid' ]
					and
					message[ 'threadindex' ] == ( reply[ 'threadindex' ] - 1 )
				):
					logger.debug( f"{ self.name }.{ calframe[ 0 ][ 3 ] }() : reply found." )
					break
					pass # END IF

				# Save for restoring queue.
				else:
					messages.append( reply )
					pass # END ELSE

				pass # END TRY

			except queueEmpty:
				reply	=	None
				time.sleep( 1 )
				continue
				pass # END EXCEPT

			pass # END WHILE

		# Continue backing up messages from queue
		while not q.empty():
			messages.append( q.get() )
			pass # END

		# Restore queue for mailman to resume
		[ q.put( m ) for m in messages ]

		if not ignoreLock:
			self.getLocks( 'queue' ).release()
			pass # END IF

		return reply

		pass # END METHOD : Wait for reply

	def reply( self, message, **kwargs ):
		'''

		Used in message filter callbacks, and allows for an immediate response to an inbound message.

		Parameters
		----------
		message : :obj:`dict`
			The message that was received by another process.

		**kwargs
			Arbitrary keyword arguments added to a reply's message headers.

			Please note, there are reserved keywords that are used by this method:

			* **subject** (:obj:`str`, optional, default: `reply`) - Can be used to override the standard message subject when replying.

		Returns
		-------
		:obj:`dict`
			Message from :any:`Messenger.send() <polycephaly.comms.messenger.actions.Extend.send>`.

		'''

		# Flip recipient and sender
		message.update({
			'recipient'	:	message.get( 'sender' ),
			'sender'	:	message.get( 'recipient' ),
			'subject'	:	kwargs.get( 'subject', 'reply' )
		})

		for k in [
			'messageid',
			'time',
		]:
			if k in message:
				del message[ k ]
				pass # END IF
			pass # END FOR

		message	=	{
						**message,
						**kwargs,
					}

		return self._messenger.send(
			caller=self.name,
			**message,
		)

		pass # END METHOD : Reply

	pass # END CLASS : Extend

#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# System
import time

# Reflection / Debugging
import inspect
import traceback

# Types
import uuid

# Message Queues
from queue import Full as queueFull

# Polycephaly
import polycephaly.functions.utilities

# Formatting
from pprint import pformat as pf

# Logging
from logbook import Logger
from polycephaly.log import logger_group
logger = Logger( __loader__.name )
logger_group.add_logger( logger )

class Extend( object ):

	def getQueueMessage( self, caller=None, mailboxQueue=None, **kwargs ):
		'''

		Retrieves a message from a message queue.

		Parameters
		----------
		caller : :obj:`str`, optional
			Process that's calling this method.

		mailboxQueue : :obj:`Threading.Queue` or :obj:`Multiprocessing.Queue`, optional
			Message queue to check.

		**kwargs
			Arbitrary keyword arguments that allow additional headers to be added onto the message.

		Returns
		-------
		dict
			Single message from queue.

		'''

		# Frame info.
		curframe	=	inspect.currentframe()
		calframe	=	inspect.getouterframes( curframe, 2 )
		logger.debug( f"{ calframe[ 0 ][ 3 ] }() called by { calframe[ 1 ][ 3 ] }()" )

		msg	=	{}

		try:

			# Locate caller in queues.
			if ( caller not in self.listQueues() ) and not mailboxQueue:
				raise KeyError( f"'{ caller }' queue doesn't exist." )
				pass # END IF

			# Current queue for caller.
			mailboxQueue	=	mailboxQueue if mailboxQueue else self.getQueue( caller )

			# Queue not empty
			if not mailboxQueue.empty():

				msg	=	mailboxQueue.get()		# Get message

				logger.debug( f"{ calframe[ 0 ][ 3 ] }( caller='{ caller }', mailboxQueue='{ pf( mailboxQueue ) }' ) received { pf( msg ) }" )

				msg	=	{
							**msg,
							**kwargs,
						}

				pass # END IF : QUEUE NOT EMPTY

			pass # END TRY

		except Exception as e:

			logger.warning( e )
			logger.warning( traceback.format_exc() )

			msg		=	{
							**{
								'sender'			:	caller,
								'recipient'			:	caller,
								'action'			:	calframe[ 0 ][ 3 ],
								'failed'			:	True,
								'body'				:	msg,
								'e'					:	e,
								'traceback'			:	traceback.format_exc(),
							},
							**kwargs,
						}

			pass # END EXCEPTION

		finally:
			return msg
			pass # END

		pass # END METHOD : Get Queue Message

	def _relay( self, caller, route, message ):
		'''

		Used by :any:`Messenger.mailman() <polycephaly.comms.messenger.actions.Extend.mailman>` to relay messages between sub-processes.

		Parameters
		----------

		caller : :obj:`str`
			Process that's calling this method.

		route : :obj:`str`
			Route to check filters on.

		message : :obj:`dict`
			Message to move to queue.

		'''

		relayer	=	message.pop( 'queue', None )

		q		=	self.getQueue( message[ 'recipient' ] )

		message.update({
			'relayer'	:	relayer,
			'queue'		:	(
								message[ 'recipient' ],
								str( q ),
							),
		})

		q.put(
			message,	# Data
			True,		# Block
			5			# Timeout
		)

		pass # END METHOD : Relay

	def mailman( self, caller, route=None, message=None ):
		'''

		Checks for a new message, runs callbacks for any filters that match against this message.

		Parameters
		----------
		caller : :obj:`str`, optional
			Process that's calling this method.

		route : :obj:`str`, optional
			Route to check filters on.

		message : :obj:`dict`, optional
			Message to check filters against.

		Returns
		-------
		bool or None
			* `True` - message received and matched against 1 or more filters.
			* `None` - no message was received.
			* `False` - no filters matched this message.

		'''

		# Empty dictionary
		if not message:
			return None
			pass # END IF

		logger.debug( f"mailman( caller={ caller }, route={ route }, message={ pf( message ) } )" )

		'''
		Relay message via the Main process.

		Optionally, this could go on the monkey-patching side of the Process class,
		but then it's more of a dance for unit testing, etc.
		'''
		if (
			( caller == self.nameMain )				# Main process is being used
			and
			( caller == route )						# Internal messaging bus
			and
			( caller != message[ 'recipient' ] )	# This is a relayed message via the main process
		):
			return self._relay( caller, route, message )
			pass # END IF

		currMatchCBs		=	self.matchFilter(
									caller=caller,
									route=route,
									message=message,
								)
		currMatchCBs_size	=	len( currMatchCBs )

		if not currMatchCBs_size:
			logger.warning( f"No filters were found for '{ caller }' process to match message:\n\n{ pf( message ) }" )
			return False
			pass # END IF

		for i, currCB in enumerate( currMatchCBs ):

			try:
				logger.debug( f"{ caller } filter { i+1 } / { currMatchCBs_size } : { currCB.__name__ }() : running." )
				currCB( message )
				logger.debug( f"{ caller } filter { i+1 } / { currMatchCBs_size } : { currCB.__name__ }() : finished." )
				pass # END

			except Exception as e:

				logger.error( f"{ caller } filter { i+1 } / { currMatchCBs_size } : { currCB.__name__ }() : failed : { e }." )
				logger.error( traceback.format_exc() )

				pass # END

			pass # END FOR

		return True

		pass # END METHOD : Mailman

	def _sendRoute( self, kwargs, recipientType, recipientQueue ):
		'''

		Used by :any:`Messenger.send() <polycephaly.comms.messenger.actions.Extend.send>` to determine which queue to place messages into.

		Parameters
		----------

		kwargs : :obj:`dict`

			Reserved keywords:

				* sender (:obj:`str`) - Message sender.
				* recipient (:obj:`str`) - Message recipient.

		recipientType : :obj:`str` or :obj:`queue`
			Passed from send(), and determined by recipient.

		recipientQueue : :obj:`queue`
			Used for placing messages into.

		'''

		qName			=	None	# Name (e.g. `main`)
		q				=	None	# Object

		# Message to self
		if ( kwargs[ 'sender' ] == kwargs[ 'recipient' ] ):

			qName	=	kwargs[ 'recipient' ]
			q		=	recipientQueue

			pass # END IF

		# Use Main process' queue
		elif (

			# Sender needs Main to relay to Recipient.
			(
				kwargs[ 'recipient' ] != self.nameMain
				and
				kwargs[ 'sender' ] != self.nameMain
			)

			or

			# Recipient is Main.
			kwargs[ 'recipient' ] == self.nameMain

		):

			logger.debug( f"Using main process '{ self.nameMain }' queue to route a message from '{ kwargs[ 'sender' ] }' to '{ kwargs[ 'recipient' ] }'." )

			qName	=	self.nameMain
			q		=	self.getQueue( self.nameMain )

			pass # END ELSE IF

		# Direct queue access
		elif recipientQueue:

			if recipientType == 'STR':

				qName	=	kwargs[ 'recipient' ]

				pass # END IF

			elif recipientType == 'QUEUE':

				qName	=	'Direct Queue'

				pass # END ELSE

			q		=	recipientQueue

			pass # END ELSE IF

		else:

			logger.error( f"Unable to route message: '{ kwargs[ 'sender' ] }' => '{ kwargs[ 'recipient' ] }'" )

			pass # END ELSE

		# Returns tuple containing desired queue.
		return ( qName, q, )

		pass # END METHOD : Send route

	def send( self, caller, **kwargs ):
		'''

		Sends (or relays) a message between processes.

		Parameters
		----------
		caller : :obj:`str`, optional
			Process that's calling this method.

		**kwargs
			Arbitrary keyword arguments which form a message, including adding in additional headers.

		Returns
		-------
		dict
			Message that's been sent.

		'''

		# Frame info.
		curframe	=	inspect.currentframe()
		calframe	=	inspect.getouterframes( curframe, 2 )

		kwargs.update({
			'recipient'	:	kwargs[ 'recipient' ].lower(),
			'sender'	:	kwargs.get( 'sender', caller ).lower(),
			'messageid'	:	str( uuid.uuid4() ),
			'time'		:	time.time(),
			'threadid'	:	kwargs.get( 'threadid', str( uuid.uuid4() ) )
		})

		# Recipient to place message into.
		recipientType	=	polycephaly.functions.utilities.getType( kwargs[ 'recipient' ] ).upper()

		for case in polycephaly.functions.utilities.switch( recipientType ):

			if case( 'STR' ):
				recipientQueue	=	self.getQueue( kwargs[ 'recipient' ] )
				break

			if case( 'QUEUE' ):
				recipientQueue	=	kwargs[ 'recipient' ]
				break

			if case():
				recipientQueue	=	None
				break

			pass # END SWITCH

		# Returns appropriate queue's name and object.
		qName, q		=	self._sendRoute( kwargs, recipientType, recipientQueue )

		# Allows us to trace message path for debugging.
		kwargs.update({
			'queue'		:	(
								str( qName ),
								str( q ),
							),
		})

		if q:

			# If applicable, add thread index
			if kwargs.get( 'threadid' ):
				kwargs.update({
					'threadindex'	:	( kwargs.get( 'threadindex', 0 ) + 1 )
				})
				pass # END IF

			# Add message to queue
			try:

				logger.debug( f"{ calframe[ 0 ][ 3 ] }() : added message to queue:\nQueue   : '{ qName }' : { q }\nCaller  : '{ caller }'\nFrom    : '{ kwargs[ 'sender' ] }'\nTo      : '{ kwargs[ 'recipient' ] }'\nMessage :\n{ pf( kwargs ) }" )

				# Add to message queue
				q.put(
					kwargs,		# Data
					True,		# Block
					5			# Timeout
				)

				pass # END TRY

			except queueFull:
				logger.error( f"Unable to add message to '{ qName }' queue due to it being full." )
				return False
				pass # END EXCEPTION

			pass # END IF

		return kwargs

		pass # END METHOD : SEND

	pass # END CLASS : Polycephaly Messenger

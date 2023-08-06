#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# System
import time

# Testing
import pytest

# Polycephaly
from polycephaly.comms.messenger import Messenger

@pytest.fixture
def pcm():
	'''
	'''

	pcmi	=	Messenger(
					nameMain		=	'm1',
					queueType		=	'FIFO',
					queueSize		=	10,
				)

	try:

		# Add queues for 2 forked processes
		pcmi.addQueues( 'Multiprocessing', 'm1', 'm2' )

		# Add queues for 2 threads
		pcmi.addQueues( 'Threading', 't1', 't2' )

		pass # END TRY

	except Exception as e:
		pass # END EXCEPTION

	# Check for existence of queues.
	assert pcmi.listQueues() == ['m1', 'm2', 't1', 't2']

	return pcmi

	pass # END INSTANTIATION : Polycephaly Messenger

def sendMessages( pcm ):

	# Send all possible combinations, and then check the routes that were taken.
	messagePaths	=	[]

	availableQueues	=	pcm.listQueues()

	for sender, recipient in [ ( x, y ) for x in availableQueues for y in availableQueues ]:

		testMessage		=	{
								'sender'	:	sender,
								'recipient'	:	recipient,
								'subject'	:	f'{ sender } => { recipient }',
								'body'		:	f'Read by { recipient }',
							}

		# Send message
		message			=	pcm.send( caller=testMessage[ 'sender' ], **testMessage )

		# Paths dictated by Messenger.send()
		messagePaths.append({
			's' : message[ 'sender' ],
			'r' : message[ 'recipient' ],
			'q' : message[ 'queue' ][ 0 ],
		})

		pass # END FOR

	return messagePaths

	pass # END FUNCTION : Send messages

def test_sendMessages( pcm ):

	messagePaths	=	sendMessages( pcm )

	assert messagePaths == [
			{ 's': 'm1', 'r': 'm1', 'q': 'm1' },
			{ 's': 'm1', 'r': 'm2', 'q': 'm2' },
			{ 's': 'm1', 'r': 't1', 'q': 't1' },
			{ 's': 'm1', 'r': 't2', 'q': 't2' },
			{ 's': 'm2', 'r': 'm1', 'q': 'm1' },
			{ 's': 'm2', 'r': 'm2', 'q': 'm2' },
			{ 's': 'm2', 'r': 't1', 'q': 'm1' },
			{ 's': 'm2', 'r': 't2', 'q': 'm1' },
			{ 's': 't1', 'r': 'm1', 'q': 'm1' },
			{ 's': 't1', 'r': 'm2', 'q': 'm1' },
			{ 's': 't1', 'r': 't1', 'q': 't1' },
			{ 's': 't1', 'r': 't2', 'q': 'm1' },
			{ 's': 't2', 'r': 'm1', 'q': 'm1' },
			{ 's': 't2', 'r': 'm2', 'q': 'm1' },
			{ 's': 't2', 'r': 't1', 'q': 'm1' },
			{ 's': 't2', 'r': 't2', 'q': 't2' },
		]

	pass # END TEST : Send messages

def test_messageQueues( pcm ):

	queueMessages	=	{}
	for qName in pcm.listQueues():

		qInst					=	pcm.getQueue( qName )
		queueMessages[ qName ]	=	[]

		while not qInst.empty():

			tempD	=	{ k[ 0 ] : v for k,v in pcm.getQueueMessage( qName ).items() if k in [
							'sender',
							'recipient',
							'queue',
						] }
			tempD[ 'q' ]	=	tempD[ 'q' ][ 0 ]

			queueMessages[ qName ].append( tempD )

			del tempD

			pass # END WHILE LOOP

		pass # END FOR : Iterate queues

	assert queueMessages == {
		'm1'	:	[
						{'s': 'm1', 'r': 'm1', 'q': 'm1'},
						{'s': 'm2', 'r': 'm1', 'q': 'm1'},
						{'s': 'm2', 'r': 't1', 'q': 'm1'},
						{'s': 'm2', 'r': 't2', 'q': 'm1'},
						{'s': 't1', 'r': 'm1', 'q': 'm1'},
						{'s': 't1', 'r': 'm2', 'q': 'm1'},
						{'s': 't1', 'r': 't2', 'q': 'm1'},
						{'s': 't2', 'r': 'm1', 'q': 'm1'},
						{'s': 't2', 'r': 'm2', 'q': 'm1'},
						{'s': 't2', 'r': 't1', 'q': 'm1'},
					],
		'm2'	:	[
						{'s': 'm1', 'r': 'm2', 'q': 'm2'},
						{'s': 'm2', 'r': 'm2', 'q': 'm2'},
					],
		't1'	:	[
						{'s': 'm1', 'r': 't1', 'q': 't1'},
						{'s': 't1', 'r': 't1', 'q': 't1'},
					],
		't2'	:	[
						{'s': 'm1', 'r': 't2', 'q': 't2'},
						{'s': 't2', 'r': 't2', 'q': 't2'},
					]
	}

	pass # END TEST : Message paths

def test_mailmanQueues( pcm ):
	'''
	'''

	sendMessages( pcm )

	queueMessages	=	{}
	for qName in pcm.listQueues():

		qInst					=	pcm.getQueue( qName )
		queueMessages[ qName ]	=	[]

		while not qInst.empty():

			message	=	pcm.getQueueMessage( mailboxQueue=pcm.getQueue( qName ) )

			mailman	=	pcm.mailman(
							caller	=	qName,
							route	=	qName,
							message	=	message,
						)

			if mailman != None:

				message	=	{
								k : v for k, v in message.items()
								if k in [
									'sender',
									'recipient',
									'subject',
									'queue',
									'relayer',
								]
							}

				for k,v in message.copy().items():
					if k in [ 'queue', 'relayer', ]:
						message[ k ]	=	v[ 0 ]
						pass # END IF
					pass # END FOR

				queueMessages[ qName ].append( message )

				pass # END IF

			pass # END WHILE LOOP

		pass # END FOR : Iterate queues

	assert queueMessages == {
		'm1'	:	[
						{'sender': 'm1', 'recipient': 'm1', 'subject': 'm1 => m1', 'queue': 'm1'},
						{'sender': 'm2', 'recipient': 'm1', 'subject': 'm2 => m1', 'queue': 'm1'},
						{'sender': 't1', 'recipient': 'm1', 'subject': 't1 => m1', 'queue': 'm1'},
						{'sender': 't2', 'recipient': 'm1', 'subject': 't2 => m1', 'queue': 'm1'},
					],
		'm2'	:	[
						{'sender': 'm1', 'recipient': 'm2', 'subject': 'm1 => m2', 'queue': 'm2'},
						{'sender': 'm2', 'recipient': 'm2', 'subject': 'm2 => m2', 'queue': 'm2'},
						{'sender': 't1', 'recipient': 'm2', 'subject': 't1 => m2', 'relayer': 'm1', 'queue': 'm2'},
						{'sender': 't2', 'recipient': 'm2', 'subject': 't2 => m2', 'relayer': 'm1', 'queue': 'm2'},
					],
		't1'	:	[
						{'sender': 'm1', 'recipient': 't1', 'subject': 'm1 => t1', 'queue': 't1'},
						{'sender': 't1', 'recipient': 't1', 'subject': 't1 => t1', 'queue': 't1'},
						{'sender': 'm2', 'recipient': 't1', 'subject': 'm2 => t1', 'relayer': 'm1', 'queue': 't1'},
						{'sender': 't2', 'recipient': 't1', 'subject': 't2 => t1', 'relayer': 'm1', 'queue': 't1'},
					],
		't2'	:	[
						{'sender': 'm1', 'recipient': 't2', 'subject': 'm1 => t2', 'queue': 't2'},
						{'sender': 't2', 'recipient': 't2', 'subject': 't2 => t2', 'queue': 't2'},
						{'sender': 'm2', 'recipient': 't2', 'subject': 'm2 => t2', 'relayer': 'm1', 'queue': 't2'},
						{'sender': 't1', 'recipient': 't2', 'subject': 't1 => t2', 'relayer': 'm1', 'queue': 't2'},
					],
	}

	pcm.removeQueues( 'm1', 'm2', 't1', 't2', )

	pass # END TEST : Mailman

#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# Testing
import pytest

# Queue
from queue import Queue as queueThread
from multiprocessing import Queue as queueProcess
from multiprocessing.queues import Queue as queueProcessType
from queue import Full as queueFull

# Polycephaly
from polycephaly.comms.messenger import Messenger

@pytest.fixture
def pcm():
	'''
	'''

	return Messenger(
		nameMain		=	'testing',
		defaultCaller	=	'testing',
		defaultRoute	=	'testing',
		queueType		=	'FIFO',
		queueSize		=	10,
	)

	pass # END INSTANTIATION : Polycephaly Messenger

@pytest.mark.parametrize(
	"		queueType,				expected",
	[
		(	'AsyncIO',				queueProcessType	),
		(	'Thread',				queueThread			),
		(	'Multiprocessing',		queueProcessType	),
		(	'Popen',				queueProcessType	),
		(	'Fail',					None				),
	]
)
def test_addTypes( pcm, queueType, expected ):
	'''
	'''

	if queueType != 'Fail':

		q	=	pcm.addQueue( queueType, queueType )
		t	=	type( q )

		assert queueType.lower() in pcm.listQueues()
		assert queueType.lower() in pcm.getQueue( queueType, 'Key' )
		assert q == pcm.getQueue( queueType )

		assert t == expected

		pass # END IF

	else:

		with pytest.raises( ValueError ) as e_info:
			pcm.addQueue( queueType, queueType )

		assert str( e_info.value ) == "Unknown queue mode : 'F'."

		assert queueType.lower() not in pcm.listQueues()
		assert pcm.getQueue( queueType, 'Key' ) == None

		pass # END ELSE

	pass # END TEST : Add unsupported queue type

def test_multiple( pcm ):
	'''
	'''

	# Add queues of threading type with a size of 7.
	pcm.addQueues(
		'Thread',
		'Test1',
		'Test2',
		size=7,
	)

	# Add queues of multiprocessing type with a size of 9.
	pcm.addQueues(
		'Multiprocessing',
		'Test3',
		'Test4',
		size=9,
	)

	# Check sizes
	assert pcm.getQueue( 'test1' ).maxsize == 7
	assert pcm.getQueue( 'test4' )._maxsize == 9

	# Check creation
	for qName, qInstance in pcm.getQueues( 'test1', 'test2', 'test3', 'test4', ).items():

		assert qName in [

			'test1',
			'test2',
			'test3',
			'test4',

		]

		assert type( qInstance ) in [ queueThread, queueProcessType ]

		pass # END

	pass # END TEST : Add multiple

def test_addDuplicate( pcm ):
	'''
	'''

	pcm.addQueue( 'Testing', 'Thread' )

	with pytest.raises( KeyError ) as e_info:
		pcm.addQueue( 'Testing', 'Multiprocessing' )

	assert str( e_info.value ) == "'Message queue already exists.'"

	pass # END TEST : Add duplicate queue name

def test_maxMessages( pcm ):
	'''
	'''

	qMax5		=	pcm.addQueue( 'Max5', 		'Thread',			size=5	)
	qMaxDefault	=	pcm.addQueue( 'MaxDefault',	'Multiprocessing'			)

	# Local instance
	with pytest.raises( queueFull ) as e_info:
		for i in range( qMax5.maxsize + 1 ):
			qMax5.put( i, False )

	# Class default
	with pytest.raises( queueFull ) as e_info:
		for i in range( pcm._defSize + 1 ):
			qMaxDefault.put( i, False )

	pass # END TEST : Maximum messages in queue

def test_removeQueues( pcm ):
	'''
	'''

	assert pcm.removeQueue( 'Testing' ) == True

	assert pcm.removeQueue( 'Fail' ) == None

	assert pcm.removeQueues(

		'asyncio',
		'thread',
		'multiprocessing',
		'popen',
		'fail',

		'max5',
		'maxdefault',

		'test1',
		'test2',
		'test3',
		'test4',

	) == {

		'asyncio'			:	True,
		'thread'			:	True,
		'multiprocessing'	:	True,
		'popen'				:	True,
		'fail'				:	None,

		'max5'				:	True,
		'maxdefault'		:	True,

		'test1'				:	True,
		'test2'				:	True,
		'test3'				:	True,
		'test4'				:	True,
	}

	# Remove all queues
	pcm.removeQueues( *pcm.listQueues() )

	assert pcm.listQueues() == []

	pass # END TEST : Remove Queues

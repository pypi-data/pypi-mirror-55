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
		pcmi.addQueues( 'Multiprocessing', 'm1' )

		# Add queues for 2 threads
		pcmi.addQueues( 'Threading', 't1' )

		pass # END TRY

	except Exception as e:
		pass # END EXCEPTION

	return pcmi

	pass # END INSTANTIATION : Polycephaly Messenger

def test_noMessages( pcm ):

	# No message received.
	assert None == pcm.mailman(
		caller		=	'm1',
		route		=	'm1',
		message		=	pcm.getQueueMessage( mailboxQueue=pcm.getQueue( 'm1' ) ),
	)

	pass # END CALLBACK

def test_noMatches( pcm ):

	message			=	pcm.send(
							caller		=	't1',
							recipient	=	'm1',
						)

	time.sleep( 1 )

	# Message received, no matches found.
	assert False == pcm.mailman(
		caller		=	'm1',
		route		=	'm1',
		message		=	pcm.getQueueMessage( mailboxQueue=pcm.getQueue( 'm1' ) ),
	)

	pass # END TEST

def dummyCallback( message ):
	print( message )
	pass # END CALLBACK

@pytest.mark.parametrize(
	"field",
	[
		'subject',
		'body',
		'other',
	]
)
def test_filterMatch( pcm, field ):

	filterKWargs	=	{ field : 'testing' }

	pcm.addFilter(
		caller		=	'm1',
		route		=	'm1',
		callback	=	dummyCallback,
		**filterKWargs
	)

	assert dummyCallback is next( iter( pcm.listFilters(
		caller		=	'm1',
		route		=	'm1',
	) ) )[ 'callback' ]

	message			=	pcm.send(
							caller		=	't1',
							recipient	=	'm1',
							**filterKWargs
						)

	assert next( iter( pcm.matchFilter(
		caller		=	'm1',
		route		=	'm1',
		message		=	message,
	) ) ) is dummyCallback

	# Message received, matched >= 1 filters.
	assert True == pcm.mailman(
		caller		=	'm1',
		route		=	'm1',
		message		=	pcm.getQueueMessage( mailboxQueue=pcm.getQueue( 'm1' ) ),
	)

	pass # END TEST: Filter match

def test_fallThrough( pcm ):

	pcm.addFilter(
		caller		=	'm1',
		route		=	'm1',
		callback	=	lambda message: print( message ),
	)

	message			=	pcm.send(
							caller		=	't1',
							recipient	=	'm1',
							subject		=	'testing',
						)

	# Message received, no matches, fall-through.
	assert True == pcm.mailman(
		caller		=	'm1',
		route		=	'm1',
		message		=	pcm.getQueueMessage( mailboxQueue=pcm.getQueue( 'm1' ) ),
	)

	pass # END TEST: Fall-through

def test_removeFilters( pcm ):

	pcm.removeFiltersByID(
		caller	=	'm1',
		route	=	'm1',
		*[ d[ 'id' ] for d in pcm.listFilters( caller='m1', route='m1' ) ]
	)

	assert pcm.listFilters() == {
		'm1'	:	{
						'm1'	:	[]
					}
	}

	assert not pcm.listFilters( caller='m1', route='m1' )

	pass # END TEST : Remove filters

#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# Testing
import pytest

# Polycephaly
from polycephaly.comms.messenger import Messenger

def test_instantiationName():

	# Included required main process name.
	assert Messenger( nameMain = 'testing' )

	# Skipped required main process name.
	with pytest.raises( KeyError ) as e_info:
		assert Messenger()
	assert str( e_info.value ) == "'nameMain'"

	pass # END

def test_instantiationQueueType():

	# Supported queue types
	assert Messenger( nameMain = 'testing', queueType = 'FIFO' )
	assert Messenger( nameMain = 'testing', queueType = 'Priority' )

	# Unsupported queue type
	with pytest.raises( ValueError ) as e_info:
		assert Messenger( nameMain = 'testing', queueType = 'testing' )
	assert str( e_info.value ) == "Invalid queue type."

	pass # END

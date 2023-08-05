#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# System
import time

# Calculations
import math

# Reflection / Debugging
import inspect

# Logging
from logbook import Logger
from polycephaly.log import logger_group
logger = Logger( __loader__.name )
logger_group.add_logger( logger )

class Extend( object ):

	def frequency( self, i=None ):
		'''

		Sets or queries the frequency of the process.

		Parameters
		----------
		i : :obj:`int`, optional
			Sets the number of times per second that a process should attempt to run.

		Returns
		-------
		int
			Returns the process' frequency.

		'''

		if i:
			self._runtime.frequency	=	i
			pass # END IF

		return self._runtime.frequency

		pass # END METHOD : Frequency

	def freqSleep( self, multiplier=1 ):
		'''

		Frequency that should sleep

		Parameters
		----------
		multiplier : :obj:`int`, optional
			Multiplier can be used to extend the sleep time without changing the frequency.

			Example: if you wanted to double the time, set the value to 2.

		'''

		time.sleep( ( 1 / self.frequency() ) * multiplier )

		pass # END METHOD : Frequency sleep

	def lightSleeper( self, **kwargs ):
		'''

		Sleep timer that can be interrupted by a condition matched against a callback.

		Parameters
		----------
		**kwargs

			* **sleep** (:obj:`int`) - number of seconds to sleep.

			* **callback** (:obj:`Method` or :obj:`Function`) - callback that's evaluated once per second.

			* **conditional** (:obj:`Variable`) - when this variable is different from the callback's return, then sleep will be interrupted.

		Returns
		-------
		bool
			True if successful sleep, False if woken up early.


		.. seealso::

			:any:`Thread Spinner <../examples/threadSpinner/launch>` in the :any:`Examples <../examples/index>` directory, which makes use of this method in conjunction with :any:`Process.isActive() <polycephaly.core.process.info.Extend.isActive>`.

		'''

		curframe = inspect.currentframe()
		calframe = inspect.getouterframes(curframe, 2)

		sleep		=	kwargs[ 'sleep' ]
		callback	=	kwargs[ 'callback' ]
		conditional	=	kwargs.get( 'conditional', True )

		# for i in range( math.ceil( sleep ) ):
		sleep	=	1 if ( sleep < 1 ) else round( sleep )

		for i in range( sleep ):

			if callback() != conditional:
				logger.info( f'{ self.name }.{ calframe[ 0 ][ 3 ] }() being used in { self.name }.{ calframe[ 1 ][ 3 ] }() : callback condition has changed, waking up early.' )
				return False
				pass # END IF

			time.sleep( 1 )
			pass # END FOR

		return True

		pass # END METHOD : Light sleeper

	def currentFrame( self ):
		'''

		Returns the current frame within the span of a second from :any:`Process._currFrame <polycephaly.core.process.Process._currFrame>`, which is constantly updated in :any:`Process.main() <polycephaly.core.process.setup.Extend.main>`.

		For example, if the :any:`Process.frequency() <polycephaly.core.process.timing.Extend.frequency>` of this process is 30 and you're 0.5 seconds into the run, the current frame would be 15.

		Returns
		-------
		int
			The current frame.

		'''

		return self._currFrame

		pass # END METHOD

	def currentTimeFrame( self ):
		'''

		Similar to :any:`Process.currentFrame() <polycephaly.core.process.timing.Extend.currentFrame>`, this method attempts to calculate which frame in a second that the process is operating.

		Returns
		-------
		int
			The current frame.

		'''

		t	=	time.time()
		d	=	( t - math.floor( t ) )

		return math.floor( self.frequency() * d )

		pass # END

	pass # END CLASS : EXTEND

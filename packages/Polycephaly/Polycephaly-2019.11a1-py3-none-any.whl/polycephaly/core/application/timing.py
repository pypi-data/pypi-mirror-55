#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# Logging
from logbook import Logger
from polycephaly.log import logger_group
logger = Logger( __loader__.name )
logger_group.add_logger( logger )

class Extend( object ):

	def globalFrequency( self, i=None ):
		'''

		Get/Set global frequency for the application, which serves as a skeleton value when set in :any:`Application.build() <polycephaly.core.application.events.Extend.build>`

		Returns
		-------
		int
			The current global frequency.

		'''

		if i:
			logger.debug( f'Setting default runtime frequency to { i }.' )
			self._skel.runtime[ 'frequency' ]	=	i
			pass # END IF

		return self._skel.runtime[ 'frequency' ]

		pass # END METHOD : Get / Set frequency

	pass # END CLASS : EXTEND

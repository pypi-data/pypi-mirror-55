#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# Reflection / Debugging
import inspect

# Logging
from logbook import Logger
from polycephaly.log import logger_group
logger = Logger( __loader__.name )
logger_group.add_logger( logger )

class Extend( object ):

	def __subProcInfo( self, message ):
		'''

		This is a callback method for looking up process information.  A message is received, where the body of the message is the :any:`Application <polycephaly.core.application>` method to use (e.g. :any:`Application.activeSubProcesses() <polycephaly.core.application.info.Extend.activeSubProcesses>`), and the results will be sent back as a reply.

		Parameters
		----------
		message : :obj:`dict`

		'''

		self.reply(
			message,
			body	=	getattr( self.getApp(), message[ 'body' ] )(),
		)

		pass # END MESSAGE CALLBACK : Sub-Process Information

	pass # END CLASS : EXTEND

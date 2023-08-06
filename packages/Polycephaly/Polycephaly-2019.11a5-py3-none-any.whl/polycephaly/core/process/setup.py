#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# Reflection / Debugging
import traceback

# Polycephaly
import polycephaly.functions.threading

# Logging
from logbook import Logger
from polycephaly.log import logger_group
logger = Logger( __loader__.name )
logger_group.add_logger( logger )

class Extend( object ):

	def main( self, *args, **kwargs ):
		'''

		This method is responsible for the entire run of a process from start to stop, and most notably runs the sequence of:

		#. :any:`Process.birth() <polycephaly.core.process.events.Extend.birth>`
		#. :any:`Process.life() <polycephaly.core.process.events.Extend.life>` - runs in a loop so long as :any:`Process.isActive() <polycephaly.core.process.info.Extend.isActive>` evaluates to `True`.
		#. :any:`Process.death() <polycephaly.core.process.events.Extend.death>`

		Parameters
		----------
		*args
			Variable length argument list passed from process setup.

		**kwargs
			Arbitrary keyword arguments passed from process setup.  Reserved keywords that are used by this argument are:

			* **application** (:obj:`Application <polycephaly.core.application.Application>`) - the application instance is the lowest level of the program, which can be accessed from within a process by :any:`Process.getApp() <polycephaly.core.process.info.Extend.getApp>`.


		.. seealso::

			* :any:`Application.run() <polycephaly.core.application.setup.Extend.run>` refers to this method for creating the main process.
			* :any:`Application._createProcessInstance() <polycephaly.core.application.setup.Extend._createProcessInstance>` refers to this method for creating sub-processes.

		'''

		self._application	=	kwargs.pop( 'application' )

		logger.info( f"{ self.name }.main() started." )

		self.runLevel( 'BUILDUP' )

		logger.debug( f"{ self.name }.birth() starting." )
		self.birth()
		logger.debug( f"{ self.name }.birth() finished." )

		logger.debug( f"{ self.name }.addFilters() starting." )
		self.addFilters()
		logger.debug( f"{ self.name }.addFilters() finished." )

		# Default signal binding if none were set ahead of time.
		if polycephaly.functions.threading.isMainThreadInAPythonProcess() and not self.signalsUsed():

			self.backupSignals()

			tempSignals	=	[
								'SIGHUP',	# Usually, a reload request.
								'SIGINT',	# ^C
								'SIGQUIT',	# ^\
								'SIGCONT',	# Usually, a resumed process.
								'SIGTERM',	# `kill procID` or `pkill myApp.py` and systemd's default kill signal.
								'SIGTSTP',	# ^Z
							]

			logger.debug( f"Setting signals ({ ', '.join( tempSignals ) }) to route to sigTrap()" )
			self.signals( self.sigTrap, *tempSignals )
			del tempSignals

			pass # END IF

		logger.debug( f"{ self.name }.life() starting." )

		self._currFrame		=	0
		self.runLevel( 'RUN' )

		while self.isActive():

			try:

				self.life()

				# Application forgot to run mailman() which the shutdown process relies upon.
				if not self._ranMailman:
					logger.info( f"{ self.name }.mailman() wasn't run in { self.name }.life() - now running it." )
					self.mailman()
					pass # END IF

				# Reset for next run.
				self._ranMailman	=	False

				pass # END TRY

			except Exception as e:
				logger.error( f"{ self.name }.life() experienced an error:\n{ traceback.format_exc() }" )
				pass # END EXCEPTION

			self.freqSleep()

			self._currFrame	+=	1

			if self._currFrame > self.frequency():
				self._currFrame		=	1
				pass # END IF

			pass # END WHILE ACTIVE LOOP

		logger.debug( f"{ self.name }.life() finished." )

		logger.debug( f"{ self.name }.death() starting." )

		self.runLevel( 'HALT' )
		self.joinChildThreads()
		self.death()
		self.runLevel( 'UNSET' )

		logger.debug( f"{ self.name }.death() finished." )

		logger.info( f"{ self.name }.main() stopped." )

		pass # END METHOD : Main

	pass # END CLASS : EXTEND

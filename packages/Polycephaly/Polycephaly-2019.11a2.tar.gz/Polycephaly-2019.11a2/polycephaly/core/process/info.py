#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# Reflection / Debugging
import inspect

# Polycephaly
import polycephaly.functions.utilities
import polycephaly.functions.threading

# Logging
from logbook import Logger
from polycephaly.log import logger_group
logger = Logger( __loader__.name )
logger_group.add_logger( logger )

class Extend( object ):

	def runLevel( self, i=None ):
		'''

		Used for querying or setting the process' run level stored at :any:`Process._runLevel <polycephaly.core.process.Process._runLevel>` and within the range defined by :any:`Process.runLevels() <Extend.runLevels>`.

		As a process runs from :any:`Process.birth() <polycephaly.core.process.events.Extend.birth>` → :any:`Process.life() <polycephaly.core.process.events.Extend.life>` → :any:`Process.death() <polycephaly.core.process.events.Extend.death>`, the run level is updated via this method in :any:`Process.main() <polycephaly.core.process.setup.Extend.main>`.

		Parameters
		----------
		i : :obj:`int` or :obj:`str`
			Integer value within the defined range (e.g. setting to `1` for indicating `BUILDUP` level), or a String equivalent (e.g. setting to `BUILDUP`).

		Returns
		-------
		int
			Run level stored at :any:`Process._runLevel <polycephaly.core.process.Process._runLevel>`

		Raises
		------
		ValueError
			Occurs when ``i`` is set out of range.

		'''

		curframe = inspect.currentframe()
		calframe = inspect.getouterframes( curframe, 2 )

		if i:

			# Run-level given as a string instead of an integer.
			if isinstance( i, str ):
				i	=	self.runLevels( i )
				pass # END IF

			# Sanity check for integer
			runLevelsRange	=	sorted( self.runLevels( 'LIST' ).keys() )
			if not ( runLevelsRange[ 0 ] <= i <= runLevelsRange[ -1 ] ):
				raise ValueError( f"{ i } is not within range of { runLevelsRange[ 0 ] } to { runLevelsRange[ -1 ] }." )
				pass # END IF

			i	=	( None if i == -1 else i )
			logger.debug( f"'{ self.name }' : changing run level from { self._runLevel } ({ self.runLevels( self._runLevel ) }) to { i } ({ self.runLevels( i ) })." )
			self._runLevel	=	i
			pass # END IF

		else:
			logger.debug( f"'{ self.name }' current run level : { self._runLevel } ({ self.runLevels( self._runLevel ) }), queried by { calframe[ 1 ][ 3 ] }()." )
			pass # END ELSE

		return self._runLevel

		pass # END METHOD : Run Level

	def runLevels( self, i=None ):
		'''

		Used for looking up a run level by its integer or string value, or listing all available run levels.

		Parameters
		----------
		i : :obj:`int` or :obj:`str`
			Set to the run level to look up, or `list` to obtain all values.

		Returns
		-------
		str, int, dict
			* String if ``i`` is set to an integer.
			* Integer if ``i`` is set to a string.
			* Dictionary if ``i`` is set to `list` (:obj:`str`).

		'''

		runLevels		=	{
								-1	:	'UNSET',
								0	:	'HALT',
								1	:	'BUILDUP',
								2	:	'RUN',
								3	:	None,
								4	:	None,
								5	:	None,
								6	:	'REBOOT',
								7	:	'CLEANUP',
							}

		# Convert string to integer value
		if isinstance( i, str ):

			# Convert to uppercase for matching.
			i			=	i.upper()

			if i == 'LIST':
				return runLevels
				pass # END IF

			# Reverse the dictionary
			runLevels	=	polycephaly.functions.utilities.invertedDict( runLevels )

			pass # END IF

		return runLevels.get( i, None )

		pass # END METHOD : Run Levels

	def isActive( self, i=None ):
		'''

		Used for querying or setting the process' :any:`active flag <polycephaly.core.process.Process._active>`.  This method is typically used to control the run of process and child-thread loops, including for the loop of :any:`Process.life() <polycephaly.core.process.events.Extend.life>` in :any:`Process.main() <polycephaly.core.process.setup.Extend.main>`.

		Parameters
		----------
		i : :obj:`bool`
			Sets the desired state of the process (and optional child threads).

		Returns
		-------
		bool
			The current value of :any:`Process._active <polycephaly.core.process.Process._active>`.

		'''

		# Bitwise operation that determines if i is a boolean.
		if ( i == False ) ^ ( i == True ):
			logger.debug( f"'{ self.name }' : set active state to { i }." )
			self._active	=	i
			pass # END IF

		# Return active status
		return self._active

		pass # END METHOD

	def getParameter( self, name ):
		'''

		Used for returning private members of the process, and most commonly used by :any:`Application <polycephaly.core.application.Application>` to query a process' :any:`run-time variables <polycephaly.core.process.Process._runtime>`.

		Parameters
		----------
		name : :obj:`str`
			Which private member of the process to return, and the most common use is `runtime`.

		Returns
		-------
		return
			Value of the private member that's being looked up.

		'''

		return getattr( self, '_{}'.format( name ) )

		pass # END METHOD

	def getApp( self ):
		'''

		Returns the :any:`Application <polycephaly.core.application.Application>` instance to a process that's running in threaded mode.

		Returns
		-------
		Application, None
			If called by a process that's running in threaded mode, the Application instance will be returned.  Otherwise, `None` will be returned.

		'''

		return self._application if ( not polycephaly.functions.threading.isProcessForked() ) else None
		pass # END METHOD : Get Application

	def _procInfoSkel( self ):
		'''

		This is the basis for aliased methods to query the Main process for information about other processes, and is most commonly used by:

		* :any:`Process.activeSubProcesses() <polycephaly.core.process.info.Extend.activeSubProcesses>`
		* :any:`Process.listProcessInstances() <polycephaly.core.process.info.Extend.listProcessInstances>`
		* :any:`Process.listRecipients() <polycephaly.core.process.info.Extend.listRecipients>`

		Returns
		-------
		return, None
			If process information is found, will return the request, otherwise will return `None`.

		'''

		curframe = inspect.currentframe()
		calframe = inspect.getouterframes( curframe, 2 )

		# Main process
		if polycephaly.functions.threading.isApplicationMainThread():
			return getattr( self.getApp(), calframe[ 1 ][ 3 ] )()
			pass # END IF

		# Sub-process
		else:

			message		=	self.send(
								recipient	=	self.nameMain,
								subject		=	'procInfo',
								body		=	calframe[ 1 ][ 3 ],
							)

			reply		=	self.waitForReply( message, timeout=15 )

			return reply.get( 'body' )

			pass # END ELSE

		pass # END METHOD : Process Info Skeleton

	def activeSubProcesses( self ):
		'''

		Alias method to show which sub-processes are still active.

		Returns
		-------
		list
			Sub-processes that are still active.

		'''

		return self._procInfoSkel()
		pass # END METHOD : Active Processes

	def listProcessInstances( self ):
		'''

		Alias method to show process instances.

		Returns
		-------
		list
			Process instances.

		'''

		return self._procInfoSkel()
		pass # END METHOD : List processes

	def listRecipients( self ):
		'''

		Alias method to show process message queues.

		Returns
		-------
		list
			Process message queues.

		'''

		return self._procInfoSkel()
		pass # END METHOD : List recipients

	pass # END CLASS : EXTEND

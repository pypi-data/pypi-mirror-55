#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# System
import signal

# Polycephaly
import polycephaly.functions.threading
import polycephaly.functions.utilities

# Logging
from logbook import Logger
from polycephaly.log import logger_group
logger = Logger( __loader__.name )
logger_group.add_logger( logger )

class Extend( object ):

	def signalsDict( self, k=None ):
		'''

		Used for looking up a signal by its integer or string value, or a dictionary listing of all available signals.

		Parameters
		----------
		k : :obj:`int` or :obj:`str`, optional

		Returns
		-------
		:obj:`int`, :obj:`str`, or :obj:`dict`
			Returns a dictionary by default, or the desired signal lookup (`string` if an `integer` is given, or `integer` if a `string` is given).

		'''

		d	=	{ str( v ):int( k ) for v,k in signal.__dict__.items() if v.startswith( 'SIG' ) and not v.startswith( 'SIG_' ) }

		if isinstance( k, str ) and k.upper() in d.keys():
			return d[ k ]
			pass # END

		elif isinstance( k, int ) and k in d.values():
			return polycephaly.functions.utilities.invertedDict( d )[ k ]
			pass # END

		elif k is None:
			return d
			pass # END

		else:
			return None
			pass # END

		pass # END METHOD : Signals Dictionary

	def backupSignals( self ):
		'''

		Used for backing up signals and their reciprocal handlers as a :obj:`dict` to :any:`Process._signalsBak <polycephaly.core.process.Process._signalsBak>`, where key is the signal name in all capital letters, and value is the handler.

		.. seealso::

			* :any:`Process.restoreSignals() <polycephaly.core.process.signals.Extend.restoreSignals>`

		'''

		logger.debug( f'{ self.name } : backing up signals.' )

		self._signalsBak	=	{}

		# e.g. SIGINT, 2
		for sigName, sigNumber in self.signalsDict().items():

			logger.debug( f"Backing up '{ sigName }'." )
			currSignal					=	getattr( signal, sigName )		# Retrieve Signal type (e.g. Signals.SIGINT)
			self._signalsBak[ sigName ]	=	signal.getsignal( currSignal )	# Save handler (e.g. <built-in function default_int_handler>)

			pass # END FOR

		pass # END METHOD : Backup Signals

	def currSignals( self, *args ):
		'''

		Used for pulling one or more of the process' current signal handlers.

		Parameters
		----------
		*args : :obj:`str`
			Signal(s) to retrieve information for.

		Returns
		-------
		handler or dictionary
			If a single argument is given, only a single handler is returned.  For multiple arguments given, a dictionary will be returned with the names given and its reciprocal handler.

		'''

		r	=	{}

		for sigName in args:

			currSignal		=	getattr( signal, sigName )		# Retrieve Signal type based on a string (e.g. 'SIGINT' for Signals.SIGINT)
			r[ sigName ]	=	signal.getsignal( currSignal )	# Handler (e.g. <built-in function default_int_handler>)

			pass # END FOR

		return next( iter( r.values() ) ) if ( len( r ) == 1 ) else r

		pass # END METHOD

	def restoreSignals( self ):
		'''

		Used for restoring signals and their reciprocal handlers as a :obj:`dict` from :any:`Process._signalsBak <polycephaly.core.process.Process._signalsBak>`.

		Returns
		-------
		:obj:`bool`
			`True` if successful, `False` if there are no signals to restore.


		.. seealso::

			* :any:`Process.backupSignals() <polycephaly.core.process.signals.Extend.backupSignals>`

		'''

		logger.debug( f'{ self.name } : restoring signals.' )

		if not self._signalsBak:
			logger.error( "There are no signals to restore." )
			return False
			pass # END IF

		for sigName, sigHandler in self._signalsBak.items():

			logger.debug( f"Restoring '{ sigName }'." )
			currSignal	=	getattr( signal, sigName )

			if sigHandler:
				signal.signal( currSignal, sigHandler )
				pass # END IF

			pass # END FOR

		return True

		pass # END METHOD : Restore Signals

	def signalsUsed( self, i=None ):
		'''

		Used for querying or setting the process' :any:`signals used flag <polycephaly.core.process.Process._signalsUsed>`.

		Parameters
		----------
		i : :obj:`bool`, optional
			Value to set the flag to.

		Returns
		-------
		:obj:`bool`
			The value of the flag.


		.. note::

			When :any:`Process.signals() <polycephaly.core.process.signals.Extend.signals>` is called, it uses this method to set the flag to `True`.

		'''

		if i:
			self._signalsUsed	=	i
			pass # END IF

		return self._signalsUsed

		pass # END METHOD

	def signals( self, cb, *keys ):
		'''

        Bind a callback to an arbitrary number of signals.

        Parameters
        ----------
        cb : :obj:`Function` or :obj:`Method`
            Callback that's executed when a signal occurs that it's been bound to.

        *keys : :obj:`str`
            Variable length list of signals to bind callback to.

        Returns
        -------
        bool
            `True` if successful, `False` if an error occurs.


        An example for registering a callback to multiple signals:

        .. code-block:: python

            def myCallback( self, sigNum, currFrame ):

                print( f'My callback received sigNum={ sigNum } and currFrame={ currFrame }' )

                pass # END METHOD : My callback

            def birth( self ):

                self.signals(
                    self.myCallback,
                    'SIGINT',   # ^C
                    'SIGTERM',  # `kill procID` or `pkill myApp.py` and systemd's default kill signal.
                )

                pass # END METHOD : Birth

        .. seealso::

            * :any:`Process.sigTrap() <polycephaly.core.process.signals.Extend.sigTrap>`

		'''

		if not polycephaly.functions.threading.isMainThreadInAPythonProcess():
			logger.warning( f"{ self.name } ( Mode={ self.getParameter( 'runtime' ).mode } ) : ignoring signals request since these actions can only be performed on the main thread of each Python process." )
			return False
			pass # END PASS

		self.signalsUsed( True )

		r					=	None

		try:

			for currKey in keys:

				currKey	=	currKey.upper()

				if (
					currKey.startswith( 'SIG' )
					and
					not currKey.startswith( 'SIG_' )
					and
					hasattr( signal, currKey )
				):

					sigNum	=	getattr( signal, currKey )
					signal.signal( sigNum, cb )

					logger.debug( f"Process '{self.name}' : bind '{ currKey }' to { cb.__name__ }()." )
					r	=	True

					pass # END IF

				pass # END FOR

			pass # END TRY

		except Exception as e:

			logger.critical( f"{self.name} : {e}" )
			r	=	False

			pass # END EXCEPTION

		finally:

			return r

			pass # END FINALLY

		pass # END METHOD : Signals

	def sigTrap( self, sigNum, currFrame ):
		'''

		This serves as the process’ signal trap for several default signals (e.g. `SIGINT` and `SIGTERM`) set in :any:`Process.main() <polycephaly.core.process.setup.Extend.main>` if you didn't set any in :any:`Process.birth() <polycephaly.core.process.events.Extend.birth>`.

		While you can override this method, you probably won't ever need to, and can leave this to call upon :any:`Process.die() <polycephaly.core.process.actions.Extend.die>`, where your process' specific shutdown actions are carried out in :any:`Process.death() <polycephaly.core.process.events.Extend.death>`.

		Parameters
		----------
		sigNum : :obj:`int`
			Signal number (e.g. `2` for `SIGINT`, or `15` for `SIGTERM`.)

		currFrame : :obj:`frame`
			Python Stack frame.


		.. seealso::

			* :any:`Process.signalsDict() <polycephaly.core.process.signals.Extend.signalsDict>` - useful for converting :obj:`sigNum` to a string representation.

		'''

		self.die(
			sigNum		=	sigNum,
			currFrame	=	currFrame,
		)

		pass # END METHOD : Signal Trap

	pass # END CLASS : EXTEND

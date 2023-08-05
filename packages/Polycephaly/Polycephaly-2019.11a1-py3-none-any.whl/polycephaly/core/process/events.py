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

	def registerCallbacks( self, **kwargs ):
		'''

        Used in :any:`Process.birth() <polycephaly.core.process.events.Extend.birth>` to register events and their reciprocal callbacks.  A callback for a specific event is then called by :any:`Process.callbackEvent() <polycephaly.core.process.events.Extend.callbackEvent>`.

        Parameters
        ----------
        **kwargs
            An arbitrary number of events and their reciprocal callbacks can be passed to this method as keyword arguments.


        An example for registering callbacks related to a USB hardware device:


        .. code-block:: python

            # Polycephaly
            import polycephaly

            class Process( polycephaly.core.Process ):

                def connected( self ):
                    print( 'USB device connected.' )
                    pass # END METHOD : Connected

                def disconnected( self ):
                    print( 'USB device disconnected.' )
                    pass # END METHOD : Disconnected

                def boardPong( self, time, **kwargs ):
                    print( f"USB device responded to program ping with pong at { time }, abc is { kwargs[ 'abc' ] }, and xyz is { kwargs[ 'xyz' ] }." )
                    pass # END METHOD : Board pong

                def commsError( self ):
                    print( 'USB device reports a communications error.' )
                    pass # END METHOD : Communications Error

                def deviceError( self ):
                    print( 'USB device is experiencing an error.' )
                    pass # END METHOD : Device Error

                def birth( self ):

                    self.registerCallbacks(
                        connected       =   self.connected,
                        disconnected    =   self.disconnected,
                        boardPong       =   self.boardPong,
                        commsError      =   self.commsError,
                        deviceError     =   self.deviceError,
                    )

                    pass # END METHOD : Birth

                pass # END PROCESS

		'''

		for k, v in kwargs.items():
			logger.debug( f"Registered callback : '{ k }' : { v }" )
			self._callbacks.update({ k : v })
			pass # END FOR

		pass # END METHOD : registerCallbacks

	def callbackEvent( self, event, *args, **kwargs ):
		'''

        Attempts to run a callback that was registered to an event with :any:`Process.registerCallbacks() <polycephaly.core.process.events.Extend.registerCallbacks>` when a specific event is triggered.

        Parameters
        ----------

        event : :obj:`str`
            Usually called by a process' child thread at a specific event, such as (dis)connect or communication/device failure.

        *args
            Passed directly to the callback as arguments.

        **kwargs
            Passed directly to the callback as keyword arguments.

        Returns
        -------
        return
            Results directly from the callback.


        An example for triggering an event's callback:


        .. code-block:: python

            # System
            import time

            # Hardware
            import myUSBdevice

            # Polycephaly
            import polycephaly

            class Process( polycephaly.core.Process ):

                def _threadBoardPing( self ):

                    while self.isActive():

                        # Board successfully responded
                        if myUSBdevice.ping():

                            self.callbackEvent( 'boardPong', time.time(), abc=123, xyz=789 )

                            pass # END IF

                        # Device failed to respond
                        else:

                            self.callbackEvent( 'deviceError' )

                            pass # END ELSE

                        self.freqSleep()

                        pass # END WHILE LOOP

                    pass # END THREAD : Ping USB board

                def birth( self ):

                    self.launchThreads()

                    pass # END METHOD : Birth

                pass # END PROCESS

        Which would yield:

        .. code-block:: none

            USB device responded to program ping with pong at 123456.789, abc is 123, and xyz is 789.

		'''

		currCB	=	self._callbacks.get( event )

		try:

			if not currCB:
				logger.warning( f"A callback has not been registered for '{ event }' event." )
				pass # END IF

			elif callable( currCB ):
				logger.debug( f"Callback event { event }( args={ args }, kwargs={ kwargs } ) called." )
				return currCB( *args, **kwargs )
				pass # END ELIF

			else:
				logger.warning( f"Callback event { event }( args={ args }, kwargs={ kwargs } ) couldn't be called." )
				pass # END ELSE

			pass # END TRY

		except Exception as e:
			logger.critical( f"Callback event { event }( args={ args }, kwargs={ kwargs } ) experienced a critical error: '{ e }'" )
			pass # END EXCEPTION

		pass # END METHOD : callbackEvent

	def birth( self ):
		'''

		This serves as your process' constructor, and what you would override when you need to prepare your process for starting up.

		'''

		logger.debug( f'{ self.name }.{ inspect.stack()[ 0 ][ 3 ] }() - called by { inspect.stack()[ 1 ][ 3 ] }() : started.' )
		logger.debug( f'{ self.name }.{ inspect.stack()[ 0 ][ 3 ] }() : finished.' )

		pass # END METHOD : Birth

	def life( self ):
		'''

		This serves as your process' loop, and what you would override when you need to setup your process for running n times per second, as defined by the frequency.

		'''

		logger.debug( f'{ self.name }.{ inspect.stack()[ 0 ][ 3 ] }() - called by { inspect.stack()[ 1 ][ 3 ] }() : started.' )

		# Check for new messages, and run appropriate callbacks.
		self.mailman()

		logger.debug( f'{ self.name }.{ inspect.stack()[ 0 ][ 3 ] }() : finished.' )

		pass # END METHOD : Life

	def death( self ):
		'''

		This serves as your process' destructor, and what you would override when you need to prepare your process for shutting down.

		'''


		logger.debug( f'{ self.name }.{ inspect.stack()[ 0 ][ 3 ] }() - called by { inspect.stack()[ 1 ][ 3 ] }() : started.' )
		logger.debug( f'{ self.name }.{ inspect.stack()[ 0 ][ 3 ] }() : finished.' )

		pass # END METHOD : Death

	pass # END CLASS : EXTEND

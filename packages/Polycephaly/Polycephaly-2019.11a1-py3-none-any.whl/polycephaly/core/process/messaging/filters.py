#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# Logging
from logbook import Logger
from polycephaly.log import logger_group
logger = Logger( __loader__.name )
logger_group.add_logger( logger )

class Extend( object ):

	def addFilter( self, route=None, **kwargs ):
		'''

		Adds a message filter and callback to the current process.

		This method wraps :any:`Messenger.addFilter() <polycephaly.comms.messenger.filters.Extend.addFilter>`.

		Parameters
		----------
		route : :obj:`str`, optional
			Message route to use, defaults to process' name for internal messaging between processes.

		**kwargs
			Arbitrary keyword arguments that add on to the filter list.

			Please note, there are reserved keywords that are used by this method:

				* **callback** (:obj:`method` or :obj:`function`) – callable that a message (:obj:`dict`) will be sent to.

				* **id** (:obj:`str`, optional, default: `UUID`) – unique identifier for a filter.

				* **description** (:obj:`str`, optional) – human-friendly description that helps explain in log files the filter that matched.

				* **sender** (:obj:`str`, optional) - filter for a particular process that sent this message.

				* **recipient** (:obj:`str`, optional) - filter for a particular process that will receive this message (useful for making general filters that can be used by multiple processes).

				* **subject** (:obj:`str`, optional) - filter for a specific subject line.

				* **body** (:obj:`str`, optional) - filter for a specific message body.

				* **time** (:obj:`float`, optional) - filter for a specific time that the message was sent.

				* **failed** (:obj:`bool`, optional) - filter for catching critical errors that raised an exception.


		.. note::
			If the only parameter that you use is ``callback``, this will create a "fall through" filter such as demonstrated in the :any:`Fall or Fail <../examples/fallOrFail/launch>` example.

		Returns
		-------
		dict
			Filter parameters used.

		'''

		return self._messenger.addFilter(
			caller=self.name,
			route=( route if route else self.name ),
			**kwargs
		)

		pass # END METHOD : Add Filter

	def listFilters( self, name=None, topic=None ):
		'''

		List filters that are currently registered.

		Parameters
		----------
		name : :obj:`str`, optional
			Process name.

		topic : :obj:`str`, optional
			Topic name.

		Returns
		-------
		dict
			Dictionary of filters that can be whittled down by topic.

		'''

		return self._messenger.listFilters(
			caller	=	name if name else self.name,
			topic	=	topic,
		)

		pass # END METHOD

	pass # END CLASS : Extend

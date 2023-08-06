#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# Reflection
import inspect
import functools

# Types
import types

def add_dynamo( *args, **kwargs ):
	'''

	Function that's capable of generating both functions and class methods from a skeleton function or method.

	Parameters
	----------
	*args
		Passed directly to the function or method.

	**kwargs
		Passed directly to the function or method.  Reserved keywords that are used by this argument are:

		* **skel** (:obj:`method` or :obj:`function`) - Skeleton to build from.

		* **prefix** (:obj:`str`) - Prefix for new method or function that's being created.

		* **number** (:obj:`int`, optional) - Suffix for new method or function that's being created.

		* **cls** (:obj:`class`, optional) - If creating a method, you will need to supply the class as well.

		* **docString** (:obj:`str`, optional) - Documentation for the method or function that's being created.

	Returns
	-------
	function
		When creating a function, will return the newly cloned :obj:`function`, otherwise will return :obj:`None`.


	.. seealso::

		:any:`Examples <../examples/index>` making use of this function:

			* :any:`Locking <../examples/locking/launch>`

			* :any:`Thread Spinner <../examples/threadSpinner/launch>`


	.. note::

		Based upon:

		* `Stack Overflow: Dynamic/runtime method creation (code generation) in Python <https://stackoverflow.com/questions/533382/dynamic-runtime-method-creation-code-generation-in-python>`_

			* `Theran's answer for functions <https://stackoverflow.com/a/533583>`_.

			* `John Montgomery's for methods <https://stackoverflow.com/a/534597>`_.

	'''

	skel		=	kwargs.pop( 'skel' )
	prefix		=	kwargs.pop( 'prefix' )
	number		=	kwargs.pop( 'number', None )
	cls			=	kwargs.pop( 'cls', None )
	docString	=	kwargs.pop( 'docs', None )

	def innerdynamo( self=None ):
		return skel( prefix, number, *args, **kwargs )
		pass # END FUNCTION

	innerdynamo.__name__	=	f"{ prefix }{ number }"
	innerdynamo.__doc__		=	docString if docString else f"docstring for { innerdynamo.__name__ }"

	# Method
	if cls:
		setattr(
			cls,
			innerdynamo.__name__,
			innerdynamo
		)
		pass # END IF

	# Function
	else:
		return innerdynamo
		pass # END ELSE

	pass # END FUNCTION : Add Dynamo

def methodDecorator( *decoArgs, **decoKwargs ):
	'''

    General-purpose decorator which adds a ``decorators`` attribute, which is a list of information (arguments, keyword arguments, and inspected method's information available as ``myClass.myMethod.decorators.argSpec``) added to the method that can then be used from within an class (decorators come before a class is instantiated, hence why we add information that class methods can look up).

    .. seealso::
        :any:`Process.addFilters() <polycephaly.core.process.messaging.filters.Extend.addFilters>` relies on methods using this decorator for locating and adding filters to callbacks.

    Parameters
    ----------
    *args
        An arbitrary amount of arguments passed to the decorator, stored in the method, and accessible from ``myClass.myMethod.decorators.args``:

    **kwargs
        An arbitrary amount of keyword arguments passed to the decorator, stored in the method, and accessible from ``myClass.myMethod.decorators.kwargs``:

    Returns
    -------
    method or return
        If decorated, method is returned.  If the method is called, then if applicable, its return is returned.


    .. note::

        This method is heavily inspired by:

        * `Stack Overflow : Pass self to decorator object <https://stackoverflow.com/a/32614122>`_

        * `Stack Overflow : How to get all methods of a python class with given decorator <https://stackoverflow.com/a/5910893>`_

    An example of decorating a callback that will be run every time a message with the subject line `Testing` (case-insensitive matching) is received:

    .. code-block:: python

        @polycephaly.functions.dynamic.methodDecorator(
            subject     =   r'(?i)^TESTING!$',
        )
        def testing( self, message ):

            logger.notice( f"A test message was received:\\n{ message }" )

            pass # END CALLBACK : Testing


    An example of decorating a callback with a different route, and matching against different headers:

    .. code-block:: python

        @polycephaly.functions.dynamic.methodDecorator(
            'mqtt',                         # Route
            topic       =   '/testing/#',   # /testing topic, and all of its subtopics.
        )
        def testing( self, message ):

            logger.notice( f"A test message was received on the MQTT bus:\\n{ message }" )

            pass # END CALLBACK : Testing

	'''

	def decorator( function ):

		# Create list for 1 or more decorators.
		if not hasattr( function, 'decorators' ):
			setattr( function, 'decorators', [] )
			pass # END IF

		# Append decorator to list.
		getattr( function, 'decorators' ).append(
			types.SimpleNamespace(
				args	=	decoArgs,
				kwargs	=	decoKwargs,
				argSpec	=	inspect.getfullargspec( function ),
			)
		)

		@functools.wraps( function )
		def wrapper( self, *methodArgs, **methodKwargs ):

			return function( self, *methodArgs, **methodKwargs )

			pass # END WRAPPER

		return wrapper

		pass # END DECORATOR

	return decorator

	pass # END FUNCTION : Method Decorator

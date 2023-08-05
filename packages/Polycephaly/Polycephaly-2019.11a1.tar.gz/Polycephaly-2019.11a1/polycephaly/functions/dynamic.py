#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

def add_dynamo( *args, **kwargs ):
	'''

	Function that's capable of generating both functions and class methods from a skeleton function or method.

	Parameters
	----------
	*args
		DESCRIPTION

	**kwargs
		DESCRIPTION

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

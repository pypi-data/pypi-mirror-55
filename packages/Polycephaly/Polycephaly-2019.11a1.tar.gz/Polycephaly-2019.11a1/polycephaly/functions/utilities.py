#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

def invertedDict( d ):
	'''

	Inverts a dictionary's keys and values.

	Parameters
	----------
	d : :obj:`dict`
		Dictionary to flip.

	Returns
	-------
	dict
		Flipped dictionary where values are now keys, and keys are now values.


	.. note::

		Sourced from `Stack Overflow : Reverse / invert a dictionary mapping <https://stackoverflow.com/a/483833>`_.

	'''

	return { v: k for k, v in d.items() }

	pass # END FUNCTION : Inverted dictionary

def getType( v ):
	'''

	Easily obtain a variable's type without delving into its parameters.

	Parameters
	----------
	v : :obj:`variable`
		Variable to inspect.

	Returns
	-------
	str
		Type of variable.

	'''

	return type( v ).__name__

	pass # END FUNCTION: Get type of variable

def easySwitch( match, default=None, **kwargs ):
	'''

    Easier (but limited) implementation of :any:`Switch() <polycephaly.functions.utilities.switch>`.

    Parameters
    ----------
    match : :obj:`value`
        Value to inspect.

    default : :obj:`value`:
        Value to return if no matches are found.

    **kwargs
        Arbitrary amount of values to match against.

    Returns
    -------
    `value` or ``None``
        Value if a match is found from `kwargs`, otherwise default value if one was supplied, or None.


    An example for determining if it's Noon, Midnight, or some other hour:


    .. code-block:: python

        #!/usr/bin/env python -u

        # System
        import time

        # Polycephaly
        import polycephaly.functions.utilities

        print(

            polycephaly.functions.utilities.easySwitch(
                f"H{ time.strftime( '%H' ) }",
                'Some other hour.',
                H0  =   'Midnight',
                H12 =   'Noon',
            )

        )

	'''

	for k, v in kwargs.items():

		if k == match:
			return v
			pass # END IF

		pass # END FOR

	return default

	pass # END FUNCTION : Easy Switch

class switch( object ):
	'''
    An absolute Godsend `Python recipe by Brian Beck <http://code.activestate.com/recipes/410692/>`_ for implementing switching in Python, and all the way back from Mon, 25 Apr 2005!

    Licensed under the `PSF <https://en.wikipedia.org/wiki/Python_Software_Foundation_License>`_.

    .. note::
        Note from the author, Brian Beck:

        This class provides the functionality we want. You only need to look at
        this if you want to know how this works. It only needs to be defined
        once, no need to muck around with its internals.

    All examples are directly from Brian Beck's recipe on `ActiveState Code <https://code.activestate.com/>`_:

    .. code-block:: python

        # The following example is pretty much the exact use-case of a dictionary,
        # but is included for its simplicity. Note that you can include statements
        # in each suite.
        v = 'ten'
        for case in switch(v):
            if case('one'):
                print 1
                break
            if case('two'):
                print 2
                break
            if case('ten'):
                print 10
                break
            if case('eleven'):
                print 11
                break
            if case(): # default, could also just omit condition or 'if True'
                print "something else!"
                # No need to break here, it'll stop anyway

        # break is used here to look as much like the real thing as possible, but
        # elif is generally just as good and more concise.

        # Empty suites are considered syntax errors, so intentional fall-throughs
        # should contain 'pass'
        c = 'z'
        for case in switch(c):
            if case('a'): pass # only necessary if the rest of the suite is empty
            if case('b'): pass
            # ...
            if case('y'): pass
            if case('z'):
                print "c is lowercase!"
                break
            if case('A'): pass
            # ...
            if case('Z'):
                print "c is uppercase!"
                break
            if case(): # default
                print "I dunno what c was!"

        # As suggested by Pierre Quentel, you can even expand upon the
        # functionality of the classic 'case' statement by matching multiple
        # cases in a single shot. This greatly benefits operations such as the
        # uppercase/lowercase example above:
        import string
        c = 'A'
        for case in switch(c):
            if case(*string.lowercase): # note the * for unpacking as arguments
                print "c is lowercase!"
                break
            if case(*string.uppercase):
                print "c is uppercase!"
                break
            if case('!', '?', '.'): # normal argument passing style also applies
                print "c is a sentence terminator!"
                break
            if case(): # default
                print "I dunno what c was!"

        # Since Pierre's suggestion is backward-compatible with the original recipe,
        # I have made the necessary modification to allow for the above usage.
	'''

	def __init__(self, value):
		self.value = value
		self.fall = False

	def __iter__(self):
		"""Return the match method once, then stop"""
		yield self.match
		raise StopIteration
    
	def match(self, *args):
		"""Indicate whether or not to enter a case suite"""
		if self.fall or not args:
			return True
		elif self.value in args: # changed for v1.5, see below
			self.fall = True
			return True
		else:
			return False

	pass # END CLASS: Implement Switch() in Python

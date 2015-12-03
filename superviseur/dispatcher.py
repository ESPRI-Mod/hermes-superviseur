# -*- coding: utf-8 -*-

"""
.. module:: dispatcher.py
   :copyright: Copyright "Sep 25, 2015", Institute Pierre Simon Laplace
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: Dispatches supervision scripts to HPC for execution.

.. moduleauthor:: Lola Falletti <lola.falletti@idris.fr>


"""


class DispatchParameters(object):
    """Data required by the dispatcher.

    """
    def __init__(self):
        """Instance constructor.

        """
        pass


class DispatchException(Exception):
    """Dispatcher exception wrapper.

    """

    def __init__(self, msg):
        """Contructor.

        :param str msg: Exception message.

        """
        self.message = unicode(msg)


    def __str__(self):
        """Returns a string representation.

        """
        return u"PRODIGUER-SUPERVISEUR DISPATCHER EXCEPTION : {}".format(self.message)



def dispatch_script(ctx):
	"""Dispatches supervision script to HPC for execution.

	:param DispatchParameters ctx: Data required to dispatch script to HPC.

	"""
	pass

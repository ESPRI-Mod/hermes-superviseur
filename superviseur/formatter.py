# -*- coding: utf-8 -*-

"""
.. module:: formatter.py
   :copyright: Copyright "Sep 25, 2015", Institute Pierre Simon Laplace
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: Formats scripts in readiness for execution at HPC.

.. moduleauthor:: Lola Falletti <lola.falletti@idris.fr>


"""


class FormatParameters(object):
	"""Data required by the formatter.

	"""
	def __init__(self, simulation, job):
		"""Instance constructor.

		"""
    self.simulation = simulation
    self.job = job


class FormatException(Exception):
    """Formatter exception wrapper.

    """

    def __init__(self, msg):
        """Contructor.

        :param str msg: Exception message.

        """
        self.message = unicode(msg)


    def __str__(self):
        """Returns a string representation.

        """
        return u"PRODIGUER-SUPERVISEUR FORMATTER EXCEPTION : {}".format(self.message)


def format_script(params):
	"""Returns supervision script to be executed at an HPC.

	:param FormatParameters params: Data required by the formatter.

	:returns: A formatted script.
	:rtype: unicode

	"""
	return u"BASH CODE"

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
    def __init__(self, simulation, job, supervision):
        """Instance constructor.

        """
        self.simulation = simulation
        self.job = job
        self.supervision = supervision


def dispatch_script(params):
	"""Dispatches supervision script to HPC for execution.

	:param DispatchParameters params: Data required to dispatch script to HPC.

	"""
	pass

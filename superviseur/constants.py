# -*- coding: utf-8 -*-

"""
.. module:: constants.py
   :copyright: Copyright "Sep 25, 2015", Institute Pierre Simon Laplace
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: Supervision specific constants.

.. moduleauthor:: Lola Falletti <lola.falletti@idris.fr>


"""

# Level 0: skip.
SUPERVISION_LEVEL_0 = 0

# Level 1: email user.
SUPERVISION_LEVEL_1 = 1

# Level 2: automatic execution.
SUPERVISION_LEVEL_2 = 2

# Set of valid supervision levels.
SUPERVISION_LEVEL = {
	SUPERVISION_LEVEL_0,
	SUPERVISION_LEVEL_1,
	SUPERVISION_LEVEL_2
}

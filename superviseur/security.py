# -*- coding: utf-8 -*-

"""
.. module:: security.py
   :copyright: Copyright "Sep 25, 2015", Institute Pierre Simon Laplace
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: Supervision security functions.

.. moduleauthor:: Lola Falletti <lola.falletti@idris.fr>


"""
from superviseur import constants
from prodiguer.utils.security import get_user



def authorize(login):
    """Verifies that the user has authorized supervision.

    """
    # Retrieve user details.
    user = get_user(login)

    # Exit if user not found.
    if not user:
        raise UserWarning("user not found")

    # Exit if user does not want to receive emails.
    if not user.email:
        raise UserWarning("user does not want to receive emails")

    # Exit if user supervision level is insufficient.
    if user.supervisionLevel == constants.SUPERVISION_LEVEL_0:
        raise UserWarning("user supervision level is insufficient")

    return user
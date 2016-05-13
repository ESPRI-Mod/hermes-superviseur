# -*- coding: utf-8 -*-

"""
.. module:: dispatcher.py
   :copyright: Copyright "Sep 25, 2015", Institute Pierre Simon Laplace
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: Dispatches supervision scripts to HPC for execution.

.. moduleauthor:: Lola Falletti <lola.falletti@idris.fr>


"""
from prodiguer.utils import config
from prodiguer.utils import mail
from prodiguer.utils import logger



# Operator email subject template.
_EMAIL_SUBJECT = u"HERMES Supervision :: user login {}, job number {} on {} machine"

# Operator email body template.
_EMAIL_BODY = u"""Dear Hermes platform user {},

Something went wrong with your job number {} on {} machine.

{}

Regards,

The Hermes Supervision Platform"""

_EMAIL_MAP = {}

def _get_script(params):
    """Get the script generated by format_script.py

    """
    return params.supervision.script

def _dispatch_email(params):
    """Dispatches an email to the user for the supervision of his jobs.

    """
    # Initialise email content.
    subject = _EMAIL_SUBJECT.format(
        params.user.login,
        params.job.scheduler_id,
        params.simulation.compute_node_machine_raw)

    body = _EMAIL_BODY.format(
        params.user.login,
        params.job.scheduler_id,
        params.simulation.compute_node_machine_raw, {})

    body.format("Job Late")

    if params.job.is_error:
        body.format("Job fail")
    elif params.job.execution_end_date is None:
        body.format("Job late")

    # Send email.
    #mail.send_email(config.alerts.emailAddressFrom,
                    params.user.email,
                    subject,
                    body)



class DispatchParameters(object):
    """Data required by the dispatcher.

    """
    def __init__(self, simulation, job, supervision, user):
        """Instance constructor.

        """
        self.simulation = simulation
        self.job = job
        self.supervision = supervision
        self.user = user


def dispatch_script(params):
    """Dispatches supervision script to HPC for execution.

    :param DispatchParameters params: Data required to dispatch script to HPC.

    """
    script = _get_script(params)
    if params.user.supervisionLevel == 1:
        _dispatch_email(params)
    return script

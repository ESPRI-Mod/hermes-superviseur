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
from superviseur import constants



# Operator email subject template.
_EMAIL_SUBJECT = u"HERMES-SUPERVISOR :: user {}, job {} on {} machine"

# Operator email body template.
_EMAIL_BODY = u"""Dear Hermes platform user {},

Something went wrong with your job number {} on {} machine.

{}

To fix it, please find in attachment a bash script generated automatically by the Hermes supervision platform. 
You have to copy it in your $HOME and then do :
source {}

Regards,

The Hermes Supervision Platform"""

# Job state specific text.
_JOB_TEXT_LATE = "The Hermes platform has detected that your compute job {} is late for the period {} ({}-{}) for the {} time."
_JOB_TEXT_FAIL = "The Hermes platform has detected that your compute job {} has failed during the period {} ({}-{}) for the {} time."

# Map of job states to text to be sent to user.
_JOB_TEXT = {
    "compute-job-fail": _JOB_TEXT_FAIL,
    "compute-job-late": _JOB_TEXT_LATE
}

# Error raised when job state cannot be supervised.
_ERR_JOB_STATE = "Job cannot be supervised as its status is undetermined."


class JobSpecificText(object):
    """Custom formatter to adapt the text in function of the job status.

    """
    def __init__(self,
        simulation_name,
        job_status,
        period_id,
        periodDateBegin,
        perdiodDateEnd,
        periodNSubmission
        ):
        """Instance constructor.

        """
        self.simulation_name = simulation_name
        self.job_status = job_status
        self.period_id = period_id
        self.periodDateBegin = periodDateBegin
        self.perdiodDateEnd = perdiodDateEnd
        if periodNSubmission=="1":
            self.periodNSubmission = periodNSubmission+"st"
        elif periodNSubmission=="2":
            self.periodNSubmission = periodNSubmission+"nd"
        elif periodNSubmission=="3":
            self.periodNSubmission = periodNSubmission+"rd"
        else:
            self.periodNSubmission = periodNSubmission+"th"


    def __format__(self, format):
        """Instance formatter.

        """
        return _JOB_TEXT[self.job_status].format(
            self.simulation_name,
            self.period_id,
            self.periodDateBegin,
            self.perdiodDateEnd,
            self.periodNSubmission
            )


def _get_email_attachment(params):
    """Returns the email attachment to be sent to the user.

    """
    return params.supervision.script


def _get_email_attachment_name(params):
    """Returns the name of the email attachment to be sent to the user.

    """
    return "supervision-{}-{}-{}-{}.txt".format(
        params.job_status, 
        params.user.login, 
        params.job.scheduler_id, 
        params.simulation.compute_node_machine_raw)


def _get_email_subject(params):
    """Returns subject of email to be sent to user.

    """
    return _EMAIL_SUBJECT.format(
        params.user.login,
        params.job.scheduler_id,
        params.simulation.compute_node_machine_raw)


def _get_email_body(params):
    """Returns body of email to be sent to user.

    """
    return _EMAIL_BODY.format(
        params.user.login,
        params.job.scheduler_id,
        params.simulation.compute_node_machine_raw,
        JobSpecificText(
            params.simulation.name,
            params.job_status,
            params.job_period.period_id,
            params.job_period.period_date_begin,
            params.job_period.period_date_end,
            str(params.job_period_counter[1])
            ),
        _get_email_attachment_name(params)
        )


def _dispatch_email(params):
    """Dispatches an email to the user for the supervision of his jobs.

    """
    mail.send_email(
        config.alerts.emailAddressFrom,
        params.user.email,
        _get_email_subject(params),
        _get_email_body(params),
        _get_email_attachment(params),
        _get_email_attachment_name(params)
        )


class DispatchParameters(object):
    """Data required by the dispatcher.

    """
    def __init__(
        self, 
        simulation, 
        job,
        job_period, 
        job_period_counter,
        supervision, 
        user):
        """Instance constructor.

        """
        self.simulation = simulation
        self.job = job
        self.job_period = job_period
        self.job_period_counter = job_period_counter
        self.supervision = supervision
        self.user = user
        if job.is_error:
            self.job_status = u'compute-job-fail'
        elif job.execution_end_date is None:
            self.job_status = u'compute-job-late'
        else:
            raise ValueError(_ERR_JOB_STATE)


def dispatch_script(params):
    """Dispatches supervision script to HPC for execution.

    :param DispatchParameters params: Data required to dispatch script to HPC.

    """
    if params.user.supervisionLevel == constants.SUPERVISION_LEVEL_1:
        _dispatch_email(params)

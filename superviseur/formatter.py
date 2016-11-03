# -*- coding: utf-8 -*-

"""
.. module:: formatter.py
   :copyright: Copyright "Sep 25, 2015", Institute Pierre Simon Laplace
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: Formats scripts in readiness for execution at HPC.

.. moduleauthor:: Lola Falletti <lola.falletti@idris.fr>


"""
import datetime
import glob
import os

from prodiguer.cv.constants import JOB_TYPE_COMPUTING


# 
_HPC_JOB_STATUS_COMMAND = {
    "IDRIS": "llq -j $HPC_JOB_ID -f %st | sed -n 3p",
    "TGCC": "ccc_mpp | grep $HPC_JOB_ID"
}

# Templates folder.
_TEMPLATE_FOLDER = os.path.join(os.path.dirname(__file__), 'templates')

# Set of loaded templates.
_templates = dict()


def _load_templates():
    """Loads script templates from file system.

    """

    for fpath in glob.glob(os.path.join(_TEMPLATE_FOLDER, '*.txt')):
        filename = os.path.basename(fpath)
        with open(fpath) as f:
            _templates[filename] = f.read()


def _hpc_submission(params):
    """Get the HPC machine name and return the corresponding submission job command.

    """
    if params.simulation.compute_node_raw == u"IDRIS":
        return "llsubmit"
    if params.simulation.compute_node_raw == u"TGCC": #or "CCRT" ?
        return "ccc_msub"


def _hpc_cancel_job(params):
    """Get the HPC machine name and return the corresponding submission job command.

    """
    if params.simulation.compute_node_raw == u"IDRIS":
        return "llcancel"
    if params.simulation.compute_node_raw == u"TGCC": #or "CCRT" ?
        return "ccc_mdel"


def _get_template(params):
    """Get the template file and replace the generic fields.

    """
    if not _templates:
        _load_templates()

    if params.job.is_error:
        template = _templates['fail.txt']
        if params.job.typeof == JOB_TYPE_COMPUTING:
            template += _templates['computing.txt']
    elif params.job.execution_end_date is None:
        template = _templates['late.txt']
        if params.job.typeof == JOB_TYPE_COMPUTING:
            template += _templates['computing.txt']
    else:
        raise ValueError("Template not found")

    return template


class FormatParameters(object):
    """Input data required by the formatter.

    """
    def __init__(
        self,
        simulation,
        job,
        job_period,
        supervision,
        user
        ):
        """Instance constructor.

        """
        self.simulation = simulation
        self.job = job
        self.job_period = job_period
        self.now = datetime.datetime.utcnow()
        self.supervision = supervision
        self.user = user


def format_script(params):
    """Returns supervision script to be executed at an HPC.

    :param FormatParameters params: Data required by the formatter.

    :returns: A formatted script.
    :rtype: unicode

    """
    script = _get_template(params)
    script = script.replace('{timestamp}', unicode(params.now))
    script = script.replace('{year}', unicode(params.now.year))
    script = script.replace('{job_name}', "Job_{}".format(params.simulation.name))
    script = script.replace('{hpc_job_id}', params.job.scheduler_id)
    script = script.replace('{hpc_submission_cmd}', _hpc_submission(params))
    script = script.replace('{submission_path}', params.job.submission_path or u"UNKNOWN")
    if params.job.execution_end_date is None:
        script = script.replace('{compute_node_machine}', params.simulation.compute_node_machine_raw)
        script = script.replace('{hpc_cancel_cmd}', _hpc_cancel_job(params))
        script = script.replace('{job_uid}', params.job.job_uid)
        script = script.replace('{retrieve_job_status}', _HPC_JOB_STATUS_COMMAND[params.simulation.compute_node_raw])
        script = script.replace('{simulation_uid}', params.job.simulation_uid)
        script = script.replace('{user_login}', params.user.login)
        script = script.replace('{user_email}', params.user.email)
    
    return script

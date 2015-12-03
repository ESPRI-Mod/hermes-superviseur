
# Imports.
import argparse
import os
import uuid

import prodiguer
import superviseur
from prodiguer.db import pgres as db
from prodiguer.utils import logger



# Define command line arguments.
_ARGS = argparse.ArgumentParser("Writes a formatted superviseur script to file system.")
_ARGS.add_argument(
    "-j", "--job",
    help="Unique identifier of a job that failed or was late",
    dest="job_uid",
    type=str
    )


# Output directory is derived from script location.
_OUT_DIR = os.path.dirname(__file__)


def _get_data(job_uid):
    """Returns required data from database.

    """
    db.session.start()
    try:
        job = db.dao_monitoring.retrieve_job(job_uid)
        if job is None:
            raise ValueError("Job does not exist in database")
        simulation = db.dao_monitoring.retrieve_simulation(job.simulation_uid)
        return simulation, job
    finally:
        db.session.end()


def _write_script(script, job):
    """Writes script to file system.

    """
    fname = "superviseur-script-{}.sh".format(job.job_uid)
    fpath = os.path.join(_OUT_DIR, fname)
    with open(fpath, 'wb') as output_file:
        output_file.write(script)
    logger.log("Superviseur script written to --> {}".format(fpath))


def _execute_formatter(simulation, job):
    """Executes the superviseur formatter function.

    """
    formatter_params = superviseur.FormatParameters(simulation, job)
    try:
        script = superviseur.format_script(formatter_params)
    except superviseur.DispatchException as err:
        logger.log_error(err)
    else:
        _write_script(script, job)


def _main(args):
    """Main entry point.

    """
    # Validate input arguments.
    try:
        uuid.UUID(args.job_uid)
    except ValueError:
        raise ValueError("Job idnetifier is invalid")

    # Load data from database.
    simulation, job = _get_data(args.job_uid)

    # Dispatch script to HPC for execution.
    _execute_formatter(simulation, job)



# Main entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())

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
    with db.session.create():
        job = db.dao_monitoring.retrieve_job(job_uid)
        if job is None:
            raise ValueError("Job does not exist in database")

        simulation = db.dao_monitoring.retrieve_simulation(job.simulation_uid)
        if simulation is None:
            raise ValueError("Simulation does not exist in database")

        supervision = db.dao_superviseur.retrieve_supervision(2)
        if supervision is None:
            raise ValueError("Supervision does not exist in database")

        user = superviseur.authorize(simulation.compute_node_login)
        if user is None:
            raise ValueError("User does not exist in database")

        return simulation, job, supervision, user

def _execute_dispatcher(simulation, job, supervision, user):
    """Executes the superviseur dispatcher function.

    """
    params = superviseur.DispatchParameters(simulation, job, supervision, user)
    try:
        superviseur.dispatch_script(params)
    except Exception as err:
        logger.log_error(err)
    

if __name__ == '__main__':
    """Main entry point.

    """
    args = _ARGS.parse_args()
    # Validate input arguments.
    try:
        uuid.UUID(args.job_uid)
    except ValueError:
        raise ValueError("Job identifier is invalid")

    simulation, job, supervision, user = _get_data(args.job_uid)
    _execute_dispatcher(simulation, job, supervision, user)
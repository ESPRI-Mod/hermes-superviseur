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


def _get_template(params):
    """Get the template file and replace the generic fields.

    """
    if not _templates:
        _load_templates()

    if params.job.is_error:
        template = _templates['fail.txt']
    elif params.job.execution_end_date is None:
        template = _templates['late.txt']
    else:
        raise ValueError("Template not found")
    
    template = template.replace('{timestamp}', unicode(params.now))
    template = template.replace('{year}', unicode(params.now.year))
    template = template.replace('{submission_path}', params.job.submission_path)

    return template



class FormatParameters(object):
    """Input data required by the formatter.

    """
    def __init__(self, simulation, job):
        """Instance constructor.

        """
        self.simulation = simulation
        self.job = job
        self.now = datetime.datetime.now()
        #self.supervision = supervision


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
    model = params.simulation.model_raw
    space = params.simulation.space_raw
    experiment = params.simulation.experiment_raw
    job_name = params.simulation.name

    pp_name = params.job.post_processing_name
    if params.job.execution_end_date is None :
        print "JOB LATE"
    else :
        print params.job.post_processing_name
    #print "\n *** SIMULATION ***"
    #print params.simulation
    #print "\n *** JOB ***"
    #print params.job
    
    my_template = _get_template(params)
    print my_template
    submit_text = \
  u"#!/bin/bash \n\
\n\
fichier=$WORKDIR'/IGCM_OUT/%s/%s/%s/%s/Out/' \n\
\n\
if [[ -f $fichier && -s $fichier ]]; then\n\
  echo '$fichier exists and is not empty'\n\
  if grep -c ERROR $fichier; then\n\
    echo 'Errors in the file'\n\
  else\n\
    echo 'No error in the file'\n\
  fi\n\
else\n\
  echo '$fichier does not exist or is empty'\n\
fi\n" %(model, space, experiment, job_name)
    #return u"BASH CODE TO GO HERE"
    return my_template

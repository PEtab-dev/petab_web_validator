import logging
import os
import re
import tempfile

from petab.C import *
from petab.lint import lint_problem
import petab
from flask import render_template, flash
from markupsafe import Markup
import libsbml
import pandas as pd

from app import app
from app.forms import PEtabForm


@app.route('/', methods=['GET', 'POST'])
def index():
    form = PEtabForm()
    if form.validate_on_submit():
        with tempfile.TemporaryDirectory(dir=f"{app.root_path}") as tmpdirname:
            fn = tempfile.mktemp(".log", dir=f"{tmpdirname}")
            file_handler = logging.FileHandler(fn, mode='w')
            file_handler.setLevel('DEBUG')
            petab.lint.logger.addHandler(file_handler)

            try:
                petab_problem = get_problem(form.sbml_file.data,
                                            form.condition_file.data,
                                            form.measurement_file.data,
                                            form.parameters_file.data,
                                            form.observables_file.data)
            except Exception as e:
                flash(Markup(f'<p> Not valid: </p> {e} '), category='error')
                return render_template('index.html', form=form)

            try:
                res = lint_problem(petab_problem)
                if res:
                    with open(fn) as f:
                        error_log = f.read()
                        p = re.compile('\n')
                        error_log = p.sub('<br>', error_log)
                    flash(Markup(f'<p> Not valid: </p> <p> {error_log} </p>'), category='error')
                else:
                    flash(Markup(f'<p> Great! Your model is valid. </p>'), category='success')
            except Exception as e:
                flash(Markup(f'<p> Error: </p> {e} '), category='error')

    return render_template('index.html', form=form)


def get_problem(sbml_file, condition_file, measurement_file, parameters_file,
                observables_file):
    """
    will be removed
    :return:
    """

    if sbml_file:
        sbml_reader = libsbml.SBMLReader()
        sbml_str = str(sbml_file.stream.read(), "utf-8")
        sbml_document = sbml_reader.readSBMLFromString(sbml_str)
        sbml_model = sbml_document.getModel()
    else:
        sbml_reader = None
        sbml_document = None
        sbml_model = None

    if condition_file:
        condition_df = pd.read_csv(condition_file, sep='\t')
        try:
            condition_df.set_index([CONDITION_ID], inplace=True)
        except KeyError:
            raise KeyError(
                f'Condition table missing mandatory field {CONDITION_ID}.')
    else:
        condition_df = None

    if measurement_file:
        measurement_df = petab.measurements.get_measurement_df(pd.read_csv(measurement_file, sep='\t'))
    else:
        measurement_df = None

    if parameters_file:
        parameters_df = pd.read_csv(parameters_file, sep='\t')
        try:
            parameters_df.set_index([PARAMETER_ID], inplace=True)
        except KeyError:
            raise KeyError(
                f"Parameter table missing mandatory field {PARAMETER_ID}.")
    else:
        parameters_df = None

    if observables_file:
        observables_df = pd.read_csv(observables_file, sep='\t')
        try:
            observables_df.set_index([OBSERVABLE_ID], inplace=True)
        except KeyError:
            raise KeyError(
                f"Observable table missing mandatory field {OBSERVABLE_ID}.")
    else:
        observables_df = None

    petab_problem = petab.Problem(sbml_reader=sbml_reader,
                                  sbml_document=sbml_document,
                                  sbml_model=sbml_model,
                                  condition_df=condition_df,
                                  measurement_df=measurement_df,
                                  parameter_df=parameters_df,
                                  observable_df=observables_df)
    return petab_problem

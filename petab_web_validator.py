from typing import Optional

import libsbml
import pandas as pd
import petab

from app import app
app.secret_key = 'secret password'


def get_petab_problem(sbml_str: str = None,
                      condition_df: Optional[pd.DataFrame] = None,
                      measurement_df: Optional[pd.DataFrame] = None,
                      parameter_df: Optional[pd.DataFrame] = None,
                      observable_df: Optional[pd.DataFrame] = None
                      ) -> 'petab.Problem':
    """
    load petab problem.

    Arguments:
        sbml_str: PEtab SBML file
        condition_df: PEtab condition table
        measurement_df: PEtab measurement table
        parameter_df: PEtab parameter table
        observable_df: PEtab observables tables
    """

    sbml_model = sbml_document = sbml_reader = None

    if condition_df:
        condition_df = petab.conditions.get_condition_df(condition_df)

    if measurement_df:
        # TODO: If there are multiple tables, we will merge them
        measurement_df = petab.measurements.get_measurement_df(measurement_df)

    if parameter_df:
        parameter_df = petab.parameters.get_parameter_df(parameter_df)

    if sbml_str:
        sbml_reader = libsbml.SBMLReader()
        sbml_document = sbml_reader.readSBMLFromString(sbml_str)
        sbml_model = sbml_document.getModel()

    if observable_df:
        # TODO: If there are multiple tables, we will merge them
        observable_df = petab.observables.get_observable_df(observable_df)

    return petab.Problem(condition_df=condition_df,
                         measurement_df=measurement_df,
                         parameter_df=parameter_df,
                         observable_df=observable_df,
                         sbml_model=sbml_model,
                         sbml_document=sbml_document,
                         sbml_reader=sbml_reader)

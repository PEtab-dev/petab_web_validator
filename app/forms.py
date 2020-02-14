from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import SubmitField


class PEtabForm(FlaskForm):
    sbml_file = FileField(
        ' sbml file',
        validators=[
            FileAllowed(['xml'],
                        'Only files with the *.xml extension are allowed')])
    condition_file = FileField(
        ' condition file',
        validators=[
            FileAllowed(['tsv'],
                        'Only files with the *.tsv extension are allowed')])
    measurement_file = FileField(
        ' measurement file',
        validators=[
            FileAllowed(['tsv'],
                        'Only files with the *.tsv extension are allowed')])
    parameters_file = FileField(
        ' parameters file',
        validators=[
            FileAllowed(['tsv'],
                        'Only files with the *.tsv extension are allowed')])
    observables_file = FileField(
        'observables file',
        validators=[
            FileAllowed(['tsv'],
                        'Only files with the *.tsv extension are allowed')])
    submit = SubmitField('Upload')

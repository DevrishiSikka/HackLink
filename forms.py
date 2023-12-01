from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired, FileField
from wtforms import StringField, SelectField, SubmitField, EmailField, TelField
from wtforms.validators import InputRequired

class ParticipantForm(FlaskForm):
  participant_name = StringField('Participant Name', validators=[InputRequired()], render_kw={'placeholder':'Participant Name'})
  register_number = StringField('Register Number', validators=[InputRequired()], render_kw={'placeholder':'Register Numbber'})
  team_name = StringField('Team Name', validators=[InputRequired()], render_kw={'placeholder':'Team Name'})
  mobile_number = TelField('Mobile Number', validators=[InputRequired()], render_kw={'placeholder':'Mobile Number'})
  accomodation = SelectField('Accomodation', choices=[('hostel', 'Hosteller'), ('dayscholar', 'Dayschollar')], validators=[InputRequired()], render_kw={"id": "accomodation"})
  email_id = EmailField("Email ID", validators=[InputRequired()], render_kw={"placeholder":'email ID'})
  hostel_block = SelectField('Hostel Block', choices=[('A', 'A Block'), ('B', 'B Block'), ('C', 'C Block'), ('D', 'D Block')], validators=[InputRequired()], render_kw={"id": "hostelBlock"})
  gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[InputRequired()], render_kw={"id": "genderSelection"})
  submit_button = SubmitField('Submit')

class UploadForm(FlaskForm):
    file = FileField("File", validators=[
        FileRequired()])


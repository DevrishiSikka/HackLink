from flask import Flask, render_template, request, jsonify
from forms import ParticipantForm
from sqlalchemy import func
import uuid
import requests
import qrcode
import configparser
from werkzeug.utils import secure_filename
import os

# -------------------LOAD-CREDENTIALS--------------------------------------------------------------#

def load_credentials(filename='config.ini'):
    config = configparser.ConfigParser()
    config.read(filename)
    return config['Credentials']

# ------------------------------------------------------------------------------------------------# 

credentials = load_credentials()

app = Flask(__name__)
app.config['SECRET_KEY'] = credentials.get("secret_key",'')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['ALLOWED_EXTENTIONS'] = {'xlsx'}
app.config['UPLOAD_FOLDER'] = '/uploads'


from models import Participant, db

# --------------------------------------- UTIL-FUNCTIONS ------------------------------------------#

# MAILING HELPER
class SendParticipantEmail(Exception):
   def __init__(self, message, status_code):
      super().__init__(message)
      self.status_code = status_code

def mailAfterParticipant(participant_name, participant_team_name, filename, participant_email):
       files = [("attachment", ("qrcode.png", open(f"qrcodes/{filename}.png", "rb").read(), "image/png"))]
       response = requests.post(
        "https://api.mailgun.net/v3/mail.dungeonofdevs.tech/messages",
        auth=("api", f"{credentials.get("api_key",'')}"),
        data={
            "from": "Dungeon Of Developers <devrishisikka@mail.dungeonofdevs.tech>",
            "to": f"{participant_name} <{participant_email}>",
            "template": "dod_after_registration",
            "h:X-Mailgun-Variables": f'{{"participant_name": "{participant_name}", "participant_team_name": "{participant_team_name}"}}'
        },
        files=files

    )
       if response.status_code != 200:
            error_message = f"Mailgun API request failed with status code {response.status_code}"
            raise SendParticipantEmail(error_message, status_code=response.status_code)
       
       return response

# ALLOWED FILE EXTENTION
def allowed_file(filename : str):
  return "." in filename and filename.rsplit('.',1)[1] in app.config['ALLOWED_EXTENTIONS']

# --------------------------------------- MAIN-ROUTES ------------------------------------------------#

@app.route('/')
def main_page():
  male_count = db.session.query(func.count(Participant.id)).filter(Participant.gender == 'male').scalar()
  female_count = db.session.query(func.count(Participant.id)).filter(Participant.gender == 'female').scalar()
  hosteller_Count = db.session.query(func.count(Participant.id)).filter(Participant.accomodation == 'hostel').scalar()
  dayscholar_Count = db.session.query(func.count(Participant.id)).filter(Participant.accomodation == 'dayscholar').scalar()
  checked_in_count = db.session.query(func.count(Participant.id)).filter(Participant.checked_in=='False').scalar()
  total_participants = db.session.query(func.count(Participant.id)).scalar()
  return render_template('index.html', male_count=male_count, female_count=female_count, hosteller_Count=hosteller_Count, dayscholar_Count=dayscholar_Count, checked_in_count=checked_in_count, total_participants=total_participants)


@app.route('/dashboard')
def dashboard():
  data_list = Participant.query.all()
  return render_template('dashboard.html', datalist = data_list)


@app.route('/participants/add', methods=["POST", "GET"])
def addParticipant():
  form = ParticipantForm()
  if request.method == "POST" and form.validate_on_submit():
        participant_name = request.form.get('participant_name')
        register_number = request.form.get('register_number')
        team_name = request.form.get('team_name')
        mobile_number = request.form.get('mobile_number')
        accomodation = request.form.get('accomodation')
        email_id = request.form.get('email_id')
        gender = request.form.get('gender')
        if accomodation == 'dayscholar':
            hostel_block = 'N/A'
        else:
            hostel_block = request.form.get('hostel_block')
        slug_value = str(uuid.uuid4())[:15].replace("-","")

        existing_participant = Participant.query.filter_by(register_number=register_number).first()
        if existing_participant:
           return render_template("add_indivisual_participant.html", form=form, exists=True)
        else:
          new_participant = Participant(
              participant_name=participant_name,
              register_number=register_number,
              team_name=team_name,
              mobile_number=mobile_number,
              accomodation=accomodation,
              email_id=email_id,
              hostel_block=hostel_block,
              gender=gender,
              slug=slug_value
          )
          db.session.add(new_participant)
          db.session.commit()

        try:
            qr = qrcode.QRCode(
                version=1,  
                error_correction=qrcode.constants.ERROR_CORRECT_H, 
                box_size=10,  
                border=4,  
            )
            qr.add_data(slug_value)
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")
            qr_image.save(f"qrcodes/{register_number}.png")

            mailAfterParticipant(participant_name=participant_name, participant_team_name=team_name, filename=register_number,participant_email= email_id)
            new_participant = Participant.query.filter_by(register_number=register_number).first()
            new_participant.onboarding_email_sent = True
            db.session.commit()

        except SendParticipantEmail as e:
            print(e)

  return render_template('add_indivisual_participant.html', form = form, exists=False)


@app.route('/participant/info/<slug>')
def userInfo(slug):
    participant = Participant.query.filter_by(slug=slug).first()
    if participant:
        participant_info = {
            'participant_name': participant.participant_name,
            'register_number': participant.register_number,
            'team_name': participant.team_name,
            'mobile_number': participant.mobile_number,
            'accomodation': participant.accomodation,
            'email_id': participant.email_id,
            'hostel_block': participant.hostel_block,
            'gender': participant.gender,
            'checked_in': participant.checked_in,
            'onboarding_email_sent': participant.onboarding_email_sent,
        }
        return jsonify(participant_info)
    else:
        return jsonify({'error': 'Participant not found'}), 404


@app.route("/participant/upload", methods=['POST','GET'])
def uploadList():
    error = False
    if request.method == "POST":
        if "file" in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                secure_filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename))
            else:
                return render_template('upload_file.html', error=True)
    return render_template('upload_file.html', error=False)

# ----------------------------------------QR-SCANNER-UTILITY---------------------------------------------#
@app.route("/scanqr")
def scanQR():
    return render_template('qrScanner.html')


@app.route("/api/scanQR", methods=['POST'])
def QRScannData():
    try:
        qr_data = request.form.get('qr_data')
        existing_participant = Participant.query.filter_by(slug=qr_data).first()
        if existing_participant:
            existing_participant.checked_in = True
            db.session.commit()
            response_data = {'data':existing_participant.participant_name, 'present': True}
            print((response_data))
            return jsonify(response_data)
        else:
            return jsonify({'data':'Not Found', 'present': False})
    except Exception as e:
        return jsonify({'error': str(e)})

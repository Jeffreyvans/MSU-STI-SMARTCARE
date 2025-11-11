from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from datetime import date
from django.contrib import messages
from django.contrib.auth.models import User, auth

from .models import patient, doctor, diseaseinfo, consultation, rating_review
from chats.models import Chat, Feedback

# ---------------- Machine Learning Model ----------------
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("sti.csv")   # Make sure sti.csv is in the project root or static/data

# Features & target
X = df.drop("stis", axis=1)
y = df["stis"]

# Encode target labels (STIs)
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression(max_iter=2000)
model.fit(X_train, y_train)

# Store lists
stilist = le.classes_.tolist()   # List of all diseases
symptomslist = list(X.columns)
alphabaticsymptomslist = sorted(symptomslist)


# ---------------- Home ----------------
def home(request):
    if request.method == 'GET':
        return render(request, 'homepage/index.html')


# ---------------- Admin Dashboard ----------------
def admin_ui(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            auser = request.user
            Feedbackobj = Feedback.objects.all()
            return render(request, 'admin/admin_ui/admin_ui.html',
                          {"auser": auser, "Feedback": Feedbackobj})
        else:
            return redirect('home')

    if request.method == 'POST':
        return render(request, 'patient/patient_ui/profile.html')


# ---------------- Patient UI ----------------
def patient_ui(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            patientusername = request.session['patientusername']
            puser = User.objects.get(username=patientusername)
            return render(request, 'patient/patient_ui/profile.html', {"puser": puser})
        else:
            return redirect('home')

    if request.method == 'POST':
        return render(request, 'patient/patient_ui/profile.html')


def pviewprofile(request, patientusername):
    if request.method == 'GET':
        puser = User.objects.get(username=patientusername)
        return render(request, 'patient/view_profile/view_profile.html', {"puser": puser})


# ---------------- STI Prediction ----------------
def checkdisease(request):
    if request.method == 'GET':
        return render(request, 'patient/checkdisease/checkdisease.html',
                      {"list2": alphabaticsymptomslist})

    elif request.method == 'POST':
        inputno = int(request.POST["noofsym"])
        if inputno == 0:
            return JsonResponse({'predicted_sti': "none", 'confidencescore': 0})

        psymptoms = request.POST.getlist("symptoms[]")

        # Build input vector
        testingsymptoms = [0] * len(symptomslist)
        for k, sym in enumerate(symptomslist):
            if sym in psymptoms:
                testingsymptoms[k] = 1

        inputtest = [testingsymptoms]

        # Predict
        predicted_encoded = model.predict(inputtest)
        predicted_sti = le.inverse_transform(predicted_encoded)[0]   # Decode back to disease name
        confidencescore = model.predict_proba(inputtest).max() * 100

        # Save to DB
        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)
        patient_obj = puser.patient

        stiinfo_new = diseaseinfo(
            patient=patient_obj,
            diseasename=predicted_sti,
            no_of_symp=inputno,
            symptomsname=psymptoms,
            confidence=format(confidencescore, '.0f'),
            consultdoctor="STD Specialist"
        )
        stiinfo_new.save()

        request.session['diseaseinfo_id'] = stiinfo_new.id
        request.session['doctortype'] = "STD Specialist"

        return JsonResponse({
            'predicted_sti': predicted_sti,
            'confidencescore': format(confidencescore, '.0f'),
            'consultdoctor': "STD Specialist"
        })


# ---------------- Consultation ----------------
def pconsultation_history(request):
    if request.method == 'GET':
        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)
        patient_obj = puser.patient
        consultationnew = consultation.objects.filter(patient=patient_obj)
        return render(request, 'patient/consultation_history/consultation_history.html',
                      {"consultation": consultationnew})


def dconsultation_history(request):
    if request.method == 'GET':
        doctorusername = request.session['doctorusername']
        duser = User.objects.get(username=doctorusername)
        doctor_obj = duser.doctor
        consultationnew = consultation.objects.filter(doctor=doctor_obj)
        return render(request, 'doctor/consultation_history/consultation_history.html',
                      {"consultation": consultationnew})


def doctor_ui(request):
    if request.method == 'GET':
        doctorid = request.session['doctorusername']
        duser = User.objects.get(username=doctorid)
        return render(request, 'doctor/doctor_ui/profile.html', {"duser": duser})


def dviewprofile(request, doctorusername):
    if request.method == 'GET':
        duser = User.objects.get(username=doctorusername)
        r = rating_review.objects.filter(doctor=duser.doctor)
        return render(request, 'doctor/view_profile/view_profile.html',
                      {"duser": duser, "rate": r})


def consult_a_doctor(request):
    if request.method == 'GET':
        doctortype = request.session['doctortype']
        dobj = doctor.objects.all()
        return render(request, 'patient/consult_a_doctor/consult_a_doctor.html', {"dobj": dobj})


def make_consultation(request, doctorusername):
    if request.method == 'POST':
        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)
        patient_obj = puser.patient

        duser = User.objects.get(username=doctorusername)
        doctor_obj = duser.doctor
        request.session['doctorusername'] = doctorusername

        diseaseinfo_id = request.session['diseaseinfo_id']
        diseaseinfo_obj = diseaseinfo.objects.get(id=diseaseinfo_id)

        consultation_date = date.today()
        status = "active"

        consultation_new = consultation(
            patient=patient_obj,
            doctor=doctor_obj,
            diseaseinfo=diseaseinfo_obj,
            consultation_date=consultation_date,
            status=status
        )
        consultation_new.save()
        request.session['consultation_id'] = consultation_new.id
        return redirect('consultationview', consultation_new.id)


def consultationview(request, consultation_id):
    if request.method == 'GET':
        request.session['consultation_id'] = consultation_id
        consultation_obj = consultation.objects.get(id=consultation_id)
        return render(request, 'consultation/consultation.html', {"consultation": consultation_obj})


def rate_review(request, consultation_id):
    if request.method == "POST":
        consultation_obj = consultation.objects.get(id=consultation_id)
        patient = consultation_obj.patient
        doctor1 = consultation_obj.doctor
        rating = request.POST.get('rating')
        review = request.POST.get('review')

        rating_obj = rating_review(patient=patient, doctor=doctor1,
                                   rating=rating, review=review)
        rating_obj.save()

        rate = int(rating_obj.rating)
        doctor.objects.filter(pk=doctor1).update(rating=rate)

        return redirect('consultationview', consultation_id)


def close_consultation(request, consultation_id):
    if request.method == "POST":
        consultation.objects.filter(pk=consultation_id).update(status="closed")
        return redirect('home')


# ---------------- Chat System ----------------
def post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        consultation_id = request.session['consultation_id']
        consultation_obj = consultation.objects.get(id=consultation_id)

        c = Chat(consultation_id=consultation_obj, sender=request.user, message=msg)
        if msg != '':
            c.save()
            return JsonResponse({'msg': msg})
    else:
        return HttpResponse('Request must be POST.')


def chat_messages(request):
    if request.method == "GET":
        consultation_id = request.session['consultation_id']
        c = Chat.objects.filter(consultation_id=consultation_id)
        return render(request, 'consultation/chat_body.html', {'chat': c})

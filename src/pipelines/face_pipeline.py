#  face Image -> face Detect -> shape Predictor -> ResNet -> embedding
#  face Image - . resNet -> svm ->student Info

import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st
from src.database.db import get_all_students

@st.cache_resource
def load_dlib_model():
    detector= dlib.get_frontal_face_detector()
    shape_predictor= dlib.shape_predictor(face_recognition_models.pose_predictor_model_location())
    features= dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    return detector,shape_predictor,features

def get_face_embedding(image_np):
    detector,shape_predictor,features = load_dlib_model()
    if image_np.ndim == 3 and image_np.shape[2] == 4:
        image_np = image_np[:, :, :3]
    image_np = np.asarray(image_np, dtype=np.uint8)
    faces = detector(image_np,1)
    encodings = []
    for face in faces:
        shape = shape_predictor(image_np, face)
        feature_descriptor = features.compute_face_descriptor(image_np, shape, 1)
        encodings.append(np.asarray(feature_descriptor, dtype=np.float32))
    return encodings

@st.cache_resource
def get_trained_model():
    x = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:
        embeddings = student.get("face_embedding")
        if embeddings:
            x.append(np.array(embeddings))
            y.append(student.get('student_id'))

    if len(x) == 0 or len(set(y)) < 2:
        return None

    clf = SVC(
        kernel="linear",
        probability=True,
        class_weight="balanced"
    )

    clf.fit(x, y)
    return {"clf":clf,"x":x,"y":y}

def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)

def predict_attendance(class_image_np):
    encodings = get_face_embedding(class_image_np)
    detected_student = {}
    model_data = get_trained_model()
    if not model_data:
        return {},[],len(encodings)
    clf = model_data["clf"]
    x_train = model_data['x']
    y_train = model_data['y']

    all_students = list(dict.fromkeys(y_train))

    for encoding in encodings:
        if len(all_students) >= 2:
            predicted_id = clf.predict([encoding])[0]
        else:
            predicted_id = all_students[0]
        student_embedding = x_train[y_train.index(predicted_id)]
        best_match_score = np.linalg.norm(student_embedding - encoding)
        resemblance_threshold = 0.6
        if best_match_score <= resemblance_threshold:
            detected_student[predicted_id] = True
    return detected_student,all_students,len(encodings)
    
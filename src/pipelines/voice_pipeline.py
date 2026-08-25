from resemblyzer import VoiceEncoder,preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st

@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()

def get_voice_embedding(audio_bytes):
    try:
        encoder = load_voice_encoder()
        audio,sr = librosa.load(io.BytesIO(audio_bytes),sr=16000)
        wav = preprocess_wav(audio)
        embedding = encoder.embed_utterance(wav)
        return embedding.tolist()
    except Exception as e:
        st.error("voice recog error")
        return None

def identify_spaker(new_embedding, candidate_dict, threshold=0.65):
    if new_embedding is None or not candidate_dict:
        return None, 0.0
    best_student_id = None
    best_score = -1.0
    for sid, stored_embedding in candidate_dict.items():
        if stored_embedding is not None:
            similarities = np.dot(
                np.asarray(stored_embedding, dtype=np.float32),
                np.asarray(new_embedding, dtype=np.float32),
            )
            if similarities >= best_score:
                best_score = similarities
                best_student_id = sid
    if best_score >= threshold:
        return best_student_id,best_score
    return None, best_score

def process_bulk_aviod(audio_bytes,candidate_dict,threshold = 0.65):
    try:
        encoder = load_voice_encoder()
        audio,sr = librosa.load(io.BytesIO(audio_bytes),sr=16000)
        segments = librosa.effects.split(audio,top_db=30)
        identified_results = {}
        for start, end in segments:
            if (end - start) < sr * 0.5: # these means audio is less then 0.5 sec
                continue
            segment_audio = audio[start:end]
            wav = preprocess_wav(segment_audio)
            embedding = encoder.embed_utterance(wav)

            best_student_id, best_score = identify_spaker(
                embedding, candidate_dict, threshold
            )
            if best_student_id is not None:
                if (
                    best_student_id not in identified_results
                    or best_score > identified_results[best_student_id]
                ):
                    identified_results[best_student_id] = best_score
        return identified_results
    except Exception as e:
        st.error(f"Bulk voice processing error: {e}")
        return {}

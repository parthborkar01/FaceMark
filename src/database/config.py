import streamlit as st
from supabase import create_client,client
from pathlib import Path
import tomllib


def load_secrets():
    try:
        return {
            "SUPABASE_URL": st.secrets["SUPABASE_URL"],
            "SUPABASE_KEY": st.secrets["SUPABASE_KEY"],
        }
    except st.errors.StreamlitSecretNotFoundError:
        secrets_path = Path(__file__).parents[2] / ".streamlit" / "secrects.toml"
        if not secrets_path.exists():
            raise RuntimeError(
                "Supabase secrets are missing. Add .streamlit/secrets.toml "
                "with SUPABASE_URL and SUPABASE_KEY."
            )
        return tomllib.loads(secrets_path.read_text(encoding="utf-8"))


secrets = load_secrets()

supabase: client = create_client(
    secrets["SUPABASE_URL"],
    secrets["SUPABASE_KEY"]
)
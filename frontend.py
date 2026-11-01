
import streamlit as st
import requests
  
API_URL = "http://127.0.0.1:8000/predict"

st.title("Insurance Premium Category Predictor")
st.markdown("Enter your details below:")

# Input fields
age = st.number_input("Age", min_value=1, max_value=119, value=30)
weight = st.number_input("Weight (kg)", min_value=1.0, value=65.0)
height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.7)
income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=10.0)
smoker = st.selectbox("Are you a smoker?", options=[True, False])
city = st.text_input("City", value="Mumbai")

occupation = st.selectbox(
    "Occupation",
    [
        'retired',
        'freelancer',
        'student',
        'government_job',
        'business_owner',
        'unemployed',
        'private_job'
    ]
)

if st.button("Predict Premium Category"):

    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        response = requests.post(
            API_URL,
            json=input_data,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()

            # Support both response formats
            prediction = result.get("response", result)

            st.success(
                f"Predicted Insurance Premium Category: "
                f"**{prediction['predicted_category']}**"
            )

            if "confidence" in prediction:
                st.write(
                    "🔍 Confidence:",
                    f"{prediction['confidence']:.2%}"
                )

            if "class_probabilities" in prediction:
                st.write("📊 Class Probabilities:")
                st.json(prediction["class_probabilities"])

        else:
            st.error(f"API Error: {response.status_code}")
            st.write(response.text)

    except requests.exceptions.ConnectionError:
        st.error(
            "❌ Could not connect to FastAPI. "
            "Make sure the backend is running."
        )

    except requests.exceptions.Timeout:
        st.error("⏳ API request timed out.")

    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")

    except (KeyError, ValueError) as e:
        st.error(f"Invalid API response: {e}")

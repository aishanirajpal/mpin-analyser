import streamlit as st
import datetime
from mpin_analyser import analyse_mpin_strength

def main():
    st.set_page_config(page_title="MPIN Security Analyser", layout="centered")
    st.title("MPIN Strength Analyser")
    st.write("Evaluate the security strength of your MPIN based on common patterns and demographic data.")

    # MPIN Input
    st.header("1. Enter your MPIN")
    mpin_length_choice = st.radio("Select MPIN Length:", ("4-digit", "6-digit"))
    if mpin_length_choice == "4-digit":
        mpin = st.text_input("Enter your 4-digit MPIN", max_chars=4, type="password")
    else:
        mpin = st.text_input("Enter your 6-digit MPIN", max_chars=6, type="password")

    mpin_valid = False
    if not mpin:
        st.info("Please enter an MPIN.")
    elif (mpin_length_choice == "4-digit" and len(mpin) != 4) or \
         (mpin_length_choice == "6-digit" and len(mpin) != 6):
        st.warning(f"Please enter a valid {mpin_length_choice} MPIN.")
    elif not mpin.isdigit():
        st.warning("MPIN must contain only digits.")
    else:
        mpin_valid = True

    # Demographic Inputs
    st.header("2. Enter Demographic Details (Optional)")
    st.info("Providing demographic details helps in a more accurate security assessment.")

    min_date = datetime.date(1940, 1, 1)
    today = datetime.date.today()

    dob_self = st.date_input("Your Date of Birth", value=None, min_value=min_date, max_value=today)
    dob_spouse = st.date_input("Spouse's Date of Birth (if applicable)", value=None, min_value=min_date, max_value=today)
    anniversary = st.date_input("Wedding Anniversary (if applicable)", value=None, min_value=min_date, max_value=today)

    demographics = {
        "dob_self": dob_self.strftime("%Y-%m-%d") if dob_self else None,
        "dob_spouse": dob_spouse.strftime("%Y-%m-%d") if dob_spouse else None,
        "anniversary": anniversary.strftime("%Y-%m-%d") if anniversary else None,
    }

    # Analyse Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        analyse_button = st.button("Analyse MPIN Strength", type="primary")

    if analyse_button:
        # This ensures analysis doesn't run with invalid data if dynamic checks were somehow missed.
        analysis_proceed = True
        if not mpin:
            st.warning("Please enter an MPIN to analyse.")
            analysis_proceed = False
        elif (mpin_length_choice == "4-digit" and len(mpin) != 4) or \
             (mpin_length_choice == "6-digit" and len(mpin) != 6):
            st.warning(f"Please enter a valid {mpin_length_choice} MPIN.")
            analysis_proceed = False
        elif not mpin.isdigit():
            st.warning("MPIN must contain only digits.")
            analysis_proceed = False

        if analysis_proceed:
            result = analyse_mpin_strength(mpin, demographics)
            st.subheader("Analysis Result:")
            if result["Strength"] == "WEAK":
                st.error(f"Strength: {result['Strength'].upper()}")
                st.write("Reasons for weakness:")
                # Display reasons as a single array string without underscores
                formatted_reasons = [reason.replace('_', ' ').upper() for reason in result["Reasons"]]
                st.code(str(formatted_reasons))
            else:
                st.success(f"Strength: {result['Strength'].upper()}")
                st.write("Your MPIN is strong based on the provided criteria.")

    st.markdown("""
    --- 
      Strength Analysis Explained:
    - **Commonly Used PINs:** Easily guessable PINs like 1234, 1111, 2020, etc., including patterns found on a phone keypad (e.g., 2580, 1470).
    - **Demographic-Based PINs:** Personalised but predictable patterns derived from your demographic data:
        - **Your Date of Birth:** Patterns derived from your own birth date.
        - **Spouse's Date of Birth:** Patterns derived from your spouse's birth date.
        - **Wedding Anniversary:** Patterns derived from your wedding anniversary.
    """)

if __name__ == "__main__":
    main()

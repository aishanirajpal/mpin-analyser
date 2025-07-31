# MPIN Security Analyser

This project provides a Streamlit application to evaluate the security strength of MPINs (Mobile Personal Identification Numbers) based on common patterns and demographic data.

#Files:

-   `streamlit_app.py`: This file contains the main Streamlit application. It provides a user interface for entering an MPIN and optional demographic details (Date of Birth, Anniversary, etc.). It then uses the `mpin_analyser.py` module to analyse the MPIN strength and displays the results.

-   `mpin_analyser.py`: This module contains the core logic for analysing MPIN strength. It checks for common weak patterns (e.g., repeating digits, sequential digits) and also assesses patterns based on provided demographic data (e.g., using birth dates, anniversaries as MPINs).

-   `run_analysis.py`: This script is likely used for running the MPIN analysis in a non-interactive or batch mode, separate from the Streamlit application. It would typically call functions from `mpin_analyser.py` to perform analyses.

# Methodology:

The analysis combines pattern recognition for common weak PINs using `regular expressions for pattern matching` with a demographic-based approach to identify easily guessable MPINs. This helps in providing a comprehensive security assessment beyond simple digit checks.
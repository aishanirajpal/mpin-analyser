from mpin_analyser import analyse_mpin_strength

def run_analysis():
    test_cases = [
        # 4-digit MPINs
        {"mpin": "1234", "demographics": {}, "description": "Commonly Used: 1234 (sequential)"},
        {"mpin": "1111", "demographics": {}, "description": "Commonly Used: 1111 (all same digits)"},
        {"mpin": "4321", "demographics": {}, "description": "Commonly Used: 4321 (reverse sequential)"},
        {"mpin": "1212", "demographics": {}, "description": "Commonly Used: 1212 (repeating pair)"},
        {"mpin": "1221", "demographics": {}, "description": "Commonly Used: 1221 (palindromic)"},
        {"mpin": "1122", "demographics": {}, "description": "Commonly Used: 1122 (consecutive repeating pairs)"},
        {"mpin": "0102", "demographics": {"dob_self": "1998-01-02"}, "description": "DOB Self: 0102 (MMDD)"},
        {"mpin": "0201", "demographics": {"dob_self": "1998-01-02"}, "description": "DOB Self: 0201 (DDMM)"},
        {"mpin": "9801", "demographics": {"dob_self": "1998-01-02"}, "description": "DOB Self: 9801 (YYMM)"},
        {"mpin": "1215", "demographics": {"dob_spouse": "1997-12-15"}, "description": "DOB Spouse: 1215 (MMDD)"},
        {"mpin": "0304", "demographics": {"anniversary": "2022-03-04"}, "description": "Anniversary: 0304 (MMDD)"},
        {"mpin": "0520", "demographics": {"child_dob": "2010-05-20"}, "description": "Child DOB: 0520 (MMDD)"},
        {"mpin": "1101", "demographics": {"pet_dob": "2015-11-01"}, "description": "Pet DOB: 1101 (MMDD)"},
        {"mpin": "3841", "demographics": {}, "description": "Strong: 3841"},
        {"mpin": "0102", "demographics": {"dob_self": "1998-01-02", "anniversary": "2022-03-04"}, "description": "Combined Weakness: DOB Self & Anniversary"},

        # 6-digit MPINs
        {"mpin": "123456", "demographics": {}, "description": "Commonly Used: 123456 (sequential)"},
        {"mpin": "111111", "demographics": {}, "description": "Commonly Used: 111111 (all same digits)"},
        {"mpin": "010298", "demographics": {"dob_self": "1998-01-02"}, "description": "DOB Self: 010298 (MMDDYY)"},
        {"mpin": "151297", "demographics": {"dob_spouse": "1997-12-15"}, "description": "DOB Spouse: 151297 (DDMMYY)"},
        {"mpin": "202203", "demographics": {"anniversary": "2022-03-04"}, "description": "Anniversary: 202203 (YYYYMM)"},
        {"mpin": "940281", "demographics": {}, "description": "Strong: 940281"},
        {"mpin": "0298", "demographics": {"dob_self": "1998-01-02"}, "description": "Partial match: 0298 (DDYY from DOB Self MMDDYY)"},
        {"mpin": "9801", "demographics": {"dob_self": "1998-01-02"}, "description": "Partial match: 9801 (YYMM from DOB Self YYYYMM)"},

        # Strong MPINs
        {"mpin": "7263", "demographics": {}, "description": "Strong: 7263"},
        {"mpin": "8059", "demographics": {}, "description": "Strong: 8059"},
        {"mpin": "130948", "demographics": {}, "description": "Strong: 130948"},
        {"mpin": "672154", "demographics": {}, "description": "Strong: 672154"},
        {"mpin": "500593", "demographics": {}, "description": "Strong: 500593"}
    ]

    print("--- MPIN Strength Analysis Results ---")
    for i, case in enumerate(test_cases):
        mpin = case["mpin"]
        demographics = case["demographics"]
        description = case["description"]
        result = analyse_mpin_strength(mpin, demographics)
        
        print(f"\nTest Case {i+1}: {description}")
        print(f"  MPIN: {mpin}")
        if demographics:
            print(f"  Demographics: {demographics}")
        print(f"  Strength: {result['Strength']}")
        print(f"  Reasons: {', '.join(result['Reasons']) if result['Reasons'] else 'None'}")

if __name__ == "__main__":
    run_analysis()
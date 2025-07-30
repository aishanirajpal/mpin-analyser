import unittest
import datetime
from mpin_analyzer import is_commonly_used, extract_date_patterns, analyze_mpin_strength

class TestMPINAnalyzer(unittest.TestCase):

    def test_is_commonly_used_4_digit(self):
        self.assertTrue(is_commonly_used("1111", 4))
        self.assertTrue(is_commonly_used("1234", 4))
        self.assertTrue(is_commonly_used("4321", 4))
        self.assertTrue(is_commonly_used("1357", 4)) # All odd
        self.assertTrue(is_commonly_used("2468", 4)) # All even
        self.assertTrue(is_commonly_used("1212", 4)) # Repeated two-digit
        self.assertTrue(is_commonly_used("1221", 4)) # Palindromic
        self.assertTrue(is_commonly_used("1122", 4)) # Consecutive repeating pairs
        self.assertFalse(is_commonly_used("3841", 4))

    def test_is_commonly_used_6_digit(self):
        self.assertTrue(is_commonly_used("111111", 6))
        self.assertTrue(is_commonly_used("012345", 6))
        self.assertTrue(is_commonly_used("987654", 6))
        self.assertTrue(is_commonly_used("135791", 6)) # All odd
        self.assertTrue(is_commonly_used("024680", 6)) # All even
        self.assertTrue(is_commonly_used("121212", 6)) # Repeated two-digit
        self.assertTrue(is_commonly_used("123123", 6)) # Repeated three-digit
        self.assertTrue(is_commonly_used("123321", 6)) # Palindromic
        self.assertTrue(is_commonly_used("112233", 6)) # Consecutive repeating pairs
        self.assertFalse(is_commonly_used("940281", 6))

    def test_extract_date_patterns(self):
        # Test with a regular date
        self.assertIn("0102", extract_date_patterns("1998-01-02"))  # MMDD
        self.assertIn("0201", extract_date_patterns("1998-01-02"))  # DDMM
        self.assertIn("9801", extract_date_patterns("1998-01-02"))  # YYMM
        self.assertIn("0198", extract_date_patterns("1998-01-02"))  # MMYY
        self.assertIn("1998", extract_date_patterns("1998-01-02"))  # YYYY
        self.assertIn("010298", extract_date_patterns("1998-01-02")) # MMDDYY
        self.assertIn("020198", extract_date_patterns("1998-01-02")) # DDMMYY
        self.assertIn("199801", extract_date_patterns("1998-01-02")) # YYYYMM
        self.assertIn("199802", extract_date_patterns("1998-01-02")) # YYYYDD

        # Test with reversed dates
        self.assertIn("0102", extract_date_patterns("2098-01-02")) # MMDD
        self.assertIn("0201", extract_date_patterns("2098-01-02")) # DDMM
        self.assertIn("9801", extract_date_patterns("2098-01-02")) # YYMM

        # Test with invalid date
        self.assertEqual([], extract_date_patterns("invalid-date"))
        self.assertEqual([], extract_date_patterns(None))

    def test_analyze_mpin_strength_4_digit(self):
        # Commonly Used
        result = analyze_mpin_strength("1234", {})
        self.assertEqual(result["Strength"], "WEAK")
        self.assertIn("COMMONLY_USED", result["Reasons"])

        # Demographic - DOB Self
        demographics = {"dob_self": "1998-01-02", "dob_spouse": None, "anniversary": None}
        result = analyze_mpin_strength("0102", demographics)
        self.assertEqual(result["Strength"], "WEAK")
        self.assertIn("DEMOGRAPHIC_DOB_SELF", result["Reasons"])

        # Demographic - DOB Spouse
        demographics = {"dob_self": "1990-01-01", "dob_spouse": "1997-12-15", "anniversary": None}
        result = analyze_mpin_strength("1215", demographics)
        self.assertEqual(result["Strength"], "WEAK")
        self.assertIn("DEMOGRAPHIC_DOB_SPOUSE", result["Reasons"])

        # Demographic - Anniversary
        demographics = {"dob_self": "1990-01-01", "dob_spouse": None, "anniversary": "2022-03-04"}
        result = analyze_mpin_strength("0304", demographics)
        self.assertEqual(result["Strength"], "WEAK")
        self.assertIn("DEMOGRAPHIC_ANNIVERSARY", result["Reasons"])

        # Demographic - Child DOB
        demographics = {"dob_self": None, "child_dob": "2010-05-20"}
        result = analyze_mpin_strength("0520", demographics)
        self.assertEqual(result["Strength"], "WEAK")
        self.assertIn("DEMOGRAPHIC_CHILD_DOB", result["Reasons"])

        # Demographic - Pet DOB
        demographics = {"dob_self": None, "pet_dob": "2015-11-01"}
        result = analyze_mpin_strength("1101", demographics)
        self.assertEqual(result["Strength"], "WEAK")
        self.assertIn("DEMOGRAPHIC_PET_DOB", result["Reasons"])

        # Strong PIN
        result = analyze_mpin_strength("3841", {})
        self.assertEqual(result["Strength"], "STRONG")
        self.assertEqual(len(result["Reasons"]), 0)

        # Combined Reasons
        demographics = {"dob_self": "1998-01-02", "anniversary": "2022-03-04"}
        result = analyze_mpin_strength("0102", demographics)
        self.assertEqual(result["Strength"], "WEAK")
        self.assertIn("DEMOGRAPHIC_DOB_SELF", result["Reasons"])

    def test_analyze_mpin_strength_6_digit(self):
        # Commonly Used
        result = analyze_mpin_strength("123456", {})
        self.assertEqual(result["Strength"], "WEAK")
        self.assertIn("COMMONLY_USED", result["Reasons"])

        # Demographic - DOB Self (MMDDYY)
        demographics = {"dob_self": "1998-01-02", "dob_spouse": None, "anniversary": None}
        result = analyze_mpin_strength("010298", demographics)
        self.assertEqual(result["Strength"], "WEAK")
        self.assertIn("DEMOGRAPHIC_DOB_SELF", result["Reasons"])

        # Demographic - DOB Spouse (DDMMYY)
        demographics = {"dob_self": "1990-01-01", "dob_spouse": "1997-12-15", "anniversary": None}
        result = analyze_mpin_strength("151297", demographics)
        self.assertEqual(result["Strength"], "WEAK")
        self.assertIn("DEMOGRAPHIC_DOB_SPOUSE", result["Reasons"])

        # Demographic - Anniversary (YYYYMM)
        demographics = {"dob_self": "1990-01-01", "dob_spouse": None, "anniversary": "2022-03-04"}
        result = analyze_mpin_strength("202203", demographics)
        self.assertEqual(result["Strength"], "WEAK")
        self.assertIn("DEMOGRAPHIC_ANNIVERSARY", result["Reasons"])

        # Strong PIN
        result = analyze_mpin_strength("940281", {})
        self.assertEqual(result["Strength"], "STRONG")
        self.assertEqual(len(result["Reasons"]), 0)

        # Partial match for 4-digit PIN against 6-digit date patterns
        demographics = {"dob_self": "1998-01-02"}
        result = analyze_mpin_strength("0102", demographics) # MMDD from MMDDYY
        self.assertEqual(result["Strength"], "WEAK")
        self.assertIn("DEMOGRAPHIC_DOB_SELF", result["Reasons"])

        result = analyze_mpin_strength("0298", demographics) # DDYY from MMDDYY
        self.assertEqual(result["Strength"], "WEAK")
        self.assertIn("DEMOGRAPHIC_DOB_SELF", result["Reasons"])

        result = analyze_mpin_strength("9801", demographics) # YYMM from YYYYMM
        self.assertEqual(result["Strength"], "WEAK")
        self.assertIn("DEMOGRAPHIC_DOB_SELF", result["Reasons"])


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
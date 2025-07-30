import datetime
import re

def is_commonly_used(mpin: str, pin_length: int) -> bool:
    """
    Checks if a given MPIN is commonly used based on dynamic regex patterns.
    """
    if not mpin.isdigit() or len(mpin) != pin_length:
        return False

    # All same digits
    if re.fullmatch(f"^(\\d)\\1{{{pin_length - 1}}}$", mpin):
        return True

    # Sequential digits (ascending and descending)
    is_sequential_asc = True
    is_sequential_desc = True
    for i in range(pin_length - 1):
        if int(mpin[i+1]) != (int(mpin[i]) + 1) % 10:
            is_sequential_asc = False
        if int(mpin[i+1]) != (int(mpin[i]) - 1 + 10) % 10:
            is_sequential_desc = False
    if is_sequential_asc or is_sequential_desc:
        return True

    # All odd or all even digits
    if re.fullmatch(f"^[13579]{{{pin_length}}}$", mpin): # All odd
        return True
    if re.fullmatch(f"^[02468]{{{pin_length}}}$", mpin): # All even
        return True

    # Repeating sequences
    if pin_length == 4:
        if re.fullmatch(r"^(\d{2})\1$", mpin): # e.g., 1212
            return True
    elif pin_length == 6:
        if re.fullmatch(r"^(\d{2})\1{2}$", mpin) or re.fullmatch(r"^(\d{3})\1$", mpin): # e.g., 121212 or 123123
            return True

    # Palindromic/Mirrored patterns
    if pin_length == 4:
        if re.fullmatch(r"^(\d)(\d)\2\1$", mpin): # e.g., 1221
            return True
    elif pin_length == 6:
        if re.fullmatch(r"^(\d)(\d)(\d)\3\2\1$", mpin): # e.g., 123321
            return True

    # Consecutive repeating pairs (e.g., 1122, 223344)
    if pin_length == 4:
        if re.fullmatch(r"^(.)\1(.)\2$", mpin): # e.g., 1122
            return True
    elif pin_length == 6:
        if re.fullmatch(r"^(.)\1(.)\2(.)\3$", mpin): # e.g., 112233
            return True

    return False

def extract_date_patterns(date_str: str) -> list[str]:
    """
    Extracts various 4-digit and 6-digit patterns from a date string (YYYY-MM-DD).
    These patterns are designed to be directly usable as literal strings for regex matching.
    """
    if not date_str:
        return []

    try:
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        year_str = str(date_obj.year)
        month_str = f"{date_obj.month:02d}"
        day_str = f"{date_obj.day:02d}"

        patterns = []

        # 4-digit patterns
        patterns.append(f"{month_str}{day_str}")  # MMDD
        patterns.append(f"{day_str}{month_str}")  # DDMM
        patterns.append(f"{year_str[2:]}{month_str}")  # YYMM
        patterns.append(f"{month_str}{year_str[2:]}")  # MMYY
        patterns.append(year_str) # YYYY (4-digit)
        patterns.append(year_str[2:] + year_str[2:]) # YY YY

        # 6-digit patterns
        patterns.append(f"{month_str}{day_str}{year_str[2:]}") # MMDDYY
        patterns.append(f"{day_str}{month_str}{year_str[2:]}") # DDMMYY
        patterns.append(year_str + month_str) # YYYYMM (6-digit)
        patterns.append(year_str + day_str) # YYYYDD (6-digit)
        patterns.append(f"{year_str[2:]}{month_str}{day_str}") # YYMMDD
        patterns.append(f"{month_str}{year_str[2:]}{day_str}") # MMYYDD
        patterns.append(f"{day_str}{year_str[2:]}{month_str}") # DDYYMM

        return patterns
    except ValueError:
        return []

def analyze_mpin_strength(mpin: str, demographics: dict) -> dict:
    """
    Evaluates the security strength of an MPIN based on common usage and demographic data.
    """
    strength = "STRONG"
    reasons = []
    pin_length = len(mpin)

    # Check for commonly used PINs using regex
    if is_commonly_used(mpin, pin_length):
        reasons.append("COMMONLY_USED")
        strength = "WEAK"

    # Check against demographic data using regex
    demographic_fields = {
        "dob_self": "DEMOGRAPHIC_DOB_SELF",
        "dob_spouse": "DEMOGRAPHIC_DOB_SPOUSE",
        "anniversary": "DEMOGRAPHIC_ANNIVERSARY",
        "child_dob": "DEMOGRAPHIC_CHILD_DOB",
        "pet_dob": "DEMOGRAPHIC_PET_DOB"
    }

    for field, reason_key in demographic_fields.items():
        date_value = demographics.get(field)
        if date_value:
            date_patterns = extract_date_patterns(date_value)
            for pattern_str in date_patterns:
                # Exact match for same length
                if len(mpin) == len(pattern_str) and re.fullmatch(re.escape(pattern_str), mpin):
                    if reason_key not in reasons:
                        reasons.append(reason_key)
                        strength = "WEAK"
                # Partial match for 4-digit PINs within 6-digit date patterns
                elif len(mpin) == 4 and len(pattern_str) == 6:
                    # Check if the 4-digit MPIN is a prefix or suffix of the 6-digit pattern
                    if re.match(re.escape(mpin), pattern_str) or re.search(re.escape(mpin) + "$", pattern_str):
                        if reason_key not in reasons:
                            reasons.append(reason_key)
                            strength = "WEAK"

    return {"Strength": strength, "Reasons": reasons}

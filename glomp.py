import math, re


def contains_patterns(password: str) -> int:
    """
    Checks for common patterns in the password.
    Returns the number of detected patterns.
    """
    patterns = [
        # Alphabetical patterns
        "abc", "bcd", "cde", "def", "efg", "fgh", "ghi", "hij", "ijk", "jkl", "klm", "lmn", "mno", "nop", "opq", "pqr", "qrs", "rst", "stu", "tuv", "uvw", "vwx", "wxy", "xyz",
        "zyx", "yxw", "xwv", "wvu", "vut", "uts", "tsr", "srq", "rqp", "qpo", "pon", "onm", "nml", "mlk", "lkj", "kji", "jih", "ihg", "hgf", "gfe", "fed", "edc", "dcb", "cba",
        # Keyboard patterns
        "qwe", "wer", "ert", "rty", "tyu", "yui", "uio", "iop", "asd", "sdf", "dfg", "fgh", "ghj", "hjk", "jkl", "zxc", "xcv", "cvb", "vbn", "bnm",
        # Number patterns
        "123", "234", "345", "456", "567", "678", "789", "890", "098", "987", "876", "765", "654", "543", "432", "321",
        # Numpad patterns (common ones)
        "147", "258", "369", "741", "852", "963", "159", "357", "951", "753", "456", "654", "8520", "2580"
    ]
    count = 0
    lower_pw = password.lower()
    for pat in patterns:
        if pat in lower_pw:
            count += 1
    return count


def password_check(password: str) -> tuple:
    """
    Check strength of a password.
    Args:
    - password (str): The password to check.
    Returns:
    - tuple: A tuple containing a boolean indicating if the password is valid and a string of its strength, as well as the calculated entropy.
        - bool: True if valid, False otherwise.
        - str: "Weak", "Medium", or "Strong" based on the password's strength.
        - float: The calculated entropy of the password.
    """
    # calculate entropy
    entropy = 0
    length = len(password)
    unique_characters = len(set(password))

    # Basic entropy calculation
    if length > 0:
        entropy = math.log2(95 ** length)  # 95 printable ASCII characters

    # Adjust entropy based on unique characters
    if unique_characters > 0:
        entropy *= unique_characters / length

    entropy = (entropy ** 1.4) / 10 # do some meaningles transfomration to nerf lower entropy so password1234 isnt Strong

    # Penalize for patterns
    pattern_count = contains_patterns(password)
    entropy -= 5 * pattern_count

    # Determine strength
    if entropy < 10:
        strength = "Very Weak"
        valid = False
    elif 10 <= entropy < 20:
        strength = "Weak"
        valid = False
    elif 20 <= entropy < 40:
        strength = "Medium"
        valid = True
    elif 40 <= entropy < 60:
        strength = "Strong"
        valid = True
    elif 60 <= entropy < 100:
        strength = "Very Strong"
        valid = True
    else:
        strength = "Extremely Strong"
        valid = True

    return valid, strength, entropy

# test
passwords = [
    "password1234",
    "Bapple1234",
    "Gl0Mp!x",
    "bapplekururinfeetdashtriangleorboids",
    "letmein",
    "93225"
]

print("temmie is trying to glomp you")

for password in passwords:
    valid, strength, entropy = password_check(password)
    if valid:
        print(f"Password '{password}' is \033[92mvalid\033[0m and its strength is: {strength} (Entropy: {entropy:.2f})")
        print("\033[92mtemmie nibbled on your password. nothing happened\033[0m")
    else:
        print(f"Password '{password}' is \033[91minvalid\033[0m and its strength is: {strength} (Entropy: {entropy:.2f})")
        print("\033[91mtemmie glomped your password because it was too weak.\033[0m")
    print("\n") # two newlines
# because HSJ doesnt have mosto f the control characters, it has more useufl characters than ASCII that all fit in 256 values! this comment is used to check to make sure all the characters are monospaced.. it goes on and on and on and on and on and on
HSJ_SET = " \n0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~äÄöÖß§┌┐└┘├┤┬┴─│┼╔╗╚╝╠╣╦╩═║╬░▒▓█▀▄▌▐━┃┯┷┠┨┿╀╁╂╃╄╅╆╇╈╉╊╋←↑→↓↔↕¦™©®±²³⁰⁴⁵⁶⁷⁸⁹⁺⁻₀₁₂₃₄₅₆₇₈₉                                                                         "
print(len(HSJ_SET))  # 256 characters
print(f"{256 - len(HSJ_SET)} to go!")
print("NON UNIQUE CHARACTERS DETECTED" if len(HSJ_SET) != len(list(set(HSJ_SET))) else "All characters are unique!")
if len(HSJ_SET) != len(list(set(HSJ_SET))):
    bad = []
    for char in HSJ_SET:
        if HSJ_SET.count(char) > 1 and char not in bad:
            bad.append(char)
    print(f"Duplicate characters detected: {', '.join(bad)}")
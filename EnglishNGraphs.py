import string

# Letters
VOWELS = list("AEIOU")
Y = ["Y"]
CONSONANTS = [l for l in string.ascii_uppercase if ((l not in VOWELS) and (l not in Y))]

# Letter config
LETTER_TYPES = [VOWELS, CONSONANTS, Y]
TYPE_WEIGHTS = [.3, .65, .05]

MIN_WORD_LEN = 3
MAX_C_IN_ROW = 5
MAX_V_IN_ROW = 4
MAX_LEN_WITHOUT_MATCH = 12

# NGraphs
S = "S"
T = "T"
LIQUID = list("LR")
LIQUID_PAIR = list("CDTGKBPW")
SOFT = list("LRN")
HCHUNK = [l + "H" for l in "CSPGTWK"]


# 2Graphs
S_PLUS = [S + c for c in CONSONANTS]
PLUS_LIQUID = [c + l for c in LIQUID_PAIR for l in LIQUID]
DOUBLE = [c + c for c in list("WRTPLKHGFDZXCVBNM")]

PLUS_S = [c + S for c in CONSONANTS]
PLUS_T = [c + T for c in CONSONANTS]
SOFT_PLUS = [s + c for s in SOFT for c in CONSONANTS]

TWO_C_START = HCHUNK + S_PLUS + PLUS_LIQUID + ["TW", "QU", "GN", "TS"]
TWO_C_END = TWO_C_START + DOUBLE + SOFT_PLUS + ["CK", "WT", "WN", "MN", "MB", "GM"]
# TWO_C == accept anything


# 3Graphs
H_SOFT = [h + s for h in HCHUNK for s in LIQUID]
THREE_ST = [c + S + T for c in CONSONANTS]
THREE_TS = [c + T + S for c in CONSONANTS]
PLUS_2START = [c + t for c in CONSONANTS for t in TWO_C_START]
TWO_END_PLUS = [t + c for t in TWO_C_END for c in CONSONANTS]

THREE_C_START = H_SOFT + ["SPL", "SQU", "SCH", "SPH", "SCR"]
THREE_C_END = THREE_C_START + THREE_ST + THREE_TS
THREE_C = THREE_C_END + PLUS_2START + TWO_END_PLUS + ["TCH", "DGM"]


# 4Graphs
PLUS_3START = [c + t for c in CONSONANTS for t in THREE_C_START]
THREE_END_PLUS = [t + c for t in THREE_C_END for c in CONSONANTS]
TWO_TWO = [e + s for e in TWO_C_END for s in TWO_C_START]

FOUR_C_START = ["SCHR"]
FOUR_C = PLUS_3START + THREE_END_PLUS + TWO_TWO


# 5Graphs
THREE_TWO = [th + tw for th in THREE_C_END for tw in TWO_C_START]
TWO_THREE = [tw + th for tw in TWO_C_END for th in THREE_C_END]
# FIVE_C_START == don't accept anything
FIVE_C = THREE_TWO + TWO_THREE


# 6Graphs
# SIX_START == don't accept anything
SIX_C = [e + s for e in THREE_C_END for s in THREE_C_START]


# 2V
#Allow any 1, 2 combo vowels
THREE_V = ["EAU", "OUI", "EOU", "IOU", "UOU", "UEU", "OIA", "IAE", "EAE", "AIA"]
FOUR_V = ["UOIA", "UEUE"]
FIVE_V = ["UEUEI"]


def check_current_word(current_word, letter, c_in_a_row, v_in_a_row, l_in_a_row):
    if l_in_a_row >= MAX_LEN_WITHOUT_MATCH:
        should_continue = False
    else:
        should_continue = True
        is_vowel = False
        is_consonant = False

        # Consecutive letter type count
        if letter in VOWELS:
            v_in_a_row += 1
            c_in_a_row = 0
            is_vowel = True
        elif letter == Y:
            v_in_a_row = 0
            c_in_a_row = 0
        else:
            c_in_a_row += 1
            v_in_a_row = 0
            is_consonant = True

        # Check for viable letter combo
        if c_in_a_row > MAX_C_IN_ROW or v_in_a_row > MAX_V_IN_ROW:
            should_continue = False
        else:
            if is_consonant:
                should_continue = check_consonant_combo(current_word, c_in_a_row)
            elif is_vowel:
                should_continue = check_vowel_combo(current_word, v_in_a_row)

    return should_continue, c_in_a_row, v_in_a_row


def check_for_stretch_w_o_match(current_word, l_in_a_row):

    if l_in_a_row < MAX_LEN_WITHOUT_MATCH:
        should_continue = True
    else:
        should_continue = False

    return should_continue


def check_consonant_combo(current_word, c_in_a_row):
    should_continue = False

    # Determine cluster
    if c_in_a_row == len(current_word):
        cluster = current_word
        is_at_start = True
    else:
        cluster = current_word[-c_in_a_row:]
        is_at_start = False

    # Check cluster
    if is_at_start:
        if c_in_a_row == 1:
            should_continue = True
        elif c_in_a_row == 2:
            if cluster in TWO_C_START:
                should_continue = True
        elif c_in_a_row == 3:
            if cluster in THREE_C_START:
                should_continue = True
        elif c_in_a_row == 4:
            if cluster in FOUR_C_START:
                should_continue = True
    else:
        if c_in_a_row == 1:
            should_continue = True
        elif c_in_a_row == 2:
            should_continue = True
        elif c_in_a_row == 3:
            if cluster in THREE_C:
                should_continue = True
        elif c_in_a_row == 4:
            if cluster in FOUR_C:
                should_continue = True
        elif c_in_a_row == 5:
            if cluster in FIVE_C:
                should_continue = True
        elif c_in_a_row == 6:
            if cluster in SIX_C:
                should_continue = True

    return should_continue


def check_vowel_combo(current_word, v_in_a_row):
    should_continue = True

    # Determine cluster
    if v_in_a_row == len(current_word):
        cluster = current_word
    else:
        cluster = current_word[-v_in_a_row:]

    if v_in_a_row > 2:
        if v_in_a_row == 3:
            if cluster not in THREE_V:
                should_continue = False
        elif v_in_a_row == 4:
            if cluster not in FOUR_V:
                should_continue = False
        elif v_in_a_row == 5:
            if cluster not in FIVE_V:
                should_continue = False

    return should_continue

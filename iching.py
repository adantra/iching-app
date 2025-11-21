import random

class IChing:
    def __init__(self):
        self.lines = []
        self.hexagram_lines = []
        self.future_hexagram_lines = []

    def cast_coin(self):
        """Simulates tossing 3 coins. Heads=3, Tails=2. Returns sum."""
        # 3 is Heads (Yang), 2 is Tails (Yin)
        # Traditional method:
        # 3 heads (3+3+3=9) -> Old Yang (Moving) - O
        # 3 tails (2+2+2=6) -> Old Yin (Moving) - X
        # 2 heads 1 tail (3+3+2=8) -> Young Yin (Static) - --
        # 1 head 2 tails (3+2+2=7) -> Young Yang (Static) - -
        toss = [random.choice([2, 3]) for _ in range(3)]
        return sum(toss)

    def cast_hexagram(self):
        """Generates a full hexagram (6 lines)."""
        self.lines = []
        self.hexagram_lines = []
        self.future_hexagram_lines = []

        for _ in range(6):
            value = self.cast_coin()
            self.lines.append(value)
            
            # Determine current and future lines
            if value == 6: # Old Yin (Moving)
                self.hexagram_lines.append(0) # Yin
                self.future_hexagram_lines.append(1) # Becomes Yang
            elif value == 7: # Young Yang (Static)
                self.hexagram_lines.append(1) # Yang
                self.future_hexagram_lines.append(1) # Stays Yang
            elif value == 8: # Young Yin (Static)
                self.hexagram_lines.append(0) # Yin
                self.future_hexagram_lines.append(0) # Stays Yin
            elif value == 9: # Old Yang (Moving)
                self.hexagram_lines.append(1) # Yang
                self.future_hexagram_lines.append(0) # Becomes Yin

        return {
            "raw_values": self.lines,
            "hexagram": self.hexagram_lines,
            "future_hexagram": self.future_hexagram_lines
        }

    def get_hexagram_info(self, lines):
        """
        Identifies the hexagram from the list of lines (0=Yin, 1=Yang).
        Lines are bottom-to-top.
        Returns a dictionary with number, name, and character.
        """
        # Convert lines to binary string (Top to Bottom for standard binary reading, 
        # but I Ching is often constructed Bottom to Top. 
        # Let's use a tuple key (bottom, ..., top) to be unambiguous.
        key = tuple(lines)
        return HEXAGRAM_LOOKUP.get(key, {"number": 0, "name": "Unknown", "character": "?"})

# Full Lookup Table (Bottom line first)
# 0 = Yin (Broken), 1 = Yang (Solid)
HEXAGRAM_LOOKUP = {
    (1, 1, 1, 1, 1, 1): {"number": 1, "name": "The Creative (Chien)", "character": "䷀"},
    (0, 0, 0, 0, 0, 0): {"number": 2, "name": "The Receptive (Kun)", "character": "䷁"},
    (1, 0, 0, 0, 1, 0): {"number": 3, "name": "Difficulty at the Beginning (Chun)", "character": "䷂"},
    (0, 1, 0, 0, 0, 1): {"number": 4, "name": "Youthful Folly (Meng)", "character": "䷃"},
    (1, 1, 1, 0, 1, 0): {"number": 5, "name": "Waiting (Hsu)", "character": "䷄"},
    (0, 1, 0, 1, 1, 1): {"number": 6, "name": "Conflict (Sung)", "character": "䷅"},
    (0, 1, 0, 0, 0, 0): {"number": 7, "name": "The Army (Shih)", "character": "䷆"},
    (0, 0, 0, 0, 1, 0): {"number": 8, "name": "Holding Together (Pi)", "character": "䷇"},
    (1, 1, 1, 0, 1, 1): {"number": 9, "name": "The Taming Power of the Small (Hsiao Chu)", "character": "䷈"},
    (1, 1, 0, 1, 1, 1): {"number": 10, "name": "Treading (Lu)", "character": "䷉"},
    (1, 1, 1, 0, 0, 0): {"number": 11, "name": "Peace (Tai)", "character": "䷊"},
    (0, 0, 0, 1, 1, 1): {"number": 12, "name": "Standstill (Pi)", "character": "䷋"},
    (1, 0, 1, 1, 1, 1): {"number": 13, "name": "Fellowship with Men (Tung Jen)", "character": "䷌"},
    (1, 1, 1, 1, 0, 1): {"number": 14, "name": "Possession in Great Measure (Ta Yu)", "character": "䷍"},
    (0, 0, 1, 0, 0, 0): {"number": 15, "name": "Modesty (Chien)", "character": "䷎"},
    (0, 0, 0, 1, 0, 0): {"number": 16, "name": "Enthusiasm (Yu)", "character": "䷏"},
    (1, 0, 0, 1, 1, 0): {"number": 17, "name": "Following (Sui)", "character": "䷐"},
    (0, 1, 1, 0, 0, 1): {"number": 18, "name": "Work on What Has Been Spoiled (Ku)", "character": "䷑"},
    (1, 1, 0, 0, 0, 0): {"number": 19, "name": "Approach (Lin)", "character": "䷒"},
    (0, 0, 0, 0, 1, 1): {"number": 20, "name": "Contemplation (Kuan)", "character": "䷓"},
    (1, 0, 0, 1, 0, 1): {"number": 21, "name": "Biting Through (Shih Ho)", "character": "䷔"},
    (1, 0, 1, 0, 0, 1): {"number": 22, "name": "Grace (Pi)", "character": "䷕"},
    (0, 0, 0, 0, 0, 1): {"number": 23, "name": "Splitting Apart (Po)", "character": "䷖"},
    (1, 0, 0, 0, 0, 0): {"number": 24, "name": "Return (Fu)", "character": "䷗"},
    (1, 0, 0, 1, 1, 1): {"number": 25, "name": "Innocence (Wu Wang)", "character": "䷘"},
    (1, 1, 1, 0, 0, 1): {"number": 26, "name": "The Taming Power of the Great (Ta Chu)", "character": "䷙"},
    (1, 0, 0, 0, 0, 1): {"number": 27, "name": "The Corners of the Mouth (I)", "character": "䷚"},
    (0, 1, 1, 1, 1, 0): {"number": 28, "name": "Preponderance of the Great (Ta Kuo)", "character": "䷛"},
    (0, 1, 0, 0, 1, 0): {"number": 29, "name": "The Abysmal (Kan)", "character": "䷜"},
    (1, 0, 1, 1, 0, 1): {"number": 30, "name": "The Clinging (Li)", "character": "䷝"},
    (0, 0, 1, 1, 1, 0): {"number": 31, "name": "Influence (Hsien)", "character": "䷞"},
    (0, 1, 1, 1, 0, 0): {"number": 32, "name": "Duration (Heng)", "character": "䷟"},
    (0, 0, 1, 1, 1, 1): {"number": 33, "name": "Retreat (Tun)", "character": "䷠"},
    (1, 1, 1, 1, 0, 0): {"number": 34, "name": "The Power of the Great (Ta Chuang)", "character": "䷡"},
    (0, 0, 0, 1, 0, 1): {"number": 35, "name": "Progress (Chin)", "character": "䷢"},
    (1, 0, 1, 0, 0, 0): {"number": 36, "name": "Darkening of the Light (Ming I)", "character": "䷣"},
    (1, 0, 1, 0, 1, 1): {"number": 37, "name": "The Family (Chia Jen)", "character": "䷤"},
    (1, 1, 0, 1, 0, 1): {"number": 38, "name": "Opposition (Kuei)", "character": "䷥"},
    (0, 0, 1, 0, 1, 0): {"number": 39, "name": "Obstruction (Chien)", "character": "䷦"},
    (0, 1, 0, 1, 0, 0): {"number": 40, "name": "Deliverance (Hsieh)", "character": "䷧"},
    (1, 1, 0, 0, 0, 1): {"number": 41, "name": "Decrease (Sun)", "character": "䷨"},
    (1, 0, 0, 0, 1, 1): {"number": 42, "name": "Increase (I)", "character": "䷩"},
    (1, 1, 1, 1, 1, 0): {"number": 43, "name": "Break-through (Kuai)", "character": "䷪"},
    (0, 1, 1, 1, 1, 1): {"number": 44, "name": "Coming to Meet (Kou)", "character": "䷫"},
    (0, 0, 0, 1, 1, 0): {"number": 45, "name": "Gathering Together (Tsui)", "character": "䷬"},
    (0, 1, 1, 0, 0, 0): {"number": 46, "name": "Pushing Upward (Sheng)", "character": "䷭"},
    (0, 1, 0, 1, 1, 0): {"number": 47, "name": "Oppression (Kun)", "character": "䷮"},
    (0, 1, 1, 0, 1, 0): {"number": 48, "name": "The Well (Ching)", "character": "䷯"},
    (1, 0, 1, 1, 1, 0): {"number": 49, "name": "Revolution (Ko)", "character": "䷰"},
    (0, 1, 1, 1, 0, 1): {"number": 50, "name": "The Cauldron (Ting)", "character": "䷱"},
    (1, 0, 0, 1, 0, 0): {"number": 51, "name": "The Arousing (Chen)", "character": "䷲"},
    (0, 0, 1, 0, 0, 1): {"number": 52, "name": "Keeping Still (Ken)", "character": "䷳"},
    (0, 0, 1, 0, 1, 1): {"number": 53, "name": "Development (Chien)", "character": "䷴"},
    (1, 1, 0, 1, 0, 0): {"number": 54, "name": "The Marrying Maiden (Kuei Mei)", "character": "䷵"},
    (1, 0, 1, 1, 0, 0): {"number": 55, "name": "Abundance (Feng)", "character": "䷶"},
    (0, 0, 1, 1, 0, 1): {"number": 56, "name": "The Wanderer (Lu)", "character": "䷷"},
    (0, 1, 1, 0, 1, 1): {"number": 57, "name": "The Gentle (Sun)", "character": "䷸"},
    (1, 1, 0, 1, 1, 0): {"number": 58, "name": "The Joyous (Tui)", "character": "䷹"},
    (0, 1, 0, 0, 1, 1): {"number": 59, "name": "Dispersion (Huan)", "character": "䷺"},
    (1, 1, 0, 0, 1, 0): {"number": 60, "name": "Limitation (Chieh)", "character": "䷻"},
    (1, 1, 0, 0, 1, 1): {"number": 61, "name": "Inner Truth (Chung Fu)", "character": "䷼"},
    (0, 0, 1, 1, 0, 0): {"number": 62, "name": "Preponderance of the Small (Hsiao Kuo)", "character": "䷽"},
    (1, 0, 1, 0, 1, 0): {"number": 63, "name": "After Completion (Chi Chi)", "character": "䷾"},
    (0, 1, 0, 1, 0, 1): {"number": 64, "name": "Before Completion (Wei Chi)", "character": "䷿"},
}

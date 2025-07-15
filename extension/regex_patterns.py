import re

class RegexPatterns:
    __EMAIL = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
    __ARABIC_LETTERS = re.compile(r'[\u0600-\u06FF]')
    __FORMATION = re.compile(r'[\u0610-\u061A\u064B-\u065F\u06D6-\u06ED]')

    @classmethod
    def match_email(cls, value):
        return cls.__EMAIL.match(value)

    @classmethod
    def contains_arabic(cls, value):
        return cls.__ARABIC_LETTERS.search(value)

    @classmethod
    def contains_formation(cls, value):
        return cls.__FORMATION.search(value)
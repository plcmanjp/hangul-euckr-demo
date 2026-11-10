"""초·중·종성으로 한글을 조합하고 Python EUC-KR 바이트로 변환하는 예제."""

# --------------------------------------------
# 초성 / 중성 / 종성
# --------------------------------------------

CHO = [
    'ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ',
    'ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'
]

JUNG = [
    'ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ',
    'ㅗ','ㅘ','ㅙ','ㅚ','ㅛ',
    'ㅜ','ㅝ','ㅞ','ㅟ','ㅠ',
    'ㅡ','ㅢ','ㅣ'
]

JONG = [
    '',
    'ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ',
    'ㄷ',
    'ㄹ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ',
    'ㅁ','ㅂ','ㅄ',
    'ㅅ','ㅆ','ㅇ',
    'ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'
]


# ============================================
# 한글 조합
# ============================================

def compose_hangul(chosung: str, jungsung: str, jongsung: str = '') -> str:
    """호환 자모(예: ㄱ, ㅏ, ㄴ)를 받아 현대 한글 한 글자를 반환한다.

    받침은 생략할 수 있다. 해당 위치에 쓸 수 없는 자모는 ValueError를 낸다.
    U+1100 계열의 결합 자모나 두벌식 키 입력 조합은 처리하지 않는다.
    """
    indexes = []
    for name, value, choices in (
        ('초성', chosung, CHO),
        ('중성', jungsung, JUNG),
        ('종성', jongsung, JONG),
    ):
        try:
            indexes.append(choices.index(value))
        except ValueError:
            raise ValueError(f'유효하지 않은 {name}: {value!r}') from None

    cho, jung, jong = indexes
    return chr(0xAC00 + (cho * 21 + jung) * 28 + jong)


def encode_euc_kr(text: str) -> bytes:
    """Python 내장 euc-kr 코덱으로 변환한다.

    지원하지 않는 문자는 위치 정보가 있는 UnicodeEncodeError를 낸다.
    일부 한글은 8바이트 조합 시퀀스로 출력되므로 2바이트를 보장하지 않는다.
    """
    return text.encode('euc-kr', errors='strict')


def main() -> None:
    text = (
        compose_hangul('ㄱ', 'ㅏ', 'ㄴ')
        + compose_hangul('ㅎ', 'ㅏ', 'ㄴ')
        + compose_hangul('ㄱ', 'ㅡ', 'ㄹ')
    )
    print('조합 결과:', text)
    print('HEX:')
    print(encode_euc_kr(text).hex(' ').upper())


if __name__ == '__main__':
    main()

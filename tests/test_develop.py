import contextlib
import importlib
import io
import unittest
import unicodedata
from collections import Counter

import develop


class HangulTests(unittest.TestCase):
    def test_known_syllables(self):
        self.assertEqual(develop.compose_hangul('ㄱ', 'ㅏ'), '가')
        self.assertEqual(develop.compose_hangul('ㄱ', 'ㅏ', 'ㄴ'), '간')
        self.assertEqual(develop.compose_hangul('ㅎ', 'ㅣ', 'ㅎ'), '힣')

    def test_all_modern_syllables_against_unicode_normalization(self):
        # 표의 순서와 공식을 함께 검사한다. NFD는 Python의 Unicode 데이터를 쓴다.
        for code in range(0xAC00, 0xD7A4):
            expected = chr(code)
            jamo = unicodedata.normalize('NFD', expected)
            cho = develop.CHO[ord(jamo[0]) - 0x1100]
            jung = develop.JUNG[ord(jamo[1]) - 0x1161]
            jong = develop.JONG[ord(jamo[2]) - 0x11A7] if len(jamo) == 3 else ''
            self.assertEqual(develop.compose_hangul(cho, jung, jong), expected)

    def test_invalid_jamo_identifies_position(self):
        for args, position in (
            (('ㅏ', 'ㅏ'), '초성'),
            (('ㄱ', 'ㄱ'), '중성'),
            (('ㄱ', 'ㅏ', 'ㄸ'), '종성'),
            (('\u1100', '\u1161'), '초성'),
        ):
            with self.subTest(args=args):
                with self.assertRaisesRegex(ValueError, position):
                    develop.compose_hangul(*args)


class EncodingTests(unittest.TestCase):
    def test_demo_bytes(self):
        self.assertEqual(develop.encode_euc_kr('간한글'), bytes.fromhex('B0 A3 C7 D1 B1 DB'))

    def test_ascii_and_empty(self):
        self.assertEqual(develop.encode_euc_kr(''), b'')
        self.assertEqual(develop.encode_euc_kr('ABC 123\n'), b'ABC 123\n')

    def test_jamo_hanja_and_symbols(self):
        self.assertEqual(
            develop.encode_euc_kr('ㄱ漢★€'),
            bytes.fromhex('A4 A1 F9 D3 A1 DA A2 E6'),
        )

    def test_eight_byte_sequences(self):
        self.assertEqual(
            develop.encode_euc_kr('똠힣'),
            bytes.fromhex('A4 D4 A4 A8 A4 C7 A4 B1 A4 D4 A4 BE A4 D3 A4 BE'),
        )

    def test_all_modern_syllables_round_trip_and_lengths(self):
        lengths = Counter()
        for code in range(0xAC00, 0xD7A4):
            char = chr(code)
            encoded = develop.encode_euc_kr(char)
            self.assertEqual(encoded.decode('euc-kr'), char)
            lengths[len(encoded)] += 1
        self.assertEqual(lengths, {2: 2350, 8: 8822})

    def test_unsupported_character_keeps_error_position(self):
        with self.assertRaises(UnicodeEncodeError) as caught:
            develop.encode_euc_kr('가\U0001f600나')
        self.assertEqual(caught.exception.start, 1)
        self.assertEqual(caught.exception.end, 2)

    def test_decomposed_jamo_is_not_automatically_normalized(self):
        with self.assertRaises(UnicodeEncodeError):
            develop.encode_euc_kr('\u1100\u1161')

    def test_import_is_silent(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            importlib.reload(develop)
        self.assertEqual(output.getvalue(), '')


if __name__ == '__main__':
    unittest.main()

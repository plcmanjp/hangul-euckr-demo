# hangul-euckr-demo

초성·중성·종성으로 한글 한 글자를 조합하고, Python 내장 `euc-kr` 코덱으로 바이트를 확인하는 학습용 예제입니다.

## 실행

Python 3.10 이상을 사용합니다. 외부 패키지는 필요하지 않습니다.
로컬 검증 환경은 Windows, CPython 3.13.15입니다.

```sh
python develop.py
```

```text
조합 결과: 간한글
HEX:
B0 A3 C7 D1 B1 DB
```

## 함수 사용

```python
from develop import compose_hangul, encode_euc_kr

print(compose_hangul('ㄱ', 'ㅏ'))        # 가
print(compose_hangul('ㄱ', 'ㅏ', 'ㄴ'))  # 간
print(encode_euc_kr('간').hex(' '))      # b0 a3
print(encode_euc_kr('ㄱ漢★').hex(' '))   # a4 a1 f9 d3 a1 da
```

`compose_hangul()`은 초성 19개, 중성 21개, 종성 28개(받침 없음 포함)의 순서를 이용합니다.

```text
코드 포인트 = 0xAC00 + (초성 인덱스 × 21 + 중성 인덱스) × 28 + 종성 인덱스
```

입력에는 `ㄱ`, `ㅏ` 같은 호환 자모를 사용합니다. 잘못된 위치의 자모는 `ValueError`를 냅니다.
문자열 전체의 자동 자모 조합, 두벌식 입력 처리, 옛한글 조합은 지원하지 않습니다.

`encode_euc_kr()`은 Python 코덱이 지원하는 한글·ASCII·한자·기호·자모를 변환합니다.
이모지 등 지원하지 않는 문자는 `UnicodeEncodeError`를 내며, 문자 위치는 예외의 `start`, `end` 속성에서 확인할 수 있습니다.
문자를 삭제하거나 `?`로 바꾸지 않습니다. 분해된 결합 자모 입력은 자동 정규화하지 않습니다.

## EUC-KR과 바이트 길이

Python에서 `euc-kr` 인코딩이 성공해도 한글 한 글자가 항상 2바이트인 것은 아닙니다.
내장 코덱은 일부 한글을 KS X 1001:1998의 8바이트 조합 시퀀스로 출력합니다.

| 입력 | 출력 HEX | 바이트 수 |
|---|---|---:|
| `가` | `B0 A1` | 2 |
| `똠` | `A4 D4 A4 A8 A4 C7 A4 B1` | 8 |
| `힣` | `A4 D4 A4 BE A4 D3 A4 BE` | 8 |

CPython 3.13.15에서 현대 한글 11,172자를 확인하면 2,350자는 2바이트, 8,822자는 8바이트로 변환됩니다.
이 동작은 [CPython EUC-KR 구현](https://github.com/python/cpython/blob/3.13/Modules/cjkcodecs/_codecs_kr.c)에서 확인할 수 있습니다.

대상 장비나 프로그램이 2바이트 완성형만 지원한다면 별도의 허용 문자 검증이 필요합니다.
CP949는 별도 인코딩이므로 대상 시스템의 명세를 확인해야 합니다.
이 예제에서는 Python 코덱의 동작을 그대로 사용하며, 외부 장비와의 호환성은 검증하지 않았습니다.

## 범위

입력은 Python `str`, 출력은 `bytes`입니다. 출력한 HEX는 바이트를 읽기 쉽게 표시한 문자열입니다.
파일 인코딩 감지, UTF-8/UTF-16 파일 읽기, 변환 파일 저장 기능은 포함하지 않습니다.

## 검증

```sh
python -m unittest discover -s tests -v
```

Unicode 정규화를 기준으로 현대 한글 11,172개의 조합을 검사하고, 알려진 바이트 값,
한자·기호·자모, 지원하지 않는 문자, 분해된 자모 입력, import 시 출력 여부를 확인합니다.

## 라이선스

[MIT License](LICENSE)

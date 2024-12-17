import json
from main import parse_config  # Импортируем функцию из main.py

def test():
    examples = [
        {
            "description": "Простые числовые и строковые константы",
            "input": """
                var number 42
                var greeting @"Hello, world!"
            """,
            "expected": {
                "constants": {
                    "number": 42,
                    "greeting": "Hello, world!"
                }
            }
        },
        {
            "description": "Массив с разными значениями",
            "input": """
                var array [1; @"two"; 3]
            """,
            "expected": {
                "constants": {
                    "array": [1, "two", 3]
                }
            }
        },
        {
            "description": "Постоянная ссылка",
            "input": """
                var base 10
                var multiplier $base$
            """,
            "expected": {
                "constants": {
                    "base": 10,
                    "multiplier": 10
                }
            }
        }
    ]

    for example in examples:
        try:
            result = parse_config(example["input"])
            assert result == example["expected"], f"Failed: {example['description']}\nExpected: {example['expected']}\nGot: {result}"
            print(f"Passed: {example['description']}")
        except Exception as e:
            print(f"Failed: {example['description']}\nError: {e}")

if __name__ == "__main__":
    test()

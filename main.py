import json
import sys
import re

def parse_config(input_text):
    constants = {}

    def parse_value(value):
        # Check if the value is a number
        if value.isdigit():
            return int(value)
        # Check if the value is a string in the format @"string"
        elif value.startswith('@"') and value.endswith('"'):
            return value[2:-1]  # Remove the surrounding @" and "
        # Check if the value is a constant reference in the format $constant$
        elif value.startswith('$') and value.endswith('$'):
            const_name = value[1:-1]
            if const_name in constants:
                return constants[const_name]
            else:
                raise ValueError(f"Неопределённая константа: {const_name}")
        # Check if the value is an array
        elif value.startswith('[') and value.endswith(']'):
            items = value[1:-1].split(';')
            return [parse_value(item.strip()) for item in items if item.strip()]
        else:
            raise ValueError(f"Недопустимое значение: {value}")

    def parse_line(line):
        # Use a more flexible regex to handle variable names with underscores
        match = re.match(r'var\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+(.+)', line)
        if match:
            name, value = match.groups()
            constants[name] = parse_value(value.strip())  # Process and store the value
        else:
            raise ValueError(f"Синтаксическая ошибка в строке: {line}")

    output = {}

    # Remove multi-line comments
    cleaned_text = re.sub(r'/#.*?#/', '', input_text, flags=re.DOTALL).strip()

    for line in cleaned_text.splitlines():
        line = line.strip()
        if not line:
            continue
        parse_line(line)  # Process each line

    output['constants'] = constants
    return output

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)

    try:
        input_file = sys.argv[1]
        # Read data from file
        with open(input_file, 'r') as file:
            input_text = file.read()

        # Process the configuration
        result = parse_config(input_text)

        # Output the result as JSON
        print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()



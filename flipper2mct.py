import argparse
import re

parser = argparse.ArgumentParser(description='[+] Process NFC dumps from Flipper Zero to MCT format')
parser.add_argument('source', help='Flipper Zero dump')
parser.add_argument('destination', help='MCT filename')
args = parser.parse_args()
pattern = r"(Block \d{1,2}: )(\w\w \w\w \w\w \w\w \w\w \w\w \w\w \w\w \w\w \w\w \w\w \w\w \w\w \w\w \w\w \w\w)"

try:
    sector_counter = 0
    i = 0
    source = open(args.source, 'r')
    destination = open(args.destination, 'w')
    for line in source:
        try:
            result = re.search(pattern, line)
            data = result.group(2).replace(' ', '')
            if not i % 4:
                destination.write(f"+Sector: {sector_counter}\n")
                sector_counter += 1
            destination.write(f"{data}\n")
            i = i + 1
        except:
            pass
except Exception as e:
    print(e)
finally:
    source.close()
    destination.close()
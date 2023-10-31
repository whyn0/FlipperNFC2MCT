import argparse
from pathlib import Path
import re

parser = argparse.ArgumentParser(description='[+] Process NFC dumps from Flipper Zero to MCT format')
parser.add_argument('source', help='MCT filename', type=Path)
parser.add_argument('destination', help='Flipper Zero dump', type=Path)
parser.add_argument('-s', '--uidsize', type=int, choices=[4, 7], required=True)
args = parser.parse_args()


uidsize = 4

inblocks = [line for line in args.source.read_text().strip().splitlines() if not line.startswith("+")]
block0 = bytes.fromhex(inblocks[0])
print(block0.hex(" ").upper())

if args.uidsize == 7:
    sak_offset = 7
    atqa_offset = 8
elif args.uidsize == 4:
    sak_offset = 5
    atqa_offset = 6

sak = block0[sak_offset] - 0x80
if sak > 0x80:
    print("Subtracting 0x80 from SAK")
    sak -= 0x80
print(f"{sak = }")

atqa = int.from_bytes(block0[atqa_offset:atqa_offset+2], "little")

with args.destination.open("w") as outfile:
    outfile.write(f"Filetype: Flipper NFC device\n")
    outfile.write(f"Version: 3\n")
    outfile.write(f"# Nfc device type can be UID, Mifare Ultralight, Mifare Classic, FeliCa or ISO15693\n")
    outfile.write(f"Device type: Mifare Classic\n")
    outfile.write(f"# UID is common for all formats\n")
    outfile.write(f"UID: {block0[:uidsize].hex(' ').upper()}\n")
    outfile.write(f"# ISO14443 specific fields\n")
    outfile.write(f"ATQA: {atqa.to_bytes(2, 'big').hex(' ').upper()}\n")
    outfile.write(f"SAK: {sak:02X}\n")
    outfile.write(f"# Mifare Classic specific data\n")
    outfile.write(f"Mifare Classic type: 1K\n")
    outfile.write(f"Data format version: 2\n")
    outfile.write(f"# Mifare Classic blocks, '??' means unknown data\n")
    for i, d in enumerate(inblocks):
        s = d.replace("-", "?")
        outfile.write(f"Block {i}: {' '.join(s[i:i+2] for i in range(0, len(s), 2))}\n")


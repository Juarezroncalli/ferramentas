import sys
import zlib
import re

with open('renata.pdf', 'rb') as f:
    content = f.read()

streams = re.findall(b'stream[\r\n]+(.*?)[\r\n]+endstream', content, re.DOTALL)
text = ''

for s in streams:
    try:
        decompressed = zlib.decompress(s)
        # Extract things inside () or [] for text operators like Tj or TJ
        pieces = re.findall(b'\((.*?)\)', decompressed)
        for p in pieces:
            # Handle basic encoding or just ignore errors
            text += p.decode('latin-1', 'replace') + '\n'
        
        # also sometimes text is stored in hex like <012A>
    except Exception:
        pass

with open('renata_raw_text.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print("Done")

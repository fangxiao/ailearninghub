#!/usr/bin/env python3
"""Fix the WeChat article by properly embedding images."""
import base64
import re

# Read images
with open('mermaid/05-pe-waveform.png', 'rb') as f:
    wave_b64 = base64.b64encode(f.read()).decode()

with open('mermaid/06-pe-addition.png', 'rb') as f:
    add_b64 = base64.b64encode(f.read()).decode()

# Read the public account version
with open('大模型原理系列-03-公众号版.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check if PLACEHOLDER is present
if 'PLACEHOLDER' in content:
    content = content.replace('PLACEHOLDER_PE_WAVE', wave_b64)
    content = content.replace('PLACEHOLDER_PE_ADD', add_b64)
    print("Replaced placeholders with actual base64 images")
else:
    # Images are truncated, need to fix
    print("Found truncated images, fixing...")
    
    # Find all img tags with base64
    pattern = r'<img src="data:image/png;base64,([^"]*)"([^>]*)>'
    matches = list(re.finditer(pattern, content, re.DOTALL))
    
    if len(matches) >= 2:
        # Replace first image
        content = content[:matches[0].start(1)] + wave_b64 + content[matches[0].end(1):]
        # Adjust position for second match
        offset = len(wave_b64) - len(matches[0].group(1))
        content = content[:matches[1].start(1) + offset] + add_b64 + content[matches[1].end(1) + offset:]
        print(f"Fixed {len(matches)} images")
    else:
        print(f"Warning: Found {len(matches)} images, expected 2")

# Write back
with open('大模型原理系列-03-公众号版.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Images fixed successfully!")
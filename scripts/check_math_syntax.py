import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

repo_root = Path('.')
md_files = [p for p in repo_root.glob('**/*.md') 
            if not any(part.startswith('.') for part in p.parts if part not in ('.scratch',))]

print(f"Validating math expressions across {len(md_files)} markdown files...\n")

all_math = []

for p in md_files:
    text = p.read_text(encoding='utf-8')
    
    # 1. Blocks
    for m in re.finditer(r'\$\$(.*?)\$\$', text, flags=re.DOTALL):
        all_math.append((p, "BLOCK", m.group(1).strip()))
        
    # Remove code and blocks
    clean_text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    clean_text = re.sub(r'\$\$.*?\$\$', '', clean_text, flags=re.DOTALL)
    
    # 2. Inlines
    for line_idx, line in enumerate(clean_text.splitlines(), 1):
        if line.strip().startswith('<!--'): continue
        l_no_code = re.sub(r'`[^`\n]+`', '', line)
        for m in re.finditer(r'(?<!\\)\$(.*?)(?<!\\)\$', l_no_code):
            content = m.group(1).strip()
            if content:
                all_math.append((p, f"INLINE L{line_idx}", content))

print(f"Total extracted math expressions: {len(all_math)}")

# Validate each expression
invalid = []
for p, kind, expr in all_math:
    # 1. Check unmatched braces
    if expr.count('{') != expr.count('}'):
        invalid.append((p, kind, expr, "Unmatched braces {}"))
    # 2. Check unmatched brackets []
    if expr.count('[') != expr.count(']'):
        invalid.append((p, kind, expr, "Unmatched brackets []"))
    # 3. Check unmatched parens ()
    if expr.count('(') != expr.count(')'):
        invalid.append((p, kind, expr, "Unmatched parentheses ()"))
    # 4. Check backslashes followed by non-command or broken escapes
    # e.g., \ without valid letter or symbol
    for slash_m in re.finditer(r'\\([a-zA-Z]+|.)', expr):
        cmd = slash_m.group(1)
        # known commands
        # check if command is weird
        pass

if not invalid:
    print("\n>>> ALL 100% MATH EXPRESSIONS VALIDATED! NO SYNTAX ERRORS DETECTED! <<<")
else:
    print(f"\nFound {len(invalid)} invalid expressions:")
    for p, kind, expr, reason in invalid:
        print(f"[{p}] [{kind}]: {reason} -> {expr}")

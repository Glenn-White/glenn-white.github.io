#!/usr/bin/env python3
"""DEAI v3.0 addendum battery rows (B-29..B-36) + manifest skeleton.
Usage: python3 deai_battery_v3.py <edited.tex> <original.tex>
Offline-safe: ADS/overlap checks that need external text report NOT-RUN."""
import re, sys, difflib, random
from collections import Counter

ed = open(sys.argv[1]).read()
og = open(sys.argv[2]).read()

def body(t):
    b = re.sub(r'(?m)^%.*', '', t)
    return b[b.find(r'\begin{document}'):]

def sentences(b):
    flat = re.sub(r'\s+', ' ', b)
    flat = re.sub(r'(et al|Fig|Figs|e\.g|i\.e|cf|Eq|Sect|approx|vs|No)\. ', r'\1<KEEP> ', flat)
    s = [x.strip().replace('<KEEP>', '.') for x in re.split(r'(?<=[.!?]) (?=[A-Z\\])', flat) if len(x) > 30]
    return s

be, bo = body(ed), body(og)
se, so = sentences(be), sentences(bo)

def norm(s):
    return re.sub(r'[^a-z0-9 ]', '', re.sub(r'\\[a-zA-Z]+\*?', '', s.lower())).strip()

# B-33 edit budget + B-29 new-text audit
changed = [s for s in se if not any(difflib.SequenceMatcher(None, norm(s), norm(o)).ratio() > 0.7 for o in so)]
frac = len(changed) / max(1, len(se))
print(f"| B-33 edit budget (sentences changed) | {frac:.2f} ({len(changed)}/{len(se)}) | <=0.40 | {'ok' if frac <= 0.40 else 'FIX'} |")

def rates(sents):
    n = max(1, sum(len(re.findall(r'[A-Za-z]+', s)) for s in sents))
    p = lambda c: c * 1000 / n
    return {'rather-than': p(sum(s.count('rather than') for s in sents)),
            'colons': p(sum(s.count(':') for s in sents)),
            'semis': p(sum(s.count(';') for s in sents)),
            'parens': p(sum(s.count('(') for s in sents)),
            'contrast-not': p(len(re.findall(r', not [a-z]', ' '.join(sents))) + sum(s.count('rather than') for s in sents))}
unchanged = [s for s in se if s not in changed]
rc, ru = rates(changed), rates(unchanged)
worse = {k: (ru[k], rc[k]) for k in rc if rc[k] > ru[k] + 0.5}
print(f"| B-29 new-text audit (worse rates: unchanged->changed) | {worse or 'none'} | no rate worse | {'ok' if not worse else 'FIX'} |")

# B-31 emphasis in body prose (exclude preamble/captions)
em = len(re.findall(r'\\(?:textbf|emph)\{', be))
W = len(re.findall(r'[A-Za-z]+', be))
print(f"| B-31 emphasis commands /1000 | {em*1000/W:.2f} | <=1 | {'ok' if em*1000/W <= 1 else 'FIX'} |")

# B-32 cross-references
xr = len(re.findall(r'(?:see|as discussed|cf\.|compare)?\s*(?:Section|Sect\.?|Fig\.?|Table|equation)\s*~?\\?ref', be))
print(f"| B-32 cross-references /1000 | {xr*1000/W:.2f} | <=3 | {'ok' if xr*1000/W <= 3 else 'FIX'} |")

# B-34 acronyms
acs = Counter(re.findall(r'\b(?:[A-Z]{2,6})\b', re.sub(r'\\[a-zA-Z]+\*?|[0-9]+', ' ', be)))
defs = {a: len(re.findall(r'\(' + a + r'\)', be)) for a in acs}
anom = {a: (d, acs[a]) for a, d in defs.items() if d > 1 or (d == 0 and acs[a] >= 3)}
undef = [a for a, d in defs.items() if d == 0 and acs[a] >= 3]
print(f"| B-34 acronym anomalies (undefined-used>=3x / defined-twice) | {undef} / {[a for a,d in defs.items() if d>1]} | 0/0 | {'ok' if not anom else 'REVIEW'} |")

# B-30 coined-term candidates: hyphenated or 2-word noun phrases >=3x, not standard
words = re.findall(r'[A-Za-z]+', be.lower())
gr2 = Counter(tuple(words[i:i+2]) for i in range(len(words)-1))
cands = [' '.join(k) for k, c in gr2.items() if c >= 6 and k[0] not in ('of','the','in','to','and','is','are','with','for','a','that','from','by','on','at','as','this','these','which','not','per','than','where','be','has','have','it')]
print(f"| B-30 coined-term candidates (frequent 2-grams; ADS check manual) | {len(cands)} | ADS-verify | REVIEW |")
for c in sorted(cands, key=lambda x: -gr2[tuple(x.split())])[:20]: print('   -', c, gr2[tuple(c.split())])

# B-35 overlap: NOT RUN offline (needs cited full texts)
print("| B-35 text overlap vs cited/own papers | NOT RUN (no full texts offline) | 0 | NOT-RUN |")
# B-36 segmentation spot-check stub
random.seed(0); sample = random.sample(se, min(20, len(se)))
bad = sum(1 for s in sample if re.search(r'(?:[a-z] [a-z]+ [A-Z]|[a-z]{2,}\.$)', s) and not re.search(r'\\|\. [A-Z][a-z]+ [a-z]', s))
print(f"| B-36 segmentation spot-check (20 sampled; eyeball in report) | {bad} suspicious | <=2/50 | REVIEW |")

# LX checks
com = [l for l in ed.split('\n') if l.strip().startswith('%') and re.search(r'(?i)claude|gpt|agent|model|todo|fixme|version [0-9]', l)]
print(f"| LX-01 comment hygiene (agent/TODO mentions) | {len(com)} | 0 | {'ok' if not com else 'FIX'} |")
labels = re.findall(r'\\label\{([^}]*)\}', ed)
dupl = [l for l, c in Counter(labels).items() if c > 1]
print(f"| LX duplicate labels | {dupl} | 0 | {'ok' if not dupl else 'FIX'} |")
refs = set(re.findall(r'\\(?:ref|eqref)\{([^}]*)\}', ed))
unused = [l for l in labels if l not in refs]
print(f"| LX unreferenced labels | {len(unused)} {unused[:5]} | inspect | REVIEW |")
# HS-01 percent sign in prose
pc = len(re.findall(r'(?<![$\\])\b\d+\s?%(?!\})', be))
print(f"| HS-01 '%' in running text | {pc} | 0 (use 'per cent') | {'ok' if pc == 0 else 'FIX'} |")
# LX-05 lists in Intro/Discussion/Conclusions
seg = re.split(r'\\section\{', be)
li = [s.split('}')[0] for s in seg if re.search(r'\\begin\{itemize\}|\\begin\{enumerate\}', s) and re.match(r'[^\}]*', s)]
print(f"| LX-05 lists inside sections | {li} | none in Intro/Disc/Concl | REVIEW |")

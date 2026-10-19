#!/usr/bin/env python3
"""DEAI protocol v2.0 Section 5.13 measured battery.
Canonical location: astra_core/deai/ (importable from any working directory).
Usage: python3 deai_battery.py <edited.tex> [original.tex]"""
import re, sys, statistics
from collections import Counter

fn = sys.argv[1]
t = open(fn).read()
body = re.sub(r'(?m)^%.*', '', t)
body = body[body.find(r'\begin{document}'):]
flat = re.sub(r'\s+', ' ', body)
words_all = re.findall(r'[A-Za-z]+', flat)
W = len(words_all)
sents = [s.strip() for s in re.split(r'(?<=[.!?]) ', flat) if len(s) > 30]
sl = [len(re.findall(r'[A-Za-z]+', s)) for s in sents]
per1000 = lambda c: round(c * 1000 / W, 2)
R = []
def row(name, val, thresh, verdict): R.append((name, val, thresh, verdict))

# B-01 em-dashes
row("B-01 em-dash rate /1000", per1000(flat.count('---')), "<=1", "FIX" if flat.count('---')*1000/W > 1 else "ok")
# B-02 excess lexicon
LEX = ["delve","underscore","showcase","leverage-verb","harness","foster","bolster","elucidate","unravel","unveil","streamline","facilitate","illuminate","unpack","pivotal","crucial","intricate","comprehensive","robust","nuanced","notable","noteworthy","invaluable","meticulous","multifaceted","seamless","compelling","unprecedented","profound","groundbreaking","transformative","holistic","paramount","tapestry","interplay","testament","synergy","paradigm","plethora","myriad"]
lexhits = sum(len(re.findall(r'\b'+w, flat, re.I)) for w in LEX)
row("B-02 excess-lexicon /1000", per1000(lexhits), "<=0.3", "FIX" if lexhits*1000/W > 0.3 else "ok")
# B-03 reaction adverbs
radv = ["remarkably","strikingly","intriguingly","surprisingly","interestly","importantly","notably","crucially","critically","clearly","fundamentally"]
rc = sum(flat.lower().count(w) for w in radv)
row("B-03 reaction adverbs /1000", per1000(rc), "<=1", "FIX" if rc*1000/W > 1 else "ok")
# B-04 agent vocab
AV = ["load-bearing","honestly","genuinely","cleanly","a sharp test","the crux","the real ","earns its place","lands,","at the heart of"]
av = sum(flat.lower().count(w) for w in AV)
row("B-04 agent vocab hits", av, "0", "FIX" if av else "ok")
# B-05 rather than
rt = len(re.findall(r'rather than', flat))
row("B-05 'rather than' /1000", per1000(rt), "<=2", "FIX" if rt*1000/W > 2 else "ok")
# B-06 reasoning connectives
con = ["therefore","thus,","hence","accordingly","consequently","So "]
cc = sum(len(re.findall(re.escape(c), flat)) for c in ["therefore","hence","accordingly","consequently"]) + len(re.findall(r'(?<=[.!?]) Thus', flat)) + len(re.findall(r'(?<=[.!?]) So,', flat))
row("B-06 reasoning connectives /1000", per1000(cc), "<=4", "FIX" if cc*1000/W > 4 else "ok")
# B-07 suspended-hyphen compounds
sh = re.findall(r'\b(\w+)- (?:and|or) (\w+-\w+|\w+ed)', flat)
sh2 = len(re.findall(r'(?<![\w-])\w+-\w+-\w+(?![\w-])', flat))
row("B-07 suspended-hyphen / stacked compounds", len(sh)+sh2, "<=3 inspect", "INSP")
# B-08 anaphora profile
tn = len(re.findall(r'(?<=[.!?]) (This|These) [a-z]+', flat))
row("B-08 This/These+noun openers /1000", per1000(tn), "<=8", "FIX" if tn*1000/W > 8 else "ok")
# B-09 reporting verbs
rv = Counter(re.findall(r'\b(gives|yields|shows|hold[s]?|carries|reaches|returns)\b', flat.lower()))
share = max(rv.values())/max(1,sum(rv.values()))
row("B-09 reporting-verb top share", f"{share:.2f}", "<0.40", "FIX" if share > 0.4 else "ok")
# B-10 sentence-initial distribution
first = Counter(s.split()[0].lower() for s in sents)
top = first.most_common(1)[0]
top3 = sum(c for _, c in first.most_common(3))
row("B-10 top opener share / top-3", f"{top[0]} {top[1]/len(sents):.2f} / {top3/len(sents):.2f}", "<0.35 / <0.55",
    "FIX" if top[1]/len(sents) >= 0.35 or top3/len(sents) >= 0.55 else "ok")
# B-11 length CV
cv = statistics.stdev(sl)/statistics.mean(sl)
row("B-11 sentence-length CV", f"{cv:.2f}", ">=0.40", "FIX" if cv < 0.40 else "ok")
# B-12 mean length
row("B-12 mean sentence length", f"{statistics.mean(sl):.1f}", "<=40", "FIX" if statistics.mean(sl) > 40 else "ok")
# B-13 contrastive reframes
p01 = len(re.findall(r', not [a-z]| rather than', flat))
row("B-13 'not X' contrasts + rather-than", p01, "inspect", "INSP")
# B-14 pseudo-clefts / rhetorical questions
pc = len(re.findall(r'\bWhat [a-z]+ [a-z]+ is\b|\. Is [A-Z]| \? ', flat))
row("B-14 pseudo-clefts + questions (body)", pc, "0-ish", "INSP")
# B-15 trailing -ing clauses
tg = len(re.findall(r', (highlighting|underscoring|suggesting|indicating|demonstrating|emphasising|reflecting|revealing|providing|pointing)', flat))
row("B-15 trailing commentary clauses", tg, "<=2", "FIX" if tg > 2 else "ok")
# B-16 triads
tri = len(re.findall(r'\b\w+(?: \w+)?, \w+(?: \w+)?, and \w+', flat))
row("B-16 triadic lists", tri, "inspect", "INSP")
# B-17 noun premodality
pm = len([w for w in re.findall(r'(?:\w+-){2,}\w+', flat) if not re.search(r'per-cent|-to-|-of-|one-to-one|out-of|line-of|leave-one|signal-to|point-to', w)])
row("B-17 4+-word modifier stacks", pm, "<=3", "FIX" if pm > 3 else "ok")
# B-18 paragraph CV (approx: blank-line separated)
paras = [p for p in re.split(r'\n\s*\n|\\par\b', body) if len(p) > 100]
pl = [len(re.findall(r'[A-Za-z]+', p)) for p in paras]
pcv = statistics.stdev(pl)/statistics.mean(pl) if len(pl) > 3 else 0
row("B-18 paragraph-length CV", f"{pcv:.2f}", ">=0.35", "FIX" if pcv < 0.35 else "ok")
# B-19 paragraph-opener uniformity
_paras = [re.sub(r'\s+', ' ', p).strip() for p in re.split(r'\n\s*\n', body)
          if len(p) > 150 and not re.search(r'\\begin\{(table|figure|equation)\}|\\caption|\\label', p)]
pf = Counter(p.split()[0] for p in _paras)
ptop = pf.most_common(1)[0] if pf else ('?', 0)
row("B-18b para top-opener share", f"{ptop[0]} {ptop[1]/max(1,len(_paras)):.2f} ({len(_paras)})", "<0.35",
    "FIX" if ptop[1]/max(1,len(_paras)) >= 0.35 else "ok")
# B-20 caption uniformity (brace-matched so nested braces are visible)
def _caps(b):
    out = []
    for m in re.finditer(r'\\caption\{', b):
        d = 1; i = m.end()
        while d and i < len(b):
            if b[i] == '{': d += 1
            elif b[i] == '}': d -= 1
            i += 1
        out.append(re.sub(r'\s+', ' ', b[m.end():i-1]))
    return out
caps = _caps(body)
cf = Counter(((re.sub(r'\\[a-zA-Z]+\*?', '', c).strip().split() or ['?'])[0]) for c in caps)
ctop = cf.most_common(1)[0] if cf else ('?', 0)
row("B-20 captions / top first-word share", f"{len(caps)} / {ctop[0]} {ctop[1]/max(1,len(caps)):.2f}", "<0.45",
    "FIX" if ctop[1]/max(1,len(caps)) >= 0.45 else "ok")
# B-21a p-values /1000
pv = len(re.findall(r'\$p[=<]|\$?p\s*=|p=|Fisher|Kolmogorov|Mann', flat))
row("B-21a p-value/test mentions /1000", per1000(pv), "<=2.5", "FIX" if pv*1000/W > 2.5 else "ok")
# B-22 hedge census
H = ["not established","not a test","not tests","conditional on","phenomenological","cannot decide","cannot distinguish","does not determine","no significant","consistent with","caveat","not quantified","neither for nor against","either way","no evidence","suggestive of"]
hc = sum(len(re.findall(re.escape(h), flat)) for h in H)
row("B-22 hedge total /1000", per1000(hc), "<=2 inspect-decomp", "INSP")
# B-23 near-duplicate sentences
def sig(s): return set(w.lower() for w in re.findall(r'[a-z]{5,}', s))
dups = 0
for i in range(len(sents)):
    for j in range(i+1, len(sents)):
        a, b = sig(sents[i]), sig(sents[j])
        if a and b and len(a & b)/min(len(a), len(b)) >= 0.75 and abs(len(a)-len(b)) <= 3:
            dups += 1
row("B-23 near-duplicate sentence pairs", dups, "0", "INSP")
# B-24 repeated 6-grams
gr = Counter(tuple(words_all[i:i+6]) for i in range(len(words_all)-5))
r6 = sum(1 for g, c in gr.items() if c >= 3)
row("B-24 repeated 6-grams (>=3x)", r6, "0", "INSP")
# B-26 punctuation deltas (vs original if given as argv[2]; otherwise absolute)
if len(sys.argv) > 2:
    obody = re.sub(r'(?m)^%.*', '', open(sys.argv[2]).read())
    obody = obody[obody.find(r'\begin{document}'):]
    oflat = re.sub(r'\s+', ' ', obody)
    oW = len(re.findall(r'[A-Za-z]+', oflat))
    dl = [round(flat.count(c)*1000/W - oflat.count(c)*1000/oW, 2) for c in ':;(']
    row("B-26 colon/semicolon/paren DELTA vs orig /1000", f"{dl[0]}/{dl[1]}/{dl[2]}", "each <=3",
        "FIX" if max(abs(d) for d in dl) > 3 else "ok")
else:
    row("B-26 colons/semicolons/parens per 1000", f"{per1000(flat.count(':'))}/{per1000(flat.count(';'))}/{per1000(flat.count('('))}", "delta<=3 vs orig", "INSP")

print(f"| Metric | Value | Threshold | Verdict |\n|---|---|---|---|")
for name, val, th, v in R:
    print(f"| {name} | {val} | {th} | {v} |")
print(f"\n(words {W}, sentences {len(sents)}, paragraphs {len(pl)})")

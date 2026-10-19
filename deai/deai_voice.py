#!/usr/bin/env python3
"""deai_voice.py — author-voice profiler and scorer (DEAI v3.0 Class B voice rows).

Usage:
  build:  python3 deai_voice.py build <corpus_dir> <profile.json>
          corpus_dir holds *.txt (pdftotext output of the author's papers)
  score:  python3 deai_voice.py score <profile.json> <file.txt|file.tex> [file2 ...]
          prints per-file voice distance D (0=identical to profile, larger=farther)
          plus the five worst feature z-offsets.
  validate: python3 deai_voice.py validate <corpus_dir> <profile.json> <ctrl_dir>
          leave-out check: held-out author papers must score closer than controls.

Method: stylometric feature vector (function words, punctuation, sentence
length distribution, openers, hedges, passive/active mix) z-scored against
the corpus, scored by mean |z| (Manhattan/L1 in z-space, like a Burrows'
Delta with an extended feature set). Pure Python + (optional) numpy.
"""
import json, math, os, re, sys
from collections import Counter

FUNC_WORDS = """the of and to in a is that for as with by on are be from or this
which we it an not at these their has have was were but can may our its all such
than then when where while also both each more most only some there they thus
under within without through between during after before above below over
however therefore moreover furthermore hence thus consequently indeed rather
although though because since until unless whereas while
one two three four five six seven eight nine ten
do does did done has had having its it's they them their
very quite rather somewhat more less least most
about across against along among around despite except into near off out per
till toward upon via whether""".split()

HEDGES = """may might could would should appears suggests seems likely unlikely
possibly probably perhaps approximately roughly consistent compatible
candidate tentative indicative suggestive presume presume presumably suspect
arguably conceivably plausibly""".split()

REPORTING = """show shows shown demonstrate demonstrates demonstrated reveal
reveals revealed find found finds observe observes observed detect detects
detected measure measures measured derive derives derived estimate estimates
estimate obtain obtained report reports reported""".split()

PASSIVE = re.compile(r'\b(?:is|are|was|were|be|been|being)\s+(\w+(?:ed|en))\b', re.I)

# --- Topic-robust feature whitelist -------------------------------------
# Style features whose rate does not track subject matter. Prepositions,
# numerals and pronoun rates are EXCLUDED: their usage varies with the
# science being described (plot idioms, sample sizes), not with the hand.
RHYTHM = ('Smean', 'Ssd', 'Sshort', 'Slong')
PUNCT = ('P:comma', 'P:semi', 'P:colon')
CONNECT = tuple('fw:' + w for w in (
    'however therefore moreover furthermore hence thus consequently indeed '
    'although though because whereas while also very quite').split())
OPENERS = ('O:the', 'O:we', 'O:in', 'O:this', 'O:these', 'O:however')
CORE = ('Zwe', 'Zpassive', 'Zreport') + tuple('hd:' + h for h in HEDGES)
ROBUST_KEYS = set(RHYTHM + PUNCT + CONNECT + OPENERS + CORE)

# --- LLM-tell features (diagnostic, independent of author profile) ------
LLM_TELLS = (
    'rather than', 'not only', 'it is worth noting', 'notably',
    'crucially', 'importantly', 'delve', 'delves', 'comprehensive',
    'seamless', 'highlights', 'underscores', 'showcases', 'landscape',
    'a range of', 'in summary', 'overall', 'furthermore', 'moreover',
)

def sentences(text):
    flat = re.sub(r'\s+', ' ', text)
    flat = re.sub(r'\b(?:et al|Fig|Figs|e\.g|i\.e|cf|Eq|Eqs|Sect|approx|vs|No)\. ', lambda m: m.group(0).replace('.', '\x00'), flat)
    s = [x.strip().replace('\x00', '.') for x in re.split(r'(?<=[.!?]) (?=[A-Z(])', flat)]
    return [x for x in s if len(x) > 30]

def clean_corpus_text(raw):
    """Strip page furniture, references, tables, acknowledgements from a
    pdftotext dump; keep body prose only."""
    t = raw
    for cut in (r'(?is)^.*?abstract', ):
        pass
    # drop everything from References onward (first occurrence mid-doc)
    m = re.search(r'(?m)^(R E F E R E N C E S|References|REFERENCES)\s*$', t)
    if m and m.start() > len(t) * 0.35:
        t = t[:m.start()]
    for pat in (r'(?is)^Acknowledgements.*?(\n\n\n|\Z)', r'(?is)^Acknowledgments.*?(\n\n\n|\Z)'):
        t = re.sub(pat, '\n', t)
    t = re.sub(r'(?m)^(Downloaded|Received|Accepted|Published|https?://\S+|.*\bdoi:\b.*)$', ' ', t)
    t = re.sub(r'\s+', ' ', t)
    return t

def words(t):
    return re.findall(r"[A-Za-z']+", t.lower())

def features(text):
    """Feature dict: rates per 1000 words + distributional stats."""
    w = words(text)
    n = len(w)
    f = {}
    if n < 400:
        return None
    c = Counter(w)
    for fw in FUNC_WORDS:
        f['fw:' + fw] = c[fw] * 1000 / n
    for h in HEDGES:
        f['hd:' + h] = c[h] * 1000 / n
    f['Zreport'] = sum(c[r] for r in REPORTING) * 1000 / n
    f['Zpassive'] = len(PASSIVE.findall(text)) * 1000 / n
    f['Zwe'] = c['we'] * 1000 / n
    f['Zwe_restricted'] = (len(re.findall(r'\bwe\b', text.lower()))) * 1000 / n
    s = sentences(text)
    if len(s) < 15:
        return None
    sl = [len(re.findall(r'[A-Za-z]+', x)) for x in s]
    mean = sum(sl) / len(sl)
    sd = (sum((x - mean) ** 2 for x in sl) / len(sl)) ** 0.5
    f['Smean'], f['Ssd'] = mean, sd
    f['Sshort'] = sum(1 for x in sl if x <= 12) * 1000 / len(sl)
    f['Slong'] = sum(1 for x in sl if x >= 40) * 1000 / len(sl)
    for ch, tag in ((',', 'comma'), (';', 'semi'), (':', 'colon'),
                    ('(', 'paren'), (')', 'paren2'), ('-', 'dash')):
        f['P:' + tag] = text.count(ch) * 1000 / n
    openers = Counter()
    for x in s:
        m0 = re.match(r'([A-Za-z]+)', x.strip())
        if m0:
            openers[m0.group(1).lower()] += 1
    for o in ('the', 'we', 'in', 'this', 'these', 'however', 'figure', 'table', 'fig'):
        f['O:' + o] = openers[o] * 1000 / len(s)
    f['Nsent'] = len(s)
    return f

def build(corpus_dir, out):
    rows, kept = [], []
    for fn in sorted(os.listdir(corpus_dir)):
        if not fn.endswith('.txt'):
            continue
        raw = open(os.path.join(corpus_dir, fn), errors='ignore').read()
        f = features(clean_corpus_text(raw))
        if f:
            rows.append(f); kept.append(fn)
    keys = [k for k in rows[0] if not k.startswith('N')]
    prof = {'n_docs': len(rows), 'docs': kept, 'features': {}}
    min_docs = max(2, len(rows) // 3)
    for k in keys:
        v = [r[k] for r in rows if k in r and r[k] > 0]
        if len(v) < min_docs:
            continue  # feature too rare to be a stable profile signal
        m = sum(v) / len(v)
        sd = (sum((x - m) ** 2 for x in v) / len(v)) ** 0.5
        sd = max(sd, m * 0.15, 0.05)  # floor: no z-explosion on quiet features
        prof['features'][k] = [m, sd]
    json.dump(prof, open(out, 'w'), indent=1)
    print('profile: %d docs, %d features -> %s' % (len(rows), len(keys), out))

def score(prof, text, robust=False):
    f = features(text)
    if f is None:
        return None
    tot, cnt, offs = 0.0, 0, []
    for k, (m, sd) in prof['features'].items():
        if k not in f:
            continue
        if robust and k not in ROBUST_KEYS:
            continue
        z = abs(f[k] - m) / sd
        tot += z; cnt += 1
        offs.append((z, k, f[k], m))
    offs.sort(reverse=True)
    return tot / cnt, offs[:6]

def llm_tells(text):
    """Rate per 1000 words of known LLM-flavoured expressions."""
    w = words(text)
    n = len(w)
    t = text.lower()
    out = {}
    for p in LLM_TELLS:
        c = t.count(p)
        if c:
            out[p] = (c, c * 1000 / n)
    # "X, Y, and Z" triadic lists per 1000 sentences
    s = sentences(text)
    tri = sum(len(re.findall(r'[^,;:]+,[^,;:]+,[^,;:]+ and ', x)) for x in s)
    out['TRIADS (a, b, and c)'] = (tri, tri * 1000 / max(1, len(s)))
    return out

def preprocess_tex(path):
    """§T-3 honest-scoring preprocessor: recursively inline \\input files,
    strip comments and table/figure/math/bibliography environments, strip
    macros. Raw .tex scoring without this is INVALID (tables inflate Dr)."""
    def rec(p, depth=0):
        if depth > 8:
            return ''
        t = open(p, errors='ignore').read()
        base = os.path.dirname(os.path.abspath(p))
        def sub(m):
            f = os.path.join(base, m.group(2) + '.tex')
            return rec(f, depth + 1) if os.path.exists(f) else ''
        return re.sub(r'(?m)^([^%\n]*?)\\input\{([^}]+)\}', sub, t)
    t = rec(path)
    t = re.sub(r'(?m)(?<!\\)%.*', '', t)
    for env in ('deluxetable', 'deluxetable*', 'tabular', 'tabular*', 'table',
                'table*', 'figure', 'figure*', 'align', 'align*', 'equation',
                'equation*', 'eqnarray', 'math', 'displaymath', 'verbatim',
                'thebibliography'):
        t = re.sub(r'(?is)\\begin\{' + re.escape(env) + r'\}.*?\\end\{' + re.escape(env) + r'\}', ' ', t)
    t = re.sub(r'\\[a-zA-Z]+\*?(\[[^\]]*\])?', ' ', t)
    t = re.sub(r'[{}$&~^_]', ' ', t)
    return re.sub(r'\s+', ' ', t)

def main():
    mode = sys.argv[1]
    if mode == 'texscore':
        # texscore <profile.json> <paper.tex> [--robust] [--tells]
        prof = json.load(open(sys.argv[2]))
        robust = '--robust' in sys.argv
        for path in [p for p in sys.argv[3:] if not p.startswith('--')]:
            raw = preprocess_tex(path)
            r = score(prof, raw, robust=robust)
            if r is None:
                print('%s\tTOO-SHORT' % path)
                continue
            d, offs = r
            print('%s\tD%s=%.3f' % (path, 'r' if robust else '', d))
            for z, k, v, m in offs:
                print('   %-12s z=%.2f  (val %.2f vs profile %.2f)' % (k, z, v, m))
            if '--tells' in sys.argv:
                for k, (c, rt) in sorted(llm_tells(raw).items(), key=lambda x: -x[1][1]):
                    print('   TELL %-24s %3d  (%.2f/1000)' % (k, c, rt))
    elif mode == 'build':
        build(sys.argv[2], sys.argv[3])
    elif mode == 'score':
        prof = json.load(open(sys.argv[2]))
        robust = '--robust' in sys.argv
        paths = [p for p in sys.argv[3:] if not p.startswith('--')]
        for path in paths:
            raw = open(path, errors='ignore').read()
            if path.endswith('.tex'):
                raw = re.sub(r'(?m)^%.*', '', raw)
                raw = re.sub(r'\\[a-zA-Z]+\*?(\[[^\]]*\])?', ' ', raw)
                raw = re.sub(r'[{}$&~^_]', ' ', raw)
            r = score(prof, raw, robust=robust)
            if r is None:
                print('%s\tTOO-SHORT' % path)
            else:
                d, offs = r
                print('%s\tD%s=%.3f' % (path, 'r' if robust else '', d))
                for z, k, v, m in offs:
                    print('   %-12s z=%.2f  (val %.2f vs profile %.2f)' % (k, z, v, m))
            if '--tells' in sys.argv:
                for k, (c, r) in sorted(llm_tells(raw).items(), key=lambda x: -x[1][1]):
                    print('   TELL %-24s %3d  (%.2f/1000)' % (k, c, r))
    elif mode == 'validate':
        corpus_dir, prof_path, ctrl_dir = sys.argv[2:5]
        robust = '--robust' in sys.argv
        prof = json.load(open(prof_path))
        hold = set(prof['docs'])
        ours = []
        for fn in sorted(os.listdir(corpus_dir)):
            if fn.endswith('.txt') and fn not in hold:
                r = score(prof, clean_corpus_text(open(os.path.join(corpus_dir, fn), errors='ignore').read()), robust=robust)
                if r: ours.append((r[0], fn))
        ctrl = []
        for fn in sorted(os.listdir(ctrl_dir)):
            if fn.endswith('.txt'):
                r = score(prof, clean_corpus_text(open(os.path.join(ctrl_dir, fn), errors='ignore').read()), robust=robust)
                if r: ctrl.append((r[0], fn))
        print('held-out author papers:')
        for d, fn in sorted(ours): print('  %.3f  %s' % (d, fn))
        print('control (other-author) papers:')
        for d, fn in sorted(ctrl): print('  %.3f  %s' % (d, fn))
        if ours and ctrl:
            sep = min(d for d, _ in ctrl) - max(d for d, _ in ours)
            print('separation (min control - max ours) = %.3f  %s' % (sep, 'OK' if sep > 0 else 'OVERLAP — do not trust gate'))

if __name__ == '__main__':
    main()

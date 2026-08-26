---
name: latex-paper
description: Compile and edit the MOD journal paper in paper-tex/. Use when writing, fixing or building the LaTeX paper, or when a LaTeX error or warning needs diagnosing.
---

# MOD paper (elsarticle)

Source lives in `paper-tex/`, which is gitignored: Overleaf is the working
copy, this repo holds the research it is written from. Figures are generated
by `experiments/paper_figures.py` and copied into `paper-tex/figures/`.

## Compile

    cd paper-tex && tectonic -X compile mod-paper.tex --keep-logs

Read `mod-paper.log` afterwards. Do not report the paper as building until
these are all zero or explained:

    grep -c "LaTeX Warning" mod-paper.log
    grep -cE "undefined" mod-paper.log
    grep -E "Overfull \\hbox" mod-paper.log

Overfull boxes under about 3\,pt are under a millimetre and not worth
chasing. Anything over 10\,pt is visible in print.

## What has already bitten this document

**`review` double-spaces everything, including floats.** A five-row table
overflowed a whole page ("Float too large for page by 202pt"). Floats are set
single-spaced with `\AtBeginEnvironment{table}{\setstretch{1}}`. Keep it: the
journal wants the body double-spaced, not the tables.

**Computer Modern is bitmapped.** Every sub- and superscript produced a "Font
shape ... in size <0.7> not available" warning. `lmodern` plus `T1` fontenc
fixes all of them.

**Wide tables need `tabularx`, not `tabular`.** Table 1 ran off the page.
Columns carrying prose want `>{\raggedright\arraybackslash}X`; justified `X`
columns generate a swarm of under- and overfull boxes.

**`\citet` expands to the full author name.** "Japan International
Cooperation Agency (2012)" does not fit an `l` column. Give citation columns
a wrapping `X`.

**Long `\texttt{}` runs cannot break.** An inline OSM tag string overflowed by
44\,pt. Split into separate `\texttt{}` units, or write it as prose, which
usually reads better anyway.

## Bibliography

`references.bib`, style `elsarticle-harv` (author-year; transport journals
expect this, not numeric).

**Never invent page numbers, DOIs or volumes to silence a BibTeX warning.**
Four entries currently warn "empty pages"; they are conference papers whose
ranges have not been verified. The warning is harmless. Inventing the range
is a fabricated citation, which `AI-GUARDRAILS.md` document rule 7 forbids and
which a reviewer can check.

Every key must resolve. Check before claiming the bibliography is complete:

    python3 - <<'PY'
    import re
    tex = open("mod-paper.tex").read()
    keys = set(re.findall(r"@\w+\{([^,]+),", open("references.bib").read()))
    cited = {c.strip() for m in re.findall(r"\\cite[pt]?\{([^}]+)\}", tex)
             for c in m.split(",")}
    print("missing from bib:", sorted(cited - keys) or "none")
    print("uncited entries:", sorted(keys - cited) or "none")
    PY

## Pending markers

Unfinished values are wrapped in `\pending{...}`, which prints in red so the
paper cannot be submitted past them. Count them before calling the paper
done:

    grep -c "\\\\pending{" mod-paper.tex

Delete the macro definition once the last one is gone.

## Figures

Regenerate rather than editing PDFs:

    uv run python -m experiments.paper_figures
    scp "dell-server:/opt/subash/mod/results/figures/paper/*.pdf" paper-tex/figures/

Greyscale with distinct markers and dash patterns, because these are printed
in black and white. Vector PDF, not PNG.

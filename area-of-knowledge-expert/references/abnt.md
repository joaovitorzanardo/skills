# ABNT citations (NBR 6023:2018 and NBR 10520:2023)

Every reference in this skill uses ABNT. It is written in English (the field labels below are the English equivalents of the Portuguese ones), but the punctuation and order follow the standard. Write **bold** with markdown `**…**`; `build_map.py` turns it into `<b>` on the page.

## Reference list entries (the `Citation:` line in RESOURCES.md)

**Authors.** `SURNAME, Initials.` in capitals. Separate up to three authors with `;`. With four or more, write the first one followed by `et al.`. An organization as author is written in full, in capitals (`MASSACHUSETTS INSTITUTE OF TECHNOLOGY.`).

**What is bold.** The title of the thing you would find on a shelf: the book title, the journal name, the proceedings title, the course or site name. A subtitle comes after `**Title**:` and is not bold. Only the first word and proper nouns are capitalized in titles.

| Type | Pattern | Example |
|---|---|---|
| Book | `SURNAME, I. **Title**: subtitle. N. ed. City: Publisher, Year.` | `CORMEN, T. H. et al. **Introduction to algorithms**. 4. ed. Cambridge: MIT Press, 2022.` |
| Book chapter | `SURNAME, I. Chapter title. In: EDITOR, I. (ed.). **Book title**. City: Publisher, Year. p. x-y.` | `LAMPORT, L. Time, clocks, and the ordering of events. In: MALKHI, D. (ed.). **Concurrency**. New York: ACM, 2019. p. 179-196.` |
| Journal paper | `SURNAME, I. Article title. **Journal**, v. X, n. Y, p. x-y, Year.` | `TURING, A. M. On computable numbers, with an application to the Entscheidungsproblem. **Proceedings of the London Mathematical Society**, v. s2-42, n. 1, p. 230-265, 1937.` |
| Conference paper | `SURNAME, I. Title. In: CONFERENCE NAME, N., Year, City. **Proceedings** [...]. City: Publisher, Year. p. x-y.` | `VASWANI, A. et al. Attention is all you need. In: ADVANCES IN NEURAL INFORMATION PROCESSING SYSTEMS, 30., 2017, Long Beach. **Proceedings** [...]. Red Hook: Curran Associates, 2017. p. 5998-6008.` |
| Preprint | `SURNAME, I. Title. **arXiv**, Year. Preprint arXiv:NNNN.NNNNN.` | `KAPLAN, J. et al. Scaling laws for neural language models. **arXiv**, 2020. Preprint arXiv:2001.08361.` |
| Course | `INSTITUTION. **Course code and title**. City: Platform, Year.` | `MASSACHUSETTS INSTITUTE OF TECHNOLOGY. **6.006 Introduction to algorithms**. Cambridge: MIT OpenCourseWare, 2020.` |
| Online article, docs, blog | `SURNAME, I. **Title**. Site or publisher, Year.` | `OLAH, C. **Understanding LSTM networks**. colah's blog, 2015.` |
| Video or lecture series | `SURNAME, I. **Title**. Channel or publisher, Year. 1 video (N min).` | `SANDERSON, G. **But what is a neural network?** 3Blue1Brown, 2017. 1 video (19 min).` |

Leave out what you cannot find (an edition, a city) rather than guessing it. Do not put the URL or DOI in the citation text: it goes in the separate `URL:` field, which the page turns into an OPEN ↗ link.

## In-text citations (OVERVIEW.md)

`(SURNAME, Year)` with the surname in capitals. Two or three authors: `(SURNAME; SURNAME, Year)`. Four or more: `(SURNAME et al., Year)`. Organizations: the name in capitals, `(MASSACHUSETTS INSTITUTE OF TECHNOLOGY, 2020)`.

In OVERVIEW.md every in-text citation is a markdown link to the resource id, so the page can jump to the reference:

```markdown
…as dynamic programming [(CORMEN et al., 2022)](#ref-cormen2022).
```

## Resource ids

The id is the first author's surname plus the year, lowercase ASCII with no accents or spaces: `cormen2022`, `vaswani2017`, `goedel1931`. For organizations use a short recognizable name: `mit6006`, `w3c2023`. If the same id would appear twice for different works, add `b`, `c`… (`knuth1997`, `knuth1997b`).

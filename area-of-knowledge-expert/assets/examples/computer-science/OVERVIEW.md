## Computer Science

Computer Science studies computation itself: what can be computed, how efficiently, and how to build reliable systems that do it. Its foundations were laid when [(TURING, 1937)](#ref-turing1937) formalized the idea of a mechanical procedure, years before the first electronic computers existed.

The field is usually split into a theoretical core, a systems layer that makes computation physical, and applied branches that put it to work. The six sub-fields below cover that spread: **Theory of Computation** and **Algorithms & Data Structures** form the core, **Computer Systems** and **Programming Languages** make it run, and **Artificial Intelligence** and **Software Engineering** apply it.

## Sub-fields

### Theory of Computation

Theory of Computation asks what problems machines can solve at all, and at what cost. Automata and formal languages classify machines by their power, computability draws the line between solvable and unsolvable problems, and complexity theory sorts the solvable ones by the resources they need [(SIPSER, 2013)](#ref-sipser2013).

Its landmark results are negative ones: Turing's proof that no program can decide whether every other program halts [(TURING, 1937)](#ref-turing1937), and the still-open question of whether P equals NP. A newcomer usually starts with finite automata and works up to Turing machines.

**Connects to:** Algorithms & Data Structures; Programming Languages; Artificial Intelligence

### Algorithms & Data Structures

This sub-field studies step-by-step procedures and the structures that hold their data, with running time and memory as the measure of quality. The standard reference organizes it around design paradigms such as divide-and-conquer, greedy choice and dynamic programming [(CORMEN et al., 2022)](#ref-cormen2022).

It is the most practical face of theory: every other sub-field relies on its sorting, searching and graph algorithms. A good first step is a full introductory course, such as MIT's [(MASSACHUSETTS INSTITUTE OF TECHNOLOGY, 2020)](#ref-mit6006).

**Connects to:** Theory of Computation; Artificial Intelligence

### Computer Systems

Computer Systems covers the layers that turn logic into running machines: processors and memory [(PATTERSON; HENNESSY, 2014)](#ref-patterson2014), the operating system that shares them among programs [(TANENBAUM; BOS, 2015)](#ref-tanenbaum2015), and the networks that connect machines into distributed systems.

Its central theme is managing limited resources safely while many things happen at once, which is why concurrency appears at every layer.

**Connects to:** Programming Languages; Software Engineering

### Programming Languages

Programming Languages designs the notations we program in and proves what they mean. Type systems catch whole classes of errors before a program runs [(PIERCE, 2002)](#ref-pierce2002), and compilers translate high-level code into efficient machine instructions [(AHO et al., 2006)](#ref-aho2006).

The sub-field borrows heavily from logic and the lambda calculus, and its ideas reach working programmers through every new language feature.

**Connects to:** Theory of Computation; Computer Systems; Software Engineering

### Artificial Intelligence

Artificial Intelligence builds systems that perceive, reason and learn. Its classical core is search, planning and logic [(RUSSELL; NORVIG, 2020)](#ref-russell2020); its modern progress is driven by models learned from data, such as the Transformer architecture behind today's language models [(VASWANI et al., 2017)](#ref-vaswani2017).

It is the most fast-moving sub-field here, so its best resources mix textbooks with recent papers.

**Connects to:** Theory of Computation; Algorithms & Data Structures

### Software Engineering

Software Engineering turns programming into an engineering discipline: how teams specify, structure, test and evolve large systems over many years [(SOMMERVILLE, 2016)](#ref-sommerville2016). Reusable solutions to recurring design problems were catalogued early as design patterns [(GAMMA et al., 1994)](#ref-gamma1994).

**Connects to:** Computer Systems; Programming Languages

## Resources

### Theory of Computation

- SIPSER, M. **Introduction to the theory of computation**. 3. ed. Boston: Cengage Learning, 2013.
- TURING, A. M. On computable numbers, with an application to the Entscheidungsproblem. **Proceedings of the London Mathematical Society**, v. s2-42, n. 1, p. 230-265, 1937.

### Algorithms & Data Structures

- CORMEN, T. H. et al. **Introduction to algorithms**. 4. ed. Cambridge: MIT Press, 2022.
- MASSACHUSETTS INSTITUTE OF TECHNOLOGY. **6.006 Introduction to algorithms**. Cambridge: MIT OpenCourseWare, 2020.

### Computer Systems

- PATTERSON, D. A.; HENNESSY, J. L. **Computer organization and design**: the hardware/software interface. 5. ed. Waltham: Morgan Kaufmann, 2014.
- TANENBAUM, A. S.; BOS, H. **Modern operating systems**. 4. ed. Boston: Pearson, 2015.

### Programming Languages

- PIERCE, B. C. **Types and programming languages**. Cambridge: MIT Press, 2002.
- AHO, A. V. et al. **Compilers**: principles, techniques, and tools. 2. ed. Boston: Pearson, 2006.

### Artificial Intelligence

- RUSSELL, S.; NORVIG, P. **Artificial intelligence**: a modern approach. 4. ed. Hoboken: Pearson, 2020.
- VASWANI, A. et al. Attention is all you need. In: ADVANCES IN NEURAL INFORMATION PROCESSING SYSTEMS, 30., 2017, Long Beach. **Proceedings** [...]. Red Hook: Curran Associates, 2017. p. 5998-6008.

### Software Engineering

- SOMMERVILLE, I. **Software engineering**. 10. ed. Boston: Pearson, 2016.
- GAMMA, E. et al. **Design patterns**: elements of reusable object-oriented software. Reading: Addison-Wesley, 1994.

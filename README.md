# GREEN

$n$-gram $F$-score for Grammatical Error Correction

## Installation

```
git clone https://github.com/shotakoyama/green.git
cd green
pip install -e .
```

## Usage

```
green -s input.txt -r reference{0,1}.txt -c system{0,1,2}.txt -t word -n 4 -d 2 -b 2.0
```

## The origin of name GREEN

BLEU ($n$-gram precision) and ROUGE ($n$-gram recall) stand for blue and red, respectively, in French.
GREEN, which is an $n$-gram $F$-score, was named after the remainder of three primary colors.

## Formulation

GREEN treats a sentence as a multiset of $n$-grams with the maximum $n$-gram size $N$.
For example, a sentence “*a a b*” is treated as a multiset {*a*, *a*, *b*, *a a*, *a b*} when $N = 2$.

GREEN compares the match between the corrections from the source sentence $S$ to the reference sentence $R$ and the corrections from $S$ to the corrected sentence $C$.
To count the match between $S \to R$ and $S \to C$, we introduce a Venn diagram illustrating the occurrences of word $n$-grams in $S, R, C$.

<img style="width: 50%;" src="https://raw.githubusercontent.com/shotakoyama/green/main/venn.svg">

Table below shows what types of corrections are performed in $S \to R$ and $S \to C$, respectively, for all $n$-grams in each region of this Venn diagram.

| Region | Name | $S \to R$ | $S \to C$ |
| --- | --- | --- | --- |
| $S \cap \overline{R} \cap \overline{C}$ | True Delete | Delete | Delete |
| $\overline{S} \cap R \cap C$ | True Insert | Insert | Insert |
| $S \cap R \cap C$ | True Keep | Keep | Keep |
| $S \cap R \cap \overline{C}$ | Over-Delete | Keep | Delete |
| $\overline{S} \cap \overline{R} \cap C$ | Over-Insert | None | Insert |
| $S \cap \overline{R} \cap C$ | Under-Delete | Delete | Keep |
| $\overline{S} \cap R \cap \overline{C}$ | Under-Insert | Insert | None |

GREEN uses three operations on multisets: intersection ($\cap$), union ($\cup$), and difference ($\setminus$).
Each operation on multisets $A$ and $B$ is defined concerning the multiplicity of any element $x$ in $A$ and $B$.
The multiplicity of an element $x$ in a multiset $A$, which is denoted as $m_A (x)$, represents the number of times $x$ occurs in $A$.

```math
\begin{align*}
  m_{A \cap B} (x) & = \min (m_A (x), m_B (x)), \\
  m_{A \cup B} (x) & = \max (m_A (x), m_B (x)), \\
  m_{A \setminus B} (x) & = \max (m_A (x) - m_B (x), 0).
\end{align*}
```

The number of $n$-gram $x$ included in each region of the Venn diagram is represented as follows:

```math
\begin{align*}
  \textsf{TD}_{S, R, C} (x)
  = & m_{S \cap \overline{R} \cap \overline{C}} (x) \\
  = & m_{S \setminus (R \cup C)} (x) \\ 
  = & \max\{m_S (x) - \max(m_R (x), m_C (x)), 0\} \\
  \\
  \textsf{TI}_{S, R, C} (x)
  = & m_{\overline{S} \cap R \cap C} (x) \\
  = & m_{(R \cap C) \setminus S} (x) \\
  = & \max\{\min(m_R (x), m_C (x)) - m_S (x), 0\} \\
  \\
  \textsf{TK}_{S, R, C} (x)
  = & m_{S \cap R \cap C}(x) \\
  = & \min(m_S(x), m_R(x), m_C (x)) \\
  \\
  \textsf{OD}_{S, R, C} (x)
  = & m_{S \cap R \cap \overline{C}} (x) \\
  = & m_{(S \cap R) \setminus C} (x) \\
  = & \max\{\min(m_S (x), m_R (x)) - m_C (x), 0\} \\
  \\
  \textsf{OI}_{S, R, C} (x)
  = & m_{\overline{S} \cap \overline{R} \cap C} (x) \\
  = & m_{C \setminus (S \cup R)} (x) \\
  = & \max\{m_C (x) - \max(m_S (x), m_R (x)), 0\} \\
  \\
  \textsf{UD}_{S, R, C} (x)
  = & m_{S \cap \overline{R} \cap C} (x) \\
  = & m_{(S \cap C) \setminus R} (x) \\
  = & \max\{\min(m_S (x), m_C (x)) - m_R (x), 0\} \\
  \\
  \textsf{UI}_{S, R, C} (x)
  = & m_{\overline{S} \cap R \cap \overline{C}} (x) \\
  = & m_{R \setminus (S \cup C)} (x) \\
  = & \max\{m_R (x) - \max(m_S (x), m_C (x)), 0\}
\end{align*}
```

GREEN calculates an $F_{\beta}$ score as follows:

```math
\begin{align*}
    \textsf{TP}_{n, S, R, C} = & \sum_{\mathclap{\forall n\text{-}\mathrm{gram}\ x}} \left( \textsf{TD}_{S,R,C} (x) + \textsf{TI}_{S,R,C} (x) + \textsf{TK}_{S,R,C} (x) \right) \\
    \textsf{FP}_{n, S, R, C} = & \sum_{\mathclap{\forall n\text{-}\mathrm{gram}\ x}} \left( \textsf{OD}_{S,R,C} (x) + \textsf{OI}_{S,R,C} (x) \right) \\
    \textsf{FN}_{n, S, R, C} = & \sum_{\mathclap{\forall n\text{-}\mathrm{gram}\ x}} \left( \textsf{UD}_{S,R,C} (x) + \textsf{UI}_{S,R,C} (x) \right)
\end{align*}
```

```math
\begin{align*}
    \mathrm{prec} (N, \mathbb{S}, \mathbb{R}, \mathbb{C}) = & \left( \prod_{n=1}^{N}
    \frac{\displaystyle \sum_{i=1}^{D} \textsf{TP}_{n, S_i, R_i, C_i}}{\displaystyle \sum_{i=1}^{D} \left( \textsf{TP}_{n, S_i, R_i, C_i} + \textsf{FP}_{n, S_i, R_i, C_i} \right)}\right)^{\tfrac{1}{N}} \\
    \mathrm{recall} (N, \mathbb{S}, \mathbb{R}, \mathbb{C}) = & \left( \prod_{n=1}^{N}
    \frac{\displaystyle \sum_{i=1}^{D} \textsf{TP}_{n, S_i, R_i, C_i}}{\displaystyle \sum_{i=1}^{D} \left( \textsf{TP}_{n, S_i, R_i, C_i} + \textsf{FN}_{n, S_i, R_i, C_i} \right)}\right)^{\tfrac{1}{N}} \\
    F_{\beta} (N, \mathbb{S}, \mathbb{R}, \mathbb{C}) = &
    \frac{(1+\beta^2) \mathrm{prec} (N, \mathbb{S}, \mathbb{R}, \mathbb{C})  \mathrm{recall} (N, \mathbb{S}, \mathbb{R}, \mathbb{C})}{\beta^2 \mathrm{prec} (N, \mathbb{S}, \mathbb{R}, \mathbb{C}) + \mathrm{recall} (N, \mathbb{S}, \mathbb{R}, \mathbb{C})}
\end{align*}
```

# Regular Expressions

Regular expressions (a sequence of characters that define a search pattern) are used to match your log event code sequences. See ~training/cheatsheets/regex-cheatsheet-for-mkpy.pdf for more detail; the basics are below

## Ordinary characters 
match themselves 1-1 for each letter, numeral, and white space (white space is in between each event code when we are matching codes in our log files)

```{admonition} Example
`1234` &nbsp; matches `1234` &nbsp; but not `1324` &nbsp; or &nbsp; `12 34`
```

## Metacharacters 
define complex patterns using symbols combined with numbers or specifiers

### Basic Matching
each symbol matches a single character
```{admonition} Example
\. &nbsp; = &nbsp; anything (other than line breaks)

\\d &nbsp; = &nbsp; digit (0123456789)

\^ &nbsp; = &nbsp; not this (i.e., ^1 would match any character, including non-numbers, other than 1)

### Square Brackets 
define a set of characters to match

```{admonition} Example
`[123]456` &nbsp; matches `1456` &nbsp; and &nbsp; `2456` &nbsp; and &nbsp; `3456` &nbsp; but not `4456`
```

### Backslash Characters 
match a type of character, e.g., numerals

```{admonition} Example
`\d456` &nbsp; and &nbsp; `[0123456789]456` &nbsp; are equivalent and would match `1456` &nbsp; and &nbsp; `2456` &nbsp; and so on
```
### Quantifiers 
specify the number of pattern repetitions to match for the character before it

```{admonition} Example
\* &nbsp; = &nbsp; zero or more, &nbsp; `12*3` &nbsp; matches `13` &nbsp; and &nbsp; `123` &nbsp; and &nbsp; `1223` &nbsp; and &nbsp; `12223` &nbsp; and so on

\+ &nbsp; = &nbsp; one or more, &nbsp; `12+3` &nbsp; matches `123` &nbsp; and &nbsp; `1223` &nbsp; and &nbsp; 12223 &nbsp; and so on

{3} &nbsp; = &nbsp; exactly 3, `1\d{3}3` &nbsp; matches `10003` &nbsp; and &nbsp; `11113` &nbsp; and &nbsp; `12223` &nbsp; and so on

{1,3} &nbsp; = &nbsp; between 1 and 3, `12{1,3}3` &nbsp; matches `123` &nbsp; and &nbsp; `1223` &nbsp; and &nbsp; `12223` &nbsp; (only)
```

### Parentheses 
capture a subpattern or group within the pattern
```{admonition} Example
`(1234) 56 78` &nbsp; captures the group `1234` &nbsp; that is followed by `56 78`

`(\d234) 56 78` &nbsp; captures any group of digits ending in `234` &nbsp; followed by &nbsp; `56 78`

`(\d{4})` &nbsp; captures any group of 4-digits 
```

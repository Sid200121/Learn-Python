"""
Static curriculum content.
Structure: each LEVEL has several short LESSONS (just concept + tiny example,
no project attached), then ONE level-ending PROJECT that combines everything
taught in that level. Passing the project (score >= 70) unlocks the next level.
"""

LEVELS = [
    (0, "Setup & Basics", "print, variables, data types, input, basic math"),
    (1, "Control Flow", "if/else, loops, comparison & logic operators"),
    (2, "Data Structures", "lists, dicts, tuples, sets"),
    (3, "Functions", "defining, args/kwargs, return values, scope"),
    (4, "Files & Errors", "reading/writing files, try/except"),
    (5, "OOP", "classes, objects, inheritance"),
    (6, "Modules & Libraries", "imports, pip, using external packages"),
    (7, "Real Projects", "combine everything — CLI tools, small games, automations"),
]

LESSONS = [
    # ---- Level 0 ----
    {
        "id": "L0-01",
        "level_id": 0,
        "position": 1,
        "name": "Print & variables",
        "lesson_md": """
`print()` shows text on screen. A variable is a name that points to a value:

```python
name = "Sid"
age = 24
print("Hello", name, "you are", age)
```
""",
    },
    {
        "id": "L0-02",
        "level_id": 0,
        "position": 2,
        "name": "Data types",
        "lesson_md": """
Python figures out the *type* for you: `"Sid"` is a `str`, `24` is an
`int`, `24.5` is a `float`, `True`/`False` is a `bool`. Check with `type(x)`.
""",
    },
    {
        "id": "L0-03",
        "level_id": 0,
        "position": 3,
        "name": "Input & basic math",
        "lesson_md": """
`input()` reads text typed by the user — it's always a string, so convert
it when you need a number:

```python
age = int(input("How old are you? "))
print("Next year you'll be", age + 1)
```

Basic operators: `+ - * /` (true division), `//` (floor division), `%`
(remainder), `**` (power).
""",
    },
    # ---- Level 1 ----
    {
        "id": "L1-01",
        "level_id": 1,
        "position": 1,
        "name": "If / else & comparisons",
        "lesson_md": """
`if`/`elif`/`else` branch based on a condition. Comparisons (`==`, `!=`,
`<`, `>`, `<=`, `>=`) return `True`/`False`:

```python
score = 76
if score >= 90:
    print("A")
elif score >= 75:
    print("B")
else:
    print("C")
```
""",
    },
    {
        "id": "L1-02",
        "level_id": 1,
        "position": 2,
        "name": "Logic operators",
        "lesson_md": """
Combine conditions with `and`, `or`, `not`:

```python
age = 20
has_id = True
if age >= 18 and has_id:
    print("allowed in")
```
""",
    },
    {
        "id": "L1-03",
        "level_id": 1,
        "position": 3,
        "name": "For loops",
        "lesson_md": """
`for` loops repeat over a known range or sequence:

```python
for i in range(5):
    print(i)

for letter in "abc":
    print(letter)
```
""",
    },
    {
        "id": "L1-04",
        "level_id": 1,
        "position": 4,
        "name": "While loops",
        "lesson_md": """
`while` loops repeat until a condition becomes false — useful when you
don't know in advance how many times you'll loop:

```python
n = 5
while n > 0:
    print(n)
    n -= 1
```

Careful: always make sure something inside the loop moves it toward
being false, or you'll loop forever.
""",
    },
]

LEVEL_PROJECTS = {
    0: {
        "brief_md": """
**Build a tiny "About Me" script.**

- Store your name, age, and one favorite thing as variables (mix of types)
- Ask the user for one more piece of info with `input()`
- Print a short paragraph about yourself using those variables
- Print the *type* of each variable on a separate line
""",
        "rubric_md": """
Check for: at least 3 variables of different/appropriate types, correct
use of input() with type conversion if needed, use of print() with
variables (not just hardcoded strings), correct use of type(), and that
the code runs without errors.
""",
    },
    1: {
        "brief_md": """
**Build a number-guessing game.**

- Set a secret number as a variable
- Loop, asking the user to guess, until they get it right
- After each wrong guess, tell them "higher" or "lower" using if/elif/else
- Count and print how many guesses it took
- Bonus: give up and reveal the answer after 5 wrong guesses
""",
        "rubric_md": """
Check for: correct loop choice (while) with a real termination condition,
correct higher/lower branching logic, a working guess counter, and that
the loop can't run forever on valid input. Bonus check: the give-up
condition after 5 guesses, if attempted.
""",
    },
}

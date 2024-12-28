# Advent of Code 2024

## How I do the puzzles

* I try to solve the puzzles in order. (This year, it worked until day 21, part
  2. I got stuck on it and decided it would be more fun to continues without it
  solved.)

* I don't look at others' solutions for a puzzle until I have solved both
  parts.

* When I have solved both parts, I look at others' solutions if I'm curious.

## File name explanations

* Files named `{day}.py` and `{day}_part2.py` are my solutions without having
  looked at other solutions. (From day 11, both parts are included in a single
  file.)

* Files with other suffixes are done afterwards.

## What I practiced this year

* I practiced object oriented design this year. So my solutions involve many
  small objects interacting with each other to produce a solution.

* I also wanted to solve all puzzles, so I learned algorithms needed. This year
  I think I got the hang of Dijkstra and A\*. (I found [Introduction to the A\*
  Algorithm
  ](https://www.redblobgames.com/pathfinding/a-star/introduction.html) from Red
  Blob Games really helpful.)

## Running my code

All files are completely self contained. They only depend on Python standard
libraries and the input file. (Some interactive modes depend on GTK to draw
visualizations.)

The first 6 days are run like this:

    python {day}.py < {day}.txt

After that I decided it was more convenient if the program read the file
itself, so only the following is needed:

    python {day}.py

Some days (16, 20, 21) have and interactive mode that either shows an animation
or runs some code that prints to the terminal. Those are invoked like this:

    python {day}.py interactive

## Notes

* Redo 6 part 2 (seems very slow)
* Redo 7 part 2 (is quite slow)
* Redo 9 part 2 (solution took long and was not very nice)

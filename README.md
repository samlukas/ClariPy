# ClariPy

CSC111 Project Report: ClariPy
Samuel Lukas, Aleksandr Kovalev, Kevin Li
Monday, April 3, 2023
Source Code: https://github.com/samlukas/ClariPy

# Problem Description and Research Question
  The problem that we are primarily dealing with is transpiling, which is essentially translation from one pro-
gramming language to another. Our idea was to transform python code into code that mimics structured human
language and can be understood by someone that does not necessarily understand Python. Trees play a key role
in transpiling (translation from one programming language to another), specifically the so-called Abstract Syntax
Trees. ASTs (Abstract Syntax Trees) are essentially tree representations of source code, where each node represents
a statement/expression.

  To provide context, programming is becoming more popular, and thus, more tools need to be developed that make
learning how to program more interactive and exploitative. To the beginner, providing autonomy and the ability to
tinker and approach various programming concepts through hands-on learning is crucial. Furthermore, tying this
learning into something as intrinsic as English may bolster learning. Being able to translate code into something we
are familiar with allows the user to learn how to code in a similar way to learning a new language. This ultimately
allows the user to associate code with phrases or words known to them, allowing code to be constructed naturally.
The goal of this project is to use ASTs to allow beginner programmers to better understand
the code that they write by translating expressions into thorough descriptions that mimic human
language. We will accomplish this by allocating pseudo language to various code blocks in the AST,
converting between tree structure and readable statements. While our original goal has not changed, the
steps we took to accomplish it have been slightly tweaked. We have included visual representations as per the TA’s
advice. Furthermore, we have restricted our problem domain to be more simplistic, thus also changing our parsing
and tokenizing algorithms. Even with these changes, ClariPy still accomplishes what we originally hoped it would.

# Computational Overview

  The chosen domain for this problem is a relatively small subset of Python, in order to make it feasible to solve.
We largely limited ourselves to content covered in CSC110, though we omitted certain things such as custom class
and function definition. Our project supports basic control flow statements, variable definition, basic array definition
and mutation and outputting via printing.

  The first part of our project is the conversion of Python programs to the pseudo-language we have designed.
The parsing of the Python code is done through the official ast module. Now, to actually produce the result in our
language, we have modified the str methods of the ast nodes of interest. This required creating separate functions
and then directly assigning them to those methods. The alternative was to create subclasses with those methods
redefined, but that would require create many such classes and require us to modify the ast’s parsing algorithms,
which is far above the scope of the scope project. Due to the recursive nature of the str methods, all that is
required is to produce a translation of a Python program is to call the str on the ast.Module node.
The pseudo-language we have created is closer in syntax to C-style languages than to Python. It demands
semicolons after statements (unless it is a While or If statement), clear designation of If and While’s test with regular
parentheses and their bodies with braces. There have been other alterations made to push the language closer to
human language, such as more verbal definition statements and allowing to switch comparator operators for their
verbal equivalents.

  After this comes the second part of the project - actually parsing and interpreting the language we have created.
While the initial plan was to convert our code to the ast node modules, due to the many variables one would have to
account for, we have made the decision to create our own module. The module is located in classes.py, and outlines
nodes similar to the Python ast module. The nodes in question have recursive defined evaluate methods. In order
to evaluate a whole program, the evaluate method parses through the statements in the body instance variable,
evaluating those statements, which in turn evaluate their children recursive.

This prepares a structure for the actual parsing, which is done throug the course of several steps:

1. Tokenization - the function tokenize breaks up the program into a set of tokes. It uses a precompiled regex
expression to detect what sequence of characters form satisfy the characteristics of a certain token and split
entire string into those tokens. After this, the ”lexer” function converts the leaves of the future AST - which
includes Nums and Strs. The lexer also accounts for Names and Subscripts (which are used for list indexing),
as they are fairly close to being a leaf, and converting them to a node simplifies the further parsing.

2. Parsing - when we have the list of all the tokens that make up the program, we need to process them into an
appropritate structure. The approach that we have used is a mix of top-down and bottom-up parsing.
The top-down aspects of our parsing algorithm is that it predicts a token that comes after a given token ac-
cording to the grammar rules (for instance, after a ’While’ token, the parser expects an opening parenthesis).
However, this approach is not particularly good at parsing expressions, as it has to factor precedence, paren-
theses and many other factors. Thus, whenever the parser expects an expression, it actually parses it using a
bottom up algorithm. Typically, the parser finds boundaries of an expression. For instance, the test expression
for a While loop is expected to be enclosed by parentheses. When we get to an opening parenthesis after a
’While’ token, we can search for a matching closing parenthesis using the matching parenthesis function. Once
we find it, we essentially have the bounds on the expression, allowing us to process it.

  To process an expression, we must first convert it to Reverse-Polish Notation using the Shunting Yard algorithm.
Reverse-Polish Notation is a way of representing expressions where the operators are postfixes (come after the
operands), instead of infixes (between operands). This makes it much more easier to parse, as it not only
removes the need for parentheses but also can be done by stacking operands and matching them to operators,
with the result being added back onto the stack. This is exactly what the function polish to ast does, with its
output being either an Expr node.

  Combining these two approaches, the parsing algorithm parses through the entire list of tokens, matching
the encountered tokens to known structures. Due to it predicting what a given structure should look like,
it is actually capable of detecting simple syntax errors (unmatched parentheses, missing semicolon statement
separators and etc). Once a statement has been matched, it is added to a accumulator list. After the parsing
is done, that accumulator becomes the body of the Module node, which is then returned.

4. Compilation - once we have the Module node, all that remains is to execute it to get the output of the function.
Due to the recursive nature of the evaluate method, calling it on the Module (which is practically the root of
the AST) would evaluate all children as well.

6. Visualization - for converting pseudo-code to Python, given the parsed module object from the aforementioned
steps, the first step of the visualizer converts the module object into a Tree, this Tree class works identically to
the Tree class discussed in lecture. We then converted the tree into an igraph Graph, with each root value being
a vertex and an edge between every root and child. We utilized the igraph Graph class due to its compatibility
with plotly, we can generate coordinates for plotting from the graph vertices and edges using the igraph Graph
methods. The coordinates are then plotted on plotly, representing the full abstract syntax tree. For converting
python to pseudo-code, we simply evaluate the module node and print it as a string.

# Instructions
  Running the program is fairly simple, provided that the dependencies have been installed. Upon running the
program, you will be prompted with a new window and your file browser, from the file browser you can choose a valid
file for the program to execute and visualize, either a .py file or .txt file are allowed, please check that the file only
contains valid python code or pseudo code. This includes assignments, control flow statements, binary and boolean
operations, literals, as well as while loops. After confirming the file, the runner will transpile pesudo code to python
code or python code to pseudo code depending on the file extension, a plotly window will then be prompted with the
results. The original program window will remain if the user wishes to select another file using the top button, and
the program can be closed using the bottom exit button or simply closing the window. We provided four example
files to test out the capabilities of ClariPy.

  Firstly, you have sums py to lang.py, a python code block specifically for demonstrating converting Python to
the pseudo-language. This is a simple program that computes the sum of numbers from 1 to 100 in the two different
ways and comparing their final values. The expectation is that it produces code equivalent to the one in sums.txt.
Next comes the block for sums.txt - now it is an identical program except written in the pseudo-language.
Running this should produce a parse of the program, which is then converted to a graphical tree representation
and evaluated. The expected output is True, as even though one method produces a float, and the other an int,
they should still be equal. This program specifically demonstrates the capacity of this language in accumulation
and dealing with relatively complex expressions. Commented out are the code for the other two sample program -
fizzbuzz and fizzbuzz array. In order for run one of them, comment out the other two segments and then run the
program.

  The fizzbuzz program is self-explanatory. Running should print out numbers from 1 to 100, replacing a number
with FIZZ if divisible by 3, BUZZ if divisible by 5, and FIZZBUZZ if divisible by both 3 and 5. While it is a fairly
simple program, it demonstrates the language’s capacity for relatively complex loop bodies and if statements with
multiple branches. Just like before, a graphical representation of the AST should also be produced.
The fizzbuzz array is pretty much identical to fizzbuzz, expect now it deals with a list, mutating it at appropriate
indices. It should print out the list where some values have been mutated with the accordance with the rules stated
above. This program is meant to demonstrate the language’s support for simple mutation of lists.

# Changes
  As we made progress with our project, we have made several changes to our original design, based both on TA
feedback and our own discussions. Firstly, one significant change we’ve made to our design was introducing the
visualization, as per the TA’s advice.
Futhermore, through the advice of the TA, we have also decided to restrict our problem domain, removing
functions and greatly simplifying arrays. However, we did decide against our initial plan of making expressions and
arithmetic extremely rigid for the sake of easier parsing. In order to figure out how to deal with this in a flexbile
manner, we had to do research on algorithms, specifically what algorithms could be used to parse expressions while
taking operator precedence in account. And thus we have come to select shunting yard algorithm for this task.
Initially, our plan for tokenization was to define specific token that a given series of characters could represent
and then manually search for those. In order to simplify this, we have instead switched our plan to use regex. While
it certainly lacks in scalability, requiring adding new operators and keywords to regex expressions as you continue
developing, for the purposes of our project it proved to be most suitable.

  Another change to the parsing algorithm was how it deals with grammar. Initially, we have planned to define
grammar explicitly and then parse the tokens to fit them. This would likely require more research and also additional
libraries. Considering the rather simple grammar of our language and the desire to implement as much of parsing
ourselves as possible, we have instead decided to define the grammar implicitly in the body of the while loop of
the parse statements function. While it certainly reduces scale-ability, it was somewhat appropriate to the simple
programming language we were creating.

  Another minor change was a change to the compilation step. Initially, we have considered to convert the program
to a Python ast (from the ast module) and then either execute it as Python code or transpile it to Python. However,
ast module was proven to be quite cumbersome to work with - for the creation of the tree nodes, we had to consider
many Python specific aspects (such as indentiation for group statements, for instance), which our language simply
did not have. Thus, we have made the decision to instead produce our own AST node classes, and then use the
parser to convert to them directly. This still allows for very simple evaluation of the code, while also remaining open
to transpiling - all that would be required to convert the language to Python is to define the str methods of the
Nodes.

# Discussion
  Overall, ClariPy accomplished our original goal. We created a system that allows users to translate python code
into a pseudo-language representation and back into python code that could be parsed and evaluated. By translating
python code into pseudo-code, the user can interpret the code in a way that is easier to understand. We chose to use
pseudo-code similar to English to utilize keywords that encapsulate the code that it represents to avoid taking away
the feeling of reading code. However, ClariPy still nonetheless provides a more easily understandable interpretation
that is intrinsically familiar to the user. On the flip side, by allowing the user to create ”blocks” of pseudo-code
that can be translated into python code and evaluated, ClariPy promotes a more modular style of learning that
encourages creativity. These features ultimately allow for a rudimentary and self-driven experience for the user that
allows for a holistic learning experience for the average beginner.

  Throughout the process of developing ClariPy, we faced many limitations and challenges. Firstly, parsing the
pseudo-code proved to be very challenging. It was difficult to develop algorithms that determine what type of
statement or expression was being parsed, especially when the provided pseudo-code was in the form of a string. To
parse the pseudo-code, we had to make multiple helper functions to detect whether a given statement or expression
was going to be an if statement, a while loop, or even a normal assignment statement; all possibilities had to be
accounted for. Because of this, we had to limit what pseudo-code a user was allowed to write, due to being unable
to write helper functions for every python functionality that would be typically available to a python user. It would
have been extremely time-consuming, labor-intensive, and arduous modifying parsing algorithms to account for niche
python expressions so as a result, we were forced to limit ourselves to an elementary subset of python. Another issue
we encountered was graphically representing the AST. Because the AST is not a conventional Tree data structure
per se, it was difficult to determine how to format it in a way that was familiar to us and even hard to figure out
how to traverse the tree. To properly format the tree, we had to determine what type of object we were recursing
into. Furthermore, to visualize the tree itself, we had to use Plotly, igraph, and Tkinter. It was difficult optimizing
the intricacies of the visualization itself, from representing the different nodes of the tree to connecting the nodes
themselves graphically; the entire process was strenuous and arduous leading to various limitations. The visualization
itself could be improved upon for a more clear and more interactive user experience.

  In terms of further exploration when it comes to ClariPy, there are a few different paths we could take. Building on
our first limitation, we can account for more Python expressions or statements to make ClariPy more comprehensive
and realistic. To accomplish this, we have to add additional classes to represent the AST nodes that would represent
these expressions or statements. Furthermore, we would then have to modify our parsing algorithms to account for
these additional expressions or statements. We may have to write helper functions to help detect these statements
when we parse through the user-provided tokens to convert them into their corresponding AST node. We would also
have to account for these additional nodes when we have to recurse through the AST in order to create graphical
visualizations. Another way we could extend ClariPy is by how we interact with the user. Currently, making the
user create a file containing the pseudo-code is inconvenient and overly complicated. Rather, it would be easier for
both the user and us to provide the user with a GUI or some other user interface that allows the user to easily
translate back and forth between pseudo-code and python code. This would allow for a much more interactive and
beginner-friendly user experience, aligning with what we originally hoped to achieve with ClariPy.
Ultimately, what we’ve created in ClariPy is an intuitive tool that may complement beginner learning. ClariPy
provides a naturally hands-on experience to beginners by equating python code to pseudo-code that is intrinsically
similar to python code and English, making it easily understood. While there is still room for growth and exploration,
ClariPy tackles the daunting task of learning how to program with simplicity and familiarity.

# References
  Antlr. “ANTLR4/Index.md at Master · ANTLR/ANTLR4.” GitHub, 25 Dec. 2021,
https://github.com/antlr/antlr4/blob/master/doc/index.md.

  “AST - Abstract Syntax Trees.” Python Documentation, https://docs.python.org/3/library/ast.html.
  
  “AST Observe/Rewrite.” Astor, https://astor.readthedocs.io/en/latest/.
  
  “Graphical User Interfaces with Tk.” Python Documentation, https://docs.python.org/3/library/tk.html.
  
  “Green tree snakes - the missing python ast docs” Green Tree Snakes - the missing Python AST docs - Green
Tree Snakes 1.0 documentation, https://greentreesnakes.readthedocs.io/en/latest/index.html

  Kuchling, Andrew M. “Regular Expression HOWTO.” Python Documentation, https://docs.python.org/3/howto/
regex.html.

  McIlroy, Mark. ”Reverse Polish Notation.” From MathWorld–A Wolfram Web Resource, created by Eric W.
Weisstein. https://mathworld.wolfram.com/ReversePolishNotation.html

  Md Shuvo on May 10, and Md Shuvo. “Let’s Create a Tiny Programming Language: CSS-Tricks.” CSS,
11 May 2022, https://css-tricks.com/lets-create-a-tiny-programming-language/.

  “Parsing.” Parsing , https://ucsb-cs56-pconrad.github.io/tutorials/parsing/.
  
  “Pygments Documentation.” Pygments, https://pygments.org/docs/.
  
  “Python API reference for plotly.” plotly, https://plotly.com/python-api-reference/.
  
  “Python-igraph API reference.” igraph, https://igraph.org/python/api/latest/.
  
  Rompf, Tiark. “Just Write the Parser.” Tiark’s Notebook, https://tiarkrompf.github.io/notes/?
  
  Setunga, Supun. “Writing a Parser-Part I: Getting Started.” Medium, Medium, 10 Sept. 2020,
https://supunsetunga.medium.com/writing-a-parser-getting-started-44ba70bb6cc9.

  Wolf, Carol E., and Paul Oser. “The Shunting Yard Algorithm.” The Shunting Yard Algorithm,
https://mathcenter.oxford.emory.edu/site/cs171/shuntingYardAlgorithm/.

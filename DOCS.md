#Documentation
##Section 1 - Rules, Style, and Structure
###Data Types
PokePL has two primitive types: strings and numbers.
###Comments
In PokePL, comments are denoted using `~`.  
`~this is a sample comment`  
Comments may be at the end of a statement, or placed on their own line. Comments in the middle of statements are not valid.
###Statements
In PokePL, each line should contain one and only one complete statement. Statements/lines will be executed in order from top to bottom of the source file.  
Therefore, additional whitespace beyond the newline characters is not required, but you may find it useful for organization and readability.
###Blocks
In PokePL, blocks (such as conditionals and loops) begin with their respective syntax and are terminated by an `OKAY` statement.  
More details below.
###Grouping
Instead of traditional parentheses, grouping is done using Pokeball halfs. `(-` will open a group and `-)` will close it.  
For example:  
`(- 5 WITH 3 -) BY 2`  
will evaluate to 16.

##Section 2 - Variable Declaration and Assignment
Variables must be named after one of the original 151 Pokemon.  
This is case insensitive, so there is a maximum of 151 consecutive variables.  

All variables must be declared before they can be assigned a value or otherwise interacted with, as follows:  
`WILD <varname> APPEARED`

Conversely, to destroy a variable, use:  
`WILD <varname> FAINTED`

Once declared, they can be assigned a value. The syntax depends on the type of data and whether they are being assigned a literal, another variable, or an expression.  
To assign a literal string value to a variable name, use:  
`NAME <varname> <literal>`  
and to assign a literal number value to a variable name, use:  
`LEVEL <varname> <literal>`

To assign another variable or an expression to the variable, however, the `LIKE` keywords must be used, i.e:  
`NAME <varname> LIKE <varname/expression>`  
`LEVEL <varname> LIKE <varname/expression>`

##Section 3 - Operators
###Numeric operations
addition: `<value> WITH <value>`  
subtraction: `<value> LESS <value>`  
multiplication: `<value> BY <value>`  
division: `<value> OVER <value>`

unary increment shorthand: `<varname> LEVELED UP`

###String operations
concatenation: `<value> JOIN <value>`

##Section 4 - Logic and Comparisons
negation: `NOT <value>`  
and: `<expression> AND <expression>`  
or: `<expression> OR <expression>`  
equality: `<value> SAME AS <value>`  
greater than: `<value> STRONGER THAN <value>`  
less than: `<value> WEAKER THAN <value>`

##Section 5 - Conditional Blocks
If blocks begin with `IS <expression>?` and terminate with a `OKAY` statement.  
```
IS BULBASAUR SAME AS SQUIRTLE?
	~code
OKAY
```

Like most languages, if blocks can be extended to include elif and else.  
In such a case the `OKAY` statement will terminate the _entire_ block chain.  
```
IS BULBASAUR SAME AS SQUIRTLE?  
	~code
OR IS BULBASAUR SAME AS CHARMANDER?
	~code
NO?
	~code
OKAY
```

##Section 6 - Loops
There is only one type of loop in PokePL. It is the equivalnet of most languages' "while" loops.  
The syntax is as follows:
```
BATTLE <expression>
	~code
OKAY
```
It is possible to move on to the next iteration, or break out of the loop completely using the keywords `FIGHT` and `RUN` respectively.  
This is logically equivalent to the typical `continue` and `break` syntax.

While there are no native "for" loops in PokePL, they are easy to simulate.  
Here is a simple example:
```
WILD PIDGEY APPEARED
LEVEL PIDGEY 0

BATTLE PIDGEY WEAKER THAN 10
	PIDGEY LEVELED UP
	~code
OKAY
```
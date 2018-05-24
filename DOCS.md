# Documentation
## Section 1 - Rules, Style, and Structure
### Data Types
PokePL has two primitive types: strings and numbers.
### Comments
In PokePL, comments are denoted using `~`.  
`~this is a sample comment`  
Comments may be at the end of a statement, or placed on their own line. Comments in the middle of statements are not valid.
### Statements
In PokePL, each line should contain one and only one complete statement. Statements/lines will be executed in order from top to bottom of the source file.  
Therefore, additional whitespace beyond the newline characters is not required, but you may find it useful for organization and readability.
### Blocks
In PokePL, blocks (such as conditionals and loops) begin with their respective syntax and are terminated by an `OKAY` statement.  
More details below.
### Grouping
Instead of traditional parentheses, grouping is done using Pokeball halfs. `(-` will open a group and `-)` will close it.  
For example:  
`(- 5 WITH 3 -) BY 2`  
will evaluate to 16.

## Section 2 - Variable Declaration and Assignment
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

## Section 3 - Operators
### Numeric operations
addition: `<value> WITH <value>`  
subtraction: `<value> LESS <value>`  
multiplication: `<value> BY <value>`  
division: `<value> OVER <value>`

unary increment shorthand: `<varname> LEVELED UP`

### String operations
concatenation: `<value> JOIN <value>`

## Section 4 - Logic and Comparisons
negation: `NOT <value>`  
and: `<expression> AND <expression>`  
or: `<expression> OR <expression>`  
equality (string): `<value> SAME NAME AS <value>`  
equality (num): `<value> SAME LEVEL AS <value>`  
greater than: `<value> STRONGER THAN <value>`  
less than: `<value> WEAKER THAN <value>`

## Section 5 - Conditional Blocks
If blocks begin with `IS <expression>?` and terminate with a `OKAY` statement.  
```
IS BULBASAUR SAME AS SQUIRTLE?
	~code
OKAY
```

## Section 6 - Loops
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

## Section 7 - Built-in Functions
Built-in functions in PokePL are named after moves from the first generation Pokemon games, and use the following syntax:  
`<varname> USED <funcname>`

For functions that require additional parameters, use the `ON` keyword:  
`<varname> USED <funcname> ON <value>`

### Basic Functions
`CONVERSION` will attempt to cast a string to a number.  
Calling it alone will perform it on the calling variable, but using `ON` will cast the passed variable.
```
WILD GROWLITHE APPEARED
NAME GROWLITHE '5'
GROWLITHE  USED CONVERSION
~5

WILD ARCANINE APPEARED
NAME ARCANINE '23'
GROWLITH USED CONVERSION ON ARCANINE
~23
```

`TRANSFORM` works similarly to `CONVERSION`, but will attempt to cast a number to a string.
```
WILD ZAPDOS APPEARED
LEVEL ZAPDOS 10
ZAPDOS USED TRANSFORM
~'10'
```
### MATH FUNCTIONS
`CUT` will reduce a number to the nearest integer value.

`FLY` will increase a number to the nearest integer value.

`CLAMP` will round a number to the nearest integer value, away from 0.

`METRONOME` will generate a random number between 0 and `<value>` and put the result in `<varname>`  
For example, generating a number between 0 and 100 and putting the result in a variable called `CLEFAIRY` may be written as follows:
```
WILD BULBASAUR APPEARED
LEVEL BULBASAUR 100
WILD CLEFAIRY APPEARED
CLEFAIRY USED METRONOME ON BULBASAUR
```

### I/O Functions
`GROWL` will output the value of the variable calling it to the terminal.  
For example, the basic Hello World program may be written as follows:  
```
WILD BULBASAUR APPEARED
NAME BULBASAUR "Hello World!"
BULBASAUR USED GROWL
```

`SUBSTITUTE` will prompt the user to input a value for the variable, which will _always_ be stored as a string.  
For example, an echo program looks like:
```
WILD CHARMANDER APPEARED
CHARMANDER USED SUBSTITUTE
CHARMANDER USED GROWL
```

`MIMIC` will open a file and store its contents as a string in the calling variable. For example:
```
WILD MUK APPEARED
MUK USED MIMIC ON "file.txt"
MUK USED GROWL
```
will echo the contents of a file.

Conversely, `ROAR` will dump the contents of a variable into the file, creating it if it does not exist.
```
WILD MUK APPEARED
NAME MUK "test data"
MUK USED ROAR ON "file.txt"
```

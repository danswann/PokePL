#Documentation
##Section 1 - Style and Structure
Placeholder.

##Section 2 - Variable Declaration and Assignment
Variables must be named after one of the original 151 Pokemon.  
This is case insensitive, so there is a maximum of 151 consecutive variables.  

All variables must be declared before they can be assigned a value or otherwise interacted with, as follows:  
`WILD <varname> APPEARED`

Conversely, to destroy a variable, use:  
`WILD <varname> FAINTED`

Once declared, they can be assigned a value. The syntax depends on the type of data and whether they are being assigned a literal, another variable, or an expression.  
To assign a literal number value to a variable name, use:  
`NAME <varname> <literal>`  
and to assign a literal string value to a variable name, use:  
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
	(- code -)
OKAY
```

Like most languages, if blocks can be extended to include elif and else.  
In such a case the `OKAY` statement will terminate the _entire_ block chain.  
```
IS BULBASAUR SAME AS SQUIRTLE?  
	(- code -)
OR IS BULBASAUR SAME AS CHARMANDER?
	(- code -)
NO?
	(- code -)
OKAY
```
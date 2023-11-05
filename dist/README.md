Design Decisions:

M1:
- ensure helper methods instead of assert
- each operation in grouped classes as static methods
- set checks all environments begin at the root and tries to set where present downwards and if new stores in the leave envirnoment
- get retrieves in the opposite order of set upward the environment tree
- operations which are not allowed to be nested return "illegal" this way the interpreter can ensure that there's no illegal nesting going on
- if has optional parameter for the else instructions
- all instructions have to be sequence
- every time the execute detects and executes a sequence a new environment gets created and destroyed when the sequences finishes
- when a new environment gets created it automatically appends itself when possible at the bottom of the environment tree 
- the environments handle scopes aka variable contexts
- when a environment gets destroyed it removes itself from the global environment tree
- destroyed environments can not be reached and are illegal to access
- the interpreter stores a map which links all commands to the corresponding internal logic
- the interpreter loads code automatically based on cli args and parses it as a json
- the interpreters execute method is similar to the do method and handles dynamically sequences, operations and values
-  let python do the handling of operations with different types like list + list, true or dict, string == object, etc.
- use previous and next to navigate through environment tree
- don't use key word "seq" but instead find out ourselves, where sequence starts and ends
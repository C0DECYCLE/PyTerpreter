# PyTerpreter - A Lightweight Python Interpreter

PyTerpreter is a lightweight Python interpreter designed for simplicity and ease of use. It provides a convenient
interface for executing Python-like commands and scripts. This interpreter is suitable for small to
medium-sized projects and is built with a focus on clarity and clean design.
(https://github.com/C0DECYCLE/PyTerpreter.git)

## Key Features:
- Basic Operations: PyTerpreter supports fundamental Python-like operations, making it suitable for various scripting tasks.
- Environment Management: The interpreter manages environments to handle variable scopes and ensure clean execution.
- Dynamic Execution: PyTerpreter dynamically executes sequences, operations, and values, 
providing flexibility in script structure.
- Error Handling: Comprehensive error messages enhance the understanding of issues during execution.
- Automatic Sequence Tracking: PyTerpreter doesn't use the "seq" keyword, but automatically handles it through logic.

## Design Decisions:

### Code Organization
- Use of "Ensure" Helper Methods: PyTerpreter prioritizes the use of "Ensure" helper methods over assert statements,
enhancing code robustness and scalability with clear error messages.
- Grouping Operations into Classes: Operations are organized into classes like "PyTerpreterBoolean" or
"PyTerpreterConditional" with static methods. These all get handle through the command logic mapping, so they can
be used in the main class.
- Command-Logic Mapping: PyTerpreter maintains a map linking commands to internal logic, simplifying execution.
All commands get added in the init of the PyTerpreter class, from where it can be executed as a command in
the PyTerpreter language. This structure improves code organization and readability.

### Variable Management
- Set Operation Behavior: The "set" operation traverses environments from the root, attempting to update in the first
environment that already has that variable name. If no previous variable value is found, the variable with the value
is stored in the current leaf environment. 
This ensures correct updating and "placement" of a variable, so it is in the right scope.
- Get Operation Behavior: The "get" operation retrieves variables in the opposite, from the current environment up
the tree until root. Once more this ensures the right scope when getting a variable, picking the "closest" environment
where a variable had been set.
- Illegal Nesting Prevention: Operations not allowed to be nested return "illegal," preventing undesirable nesting.
So "Illegal" is a predefined keyword the user can't use when coding in PyTerpreter. There is also a helper function
in the PyTerpreterEnsure class.

### Script logic
- Optional "If" Parameter: The "if" operation includes an optional "else" parameter, enhancing script logic flexibility.
The exact build up of else can be read in the Language Specification file.
- Sequence Requirement: All instructions must be part of a sequence, enforcing a structured script format.
- Avoidance of "Seq" Keyword: PyTerpreter determines sequence boundaries without relying on a dedicated "seq" keyword.
This is done in the PyTerpreterEnsure.Sequence methode by checking if all the entries in the list are 
of type list themselves.

### Environment Management
- Scope Management by Environments: Environments handle scopes and variable contexts for clean encapsulation.
Environments handle scopes and variable contexts for clean encapsulation.

- Dynamic Environment Handling: New environments are created with every sequence. 
They get systematically destroyed with each executed sequence.
This avoids memory leaks, improves performance because of smaller tress and makes the illegal to access.
- Automatic Environment Appending: Newly created environments automatically append themselves to the global tree.
- Environment Navigation via Previous and Next: "Previous" and "next" pointers navigate
efficiently through the environment tree.

### Execution and Integration
- Automatic Code Loading: Code is loaded automatically based on command-line arguments, parsed as JSON.
- Dynamic Execution Handling: The execute method dynamically handles sequences, operations, and values.
- Utilizing Python's Type Handling: Python's native type handling is leveraged for operations involving different types,
like list + list, true or dict, string == object, etc.

### Arrays
- Array is Fixed Size: Arrays in PyTerpreter have a fixed size.
- Array Access: Access arrays using special get and set functions along with an index.

### Dictionaries
- Access: Use special get and set functions along with a key to access dictionaries.
- Merge: Merge dictionaries with the second dictionary overriding existing keys in the first.

### Loops
- Implementation: Implements a "while" loop with a boolean condition and the possibility of infinite runtime.
- Repeat Loop: An additional repeat loop acts like a "for" loop, specifying how many times to repeat.

### Functions
- Definition: Defines functions, storing a copy of themselves, and calls execute on the copy.
All instructions must be sequences.
- Parameters: Parameters map one-to-one with argument call values.
- Setting Parameters: Parameters are set by inserting set operations at the beginning of a function.
- Return Keyword: Functions have an optional "return" keyword, ending function execution and passing
a value back to the call operation.
- Environment Closure: "Return" kills the function environment and all its children.

### Classes
- Inheritance as Entire Class Definition: Inheritance in PyTerpreter involves inheriting the entire class definition. This means that when a class inherits from another, it includes all the instructions, functions, and properties of the parent class.
- Instructions as Sequences of Sets: Classes in PyTerpreter consist of instructions, which are sequences of sets. These sets define the behavior of the class, including variable assignments, operations, and control flow.
- Utilizing Inheritance for Function Fetching: Inheritance allows classes to fetch overwritten functions from their parent classes. This ensures that the class hierarchy is respected, and overridden functions can be accessed when needed.
- Merging and Overwriting Cached Instructions: When a class inherits from another, the instructions of both classes are merged. If there are overlapping instructions, the ones in the inheriting class overwrite those in the parent class. This ensures that the most specific instructions are used.
- Handling Multiple Same Name Inheritance: In cases where a class inherits from multiple classes with the same function name, the oldest class in the inheritance chain takes precedence. This ensures a predictable order of function resolution.
- Constructor Function: Each class may have a constructor function, which is called with parameters when an object of that class is created. This function initializes the object's state and performs any necessary setup.

### Objects
- Instantiation of Class Definition: Objects instantiate a class definition with arguments provided for the constructor. This allows for customization of object properties and initial states.
- Accessing Objects via ObjectGet and ObjectSet: Objects are accessed using special functions, namely objectget and objectset. These functions allow for getting and setting properties of the object, respectively.
- Automatic Injection for Function Calls: To call object functions, the object instance injects itself automatically into the function in the background. This is achieved using the mount command, which links the object via its ID. The injected parameter ensures that the object's context is available within the function.
- Interaction with Object Functions: Objects can interact with functions defined in their class, utilizing the injected parameter. This allows objects to perform actions, modify internal states, and execute class-defined logic.
- Function Execution in the Object Context: When a function is executed within an object context, it operates on the specific instance of the class, enabling the use of instance-specific data and behavior.

### Tracing
- Definition: Tracing is done by the class PyTerpreterTrace
- Decorator:  The trace decorator accesses the interpreter via de args and executes the tracing in the tracing class.
- Return Value: It is important to return the return value of the call function in the decorator after the tracing is done else none gets returned.
- Tracking: A list in the form of [id, functionName, start or end, and timestamp] gets appended to a list of traced functions once before and once after the function call is called. If the function is anonymous it gets logged with brackets. The same happens with inherited functions.
- Logging: when the run is finished and tracing is wanted (--trace filename.log is written in the commandline) all the traced functions get written to a file one by one in RSV format ready for reporting.

### Reporting
- Initialization: The whole file gets executed through the init of the TraceReporter.
- Dynamic Padding: The padding for the function name gets dynamically adapted to the longest function name, ensuring
 clean display of data.
- ID is dictionary key with a dictionary as its value.
 The inner dictionary holds the data for calls, total time and start time. This is to separate ID from function name.

## How to Use PyTerpreter:

1. Installation: PyTerpreter is a single Python source file that can be included in your project by
checking out the source file. Additionally, a "reporting.py" file is provided for an easy-to-read reporting analysis.
2. Writing Scripts: To write scripts, follow a structured format using sequences.
The various commands like "print," "set," and "if" and how to use them are found in the
language specification file. Group operations logically and keep them within sequences for organized scripting.
3. Executing Scripts: Execute scripts by running the interpreter with the desired script file. Example, 
python PyTerpreter.py exampleFile.gsc
</br> Additionally, add --trace traceFile.log to save a trace file in the after named log file.
4. Reporting: Trace files can be displayed in a more readable way through the "reporting.py" file. Example,
python reporting.py traceFile.log

> For detailed usage explanation of the language, please see the "Language Specification" file.

Example Script:
    Here's an example script showcasing various functionalities of the PyTerpreter Language:
```
[
    ["print", "Hello, PyTerpreter!"],
    ["set", "a", 2],
    ["set", "b", ["add", 3, 4]],
    ["set", "result", ["add", ["get", "a"], ["get", "b"]]],
    ["print", ["get", "result"]],
    ["if", ["greater", ["get", "result"], 5], [
        ["print", "Result is greater than 5!"]
    ], [
        ["print", "Result is 5 or less."]
    ]]
]
```
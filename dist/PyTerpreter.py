from __future__ import annotations
import json
import sys

Illegal = "illegal"


class PyTerpreterEnsure:
    @staticmethod
    def Ensure(condition: bool, message: str) -> None:
        if not condition:
            raise SystemExit(f"PyTerpreter: {message}")

    @staticmethod
    def NotIllegal(value: any) -> None:
        PyTerpreterEnsure.Ensure(value != Illegal, "Illegal value occurred.")

    @staticmethod
    def Length(value: any, should: any) -> int:
        actual: int = len(value)
        if type(should) is tuple:
            PyTerpreterEnsure.Ensure(
                any(actual == possibility for possibility in should),
                f"Invalid length occurred ({actual} -> {should})",
            )
        else:
            PyTerpreterEnsure.Ensure(
                actual == should, f"Invalid length occurred ({actual} -> {should})."
            )
        return actual

    @staticmethod
    def Type(value: any, should: any) -> None:
        actual: any = type(value)
        if type(should) is tuple:
            possibilities: list[str] = [possibility.__name__ for possibility in should]
            return PyTerpreterEnsure.Ensure(
                any(actual == possibility for possibility in should),
                f"Invalid type occurred ({type(value).__name__} -> {possibilities}).",
            )
        PyTerpreterEnsure.Ensure(
            actual == should,
            f"Invalid type occurred ({type(value).__name__} -> {should.__name__}).",
        )

    @staticmethod
    def Sequence(value: any) -> None:
        PyTerpreterEnsure.Type(value, list)
        [PyTerpreterEnsure.Type(element, list) for element in value]

    @staticmethod
    def Includes(value: any, multi: any) -> None:
        PyTerpreterEnsure.Ensure(
            value in multi, f"Non-existent property occurred ({value} -> {multi})."
        )

    @staticmethod
    def Usage(environment: PyTerpreterEnvironment, value: str) -> None:
        PyTerpreterEnsure.Ensure(
            environment.usage == value,
            f"Illegal environment usage occurred ({value} -> {environment.usage}).",
        )


class PyTerpreterVariable:
    @staticmethod
    def Set(interpreter: PyTerpreter, args: list) -> Illegal:
        PyTerpreterEnsure.Length(args, 2)
        name: str = args[0]
        PyTerpreterEnsure.Type(name, str)
        PyTerpreterEnsure.NotIllegal(name)
        value: any = interpreter.execute(args[1])
        PyTerpreterEnsure.NotIllegal(value)
        return PyTerpreterVariable.__StoreDownwards(
            name, value, interpreter.environment
        )

    @staticmethod
    def __StoreDownwards(name: str, value: any, top: PyTerpreterEnvironment) -> Illegal:
        if top.exists(name) or top.next is None:
            top.store(name, value)
            return Illegal
        return PyTerpreterVariable.__StoreDownwards(name, value, top.next)

    @staticmethod
    def Get(interpreter: PyTerpreter, args: list) -> any:
        PyTerpreterEnsure.Length(args, 1)
        name: str = args[0]
        PyTerpreterEnsure.Type(name, str)
        PyTerpreterEnsure.NotIllegal(name)
        return PyTerpreterVariable.__RetrieveUpwards(
            name, interpreter.environment.lowest()
        )

    @staticmethod
    def __RetrieveUpwards(name: str, bottom: PyTerpreterEnvironment) -> any:
        if bottom.exists(name) or bottom.previous is None:
            return bottom.retrieve(name)
        return PyTerpreterVariable.__RetrieveUpwards(name, bottom.previous)

    Operations: dict = {
        "set": Set,
        "get": Get,
    }


class PyTerpreterMath:
    @staticmethod
    def Add(interpreter: PyTerpreter, args: list) -> any:
        PyTerpreterEnsure.Length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterEnsure.NotIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterEnsure.NotIllegal(b)
        return a + b

    @staticmethod
    def Subtract(interpreter: PyTerpreter, args: list) -> any:
        PyTerpreterEnsure.Length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterEnsure.NotIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterEnsure.NotIllegal(b)
        return a - b

    @staticmethod
    def Multiply(interpreter: PyTerpreter, args: list) -> any:
        PyTerpreterEnsure.Length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterEnsure.NotIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterEnsure.NotIllegal(b)
        return a * b

    @staticmethod
    def Divide(interpreter: PyTerpreter, args: list) -> any:
        PyTerpreterEnsure.Length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterEnsure.NotIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterEnsure.NotIllegal(b)
        return a / b

    @staticmethod
    def Power(interpreter: PyTerpreter, args: list) -> any:
        PyTerpreterEnsure.Length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterEnsure.NotIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterEnsure.NotIllegal(b)
        return a**b

    @staticmethod
    def Absolute(interpreter: PyTerpreter, args: list) -> any:
        PyTerpreterEnsure.Length(args, 1)
        a: any = interpreter.execute(args[0])
        PyTerpreterEnsure.NotIllegal(a)
        return abs(a)

    Operations: dict = {
        "add": Add,
        "subtract": Subtract,
        "absolute": Absolute,
        "multiply": Multiply,
        "divide": Divide,
        "power": Power,
    }


class PyTerpreterSystem:
    @staticmethod
    def Print(interpreter: PyTerpreter, args: list) -> Illegal:
        PyTerpreterEnsure.Length(args, 1)
        value: any = interpreter.execute(args[0])
        PyTerpreterEnsure.NotIllegal(value)
        print(value)
        return Illegal

    Operations: dict = {
        "print": Print,
    }


class PyTerpreterBoolean:
    @staticmethod
    def And(interpreter: PyTerpreter, args: list) -> bool:
        PyTerpreterEnsure.Length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterEnsure.NotIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterEnsure.NotIllegal(b)
        return a and b

    @staticmethod
    def Or(interpreter: PyTerpreter, args: list) -> bool:
        PyTerpreterEnsure.Length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterEnsure.NotIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterEnsure.NotIllegal(b)
        return a or b

    @staticmethod
    def Not(interpreter: PyTerpreter, args: list) -> bool:
        PyTerpreterEnsure.Length(args, 1)
        a: any = interpreter.execute(args[0])
        PyTerpreterEnsure.NotIllegal(a)
        return not a

    @staticmethod
    def Equal(interpreter: PyTerpreter, args: list) -> bool:
        PyTerpreterEnsure.Length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterEnsure.NotIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterEnsure.NotIllegal(b)
        return a == b

    @staticmethod
    def Less(interpreter: PyTerpreter, args: list) -> bool:
        PyTerpreterEnsure.Length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterEnsure.NotIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterEnsure.NotIllegal(b)
        return a < b

    @staticmethod
    def Greater(interpreter: PyTerpreter, args: list) -> bool:
        PyTerpreterEnsure.Length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterEnsure.NotIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterEnsure.NotIllegal(b)
        return a > b

    @staticmethod
    def LessEqual(interpreter: PyTerpreter, args: list) -> bool:
        PyTerpreterEnsure.Length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterEnsure.NotIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterEnsure.NotIllegal(b)
        return a <= b

    @staticmethod
    def GreaterEqual(interpreter: PyTerpreter, args: list) -> bool:
        PyTerpreterEnsure.Length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterEnsure.NotIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterEnsure.NotIllegal(b)
        return a >= b

    Operations: dict = {
        "and": And,
        "or": Or,
        "not": Not,
        "equal": Equal,
        "less": Less,
        "greater": Greater,
        "lessEqual": LessEqual,
        "greaterEqual": GreaterEqual,
    }


class PyTerpreterConditional:
    @staticmethod
    def If(interpreter: PyTerpreter, args: list) -> Illegal:
        length: int = PyTerpreterEnsure.Length(args, (2, 3))
        condition: any = interpreter.execute(args[0])
        PyTerpreterEnsure.NotIllegal(condition)
        program: any = None
        if condition:
            program = args[1]
        elif length == 3:
            program = args[2]
        if program is not None:
            PyTerpreterEnsure.Sequence(program)
            interpreter.execute(program, "if")
        return Illegal

    Operations: dict = {"if": If}


class PyterpreterDictionary:
    @staticmethod
    def Dictionary(interpreter: PyTerpreter, args: list) -> dict:
        PyTerpreterEnsure.Length(args, 0)
        return {}

    @staticmethod
    def DictionarySet(interpreter: PyTerpreter, args: list) -> "Illegal":
        PyTerpreterEnsure.Length(args, 3)
        dictionary: dict = interpreter.execute(args[0])
        PyTerpreterEnsure.Type(dictionary, dict)
        key: any = interpreter.execute(args[1])
        PyTerpreterEnsure.NotIllegal(key)
        value: any = interpreter.execute(args[2])
        PyTerpreterEnsure.NotIllegal(value)
        dictionary[key] = value
        return Illegal

    @staticmethod
    def DictionaryGet(interpreter: PyTerpreter, args: list) -> any:
        PyTerpreterEnsure.Length(args, 2)
        dictionary: dict = interpreter.execute(args[0])
        PyTerpreterEnsure.Type(dictionary, dict)
        key: any = interpreter.execute(args[1])
        PyTerpreterEnsure.NotIllegal(key)
        return dictionary.get(key, None)  # Returns None if key not found

    @staticmethod
    def DictionaryMerge(interpreter: PyTerpreter, args: list) -> dict:
        PyTerpreterEnsure.Length(args, 2)
        dict1: dict = interpreter.execute(args[0])
        PyTerpreterEnsure.Type(dict1, dict)
        dict2: dict = interpreter.execute(args[1])
        PyTerpreterEnsure.Type(dict2, dict)
        return {**dict1, **dict2}

    Operations: dict = {
        "dictionary": Dictionary,
        "dictionarySet": DictionarySet,
        "dictionaryGet": DictionaryGet,
        "dictionaryMerge": DictionaryMerge,
    }


class PyTerpreterArray:
    @staticmethod
    def Array(interpreter: PyTerpreter, args: list) -> list:
        PyTerpreterEnsure.Length(args, 1)
        size: int = interpreter.execute(args[0])
        PyTerpreterEnsure.Type(size, int)
        return [None] * size

    @staticmethod
    def ArraySet(interpreter: PyTerpreter, args: list) -> "Illegal":
        PyTerpreterEnsure.Length(args, 3)
        array: list = interpreter.execute(args[0])
        PyTerpreterEnsure.Type(array, list)
        index: int = interpreter.execute(args[1])
        PyTerpreterEnsure.Type(index, int)
        value: any = interpreter.execute(args[2])
        PyTerpreterEnsure.NotIllegal(value)
        array[index] = value
        return Illegal

    @staticmethod
    def ArrayGet(interpreter: PyTerpreter, args: list) -> any:
        PyTerpreterEnsure.Length(args, 2)
        array: list = interpreter.execute(args[0])
        PyTerpreterEnsure.Type(array, list)
        index: int = interpreter.execute(args[1])
        PyTerpreterEnsure.Type(index, int)
        return array[index]

    Operations: dict = {
        "array": Array,
        "arraySet": ArraySet,
        "arrayGet": ArrayGet,
    }


class PyTerpreterLoop:
    @staticmethod
    def While(interpreter: PyTerpreter, args: list) -> Illegal:
        PyTerpreterEnsure.Length(args, 2)
        program: any = args[1]
        PyTerpreterEnsure.Sequence(program)
        while PyTerpreterLoop.__Condition(interpreter, args[0]):
            if interpreter.environment.lowest().kill:
                break
            interpreter.execute(program, "while")
        return Illegal

    @staticmethod
    def __Condition(interpreter: PyTerpreter, arg: any) -> any:
        condition: any = interpreter.execute(arg)
        PyTerpreterEnsure.NotIllegal(condition)
        return condition

    @staticmethod
    def Repeat(interpreter: PyTerpreter, args: list) -> Illegal:
        PyTerpreterEnsure.Length(args, 2)
        count: int = args[0]
        PyTerpreterEnsure.Type(count, int)
        program: any = args[1]
        PyTerpreterEnsure.Sequence(program)
        for _ in range(count):
            if interpreter.environment.lowest().kill:
                break
            interpreter.execute(program, "repeat")
        return Illegal

    Operations: dict = {"while": While, "repeat": Repeat}


class PyTerpreterFunction:
    @staticmethod
    def Function(interpreter: PyTerpreter, args: list) -> list:
        PyTerpreterEnsure.Length(args, 2)
        parameters: list[str] = args[0]
        PyTerpreterEnsure.Type(parameters, list)
        [PyTerpreterEnsure.Type(parameter, str) for parameter in parameters]
        program: list = args[1]
        PyTerpreterEnsure.Sequence(program)
        return ["function", parameters, program]

    @staticmethod
    def Call(interpreter: PyTerpreter, args: list) -> any:
        PyTerpreterEnsure.Length(args, 2)
        function: any = interpreter.execute(args[0])
        PyTerpreterEnsure.Type(function, list)
        PyTerpreterEnsure.Ensure(
            function[0] == "function", "Illegal call of a non-function."
        )
        arguments: list = args[1]
        PyTerpreterEnsure.Type(arguments, list)
        PyTerpreterEnsure.Ensure(
            len(arguments) == len(function[1]), "Illegal function argument missmatch."
        )
        parameters: list[str] = function[1]
        program: list = function[2]
        for i in range(len(parameters)):
            value: any = interpreter.execute(arguments[i])
            operation: list = ["set", parameters[i], value]
            program.insert(0, operation)
        return interpreter.execute(program, "function")

    @staticmethod
    def Return(interpreter: PyTerpreter, args: list) -> Illegal:
        environment: PyTerpreterEnvironment = (
            PyTerpreterFunction.__FetchFunctionEnvironment(
                interpreter.environment.lowest()
            )
        )
        PyTerpreterEnsure.Length(args, 1)
        value: any = interpreter.execute(args[0])
        PyTerpreterEnsure.NotIllegal(value)
        environment.store("return", value)
        environment.determinate()

    @staticmethod
    def __FetchFunctionEnvironment(
        environment: PyTerpreterEnvironment,
    ) -> PyTerpreterEnvironment:
        if environment.usage == "function":
            return environment
        PyTerpreterEnsure.Ensure(
            environment.previous is not None, f"Illegal use of return outside function."
        )
        return PyTerpreterFunction.__FetchFunctionEnvironment(environment.previous)

    Operations: dict = {"function": Function, "call": Call, "return": Return}


class PyTerpreterEnvironment:
    def __init__(
        self, usage: str, previous: PyTerpreterEnvironment | None = None
    ) -> None:
        self.__usage: str = usage
        self.__previous: PyTerpreterEnvironment | None = None
        self.__next: PyTerpreterEnvironment | None = None
        self.__fields: dict = {}
        self.__kill: bool = False
        self.__isDestroyed: bool = False
        self.__insertIntoTree(previous)

    @property
    def usage(self) -> str:
        return self.__usage

    @property
    def previous(self) -> PyTerpreterEnvironment | None:
        return self.__previous

    @property
    def next(self) -> PyTerpreterEnvironment | None:
        return self.__next

    @property
    def kill(self) -> bool:
        return self.__kill

    def setPrevious(self, previous: PyTerpreterEnvironment | None) -> None:
        self.__previous = previous

    def setNext(self, next: PyTerpreterEnvironment | None) -> None:
        self.__next = next

    def __insertIntoTree(self, previous: PyTerpreterEnvironment | None):
        self.setPrevious(previous)
        self.setNext(None)
        if self.previous is None:
            return
        PyTerpreterEnsure.Ensure(
            self.previous.next is None,
            "Illegal environment tree insertion.",
        )
        self.previous.setNext(self)

    def lowest(self) -> PyTerpreterEnvironment:
        self.__notDestroyed()
        if self.next is None:
            return self
        return self.next.lowest()

    def store(self, name: str, value: any) -> None:
        self.__notDestroyed()
        PyTerpreterEnsure.Type(name, str)
        PyTerpreterEnsure.NotIllegal(name)
        PyTerpreterEnsure.NotIllegal(value)
        self.__fields[name] = value

    def exists(self, name: str) -> bool:
        self.__notDestroyed()
        PyTerpreterEnsure.Type(name, str)
        PyTerpreterEnsure.NotIllegal(name)
        return name in self.__fields

    def retrieve(self, name: str) -> any:
        self.__notDestroyed()
        PyTerpreterEnsure.Type(name, str)
        PyTerpreterEnsure.NotIllegal(name)
        PyTerpreterEnsure.Includes(name, self.__fields)
        return self.__fields[name]

    def determinate(self) -> None:
        self.__notDestroyed()
        self.__kill = True
        if self.next is not None:
            self.next.determinate()

    def destroy(self) -> None:
        self.__notDestroyed()
        self.__isDestroyed = True
        self.__kill = True
        self.__removeFromTree()
        self.__fields.clear()

    def __removeFromTree(self):
        PyTerpreterEnsure.Ensure(
            self.next is None,
            "Illegal environment tree removal.",
        )
        self.previous.setNext(None)
        self.setPrevious(None)

    def __notDestroyed(self) -> None:
        PyTerpreterEnsure.Ensure(
            not self.__isDestroyed, "Illegal use of destroyed environment."
        )


class PyTerpreter:
    def __init__(self, cliArgs: list[str]) -> None:
        self.environment: PyTerpreterEnvironment = PyTerpreterEnvironment("global")
        self.__operations: dict = {
            **PyTerpreterVariable.Operations,
            **PyTerpreterMath.Operations,
            **PyTerpreterSystem.Operations,
            **PyTerpreterBoolean.Operations,
            **PyTerpreterConditional.Operations,
            **PyterpreterDictionary.Operations,
            **PyTerpreterArray.Operations,
            **PyTerpreterLoop.Operations,
            **PyTerpreterFunction.Operations,
        }
        self.execute(self.__load(cliArgs))

    def __load(self, cliArgs: list[str]) -> any:
        PyTerpreterEnsure.Length(cliArgs, 2)
        with open(sys.argv[1], "r") as reader:
            return json.load(reader)

    def execute(self, program: any, usage: str | None = None) -> any:
        PyTerpreterEnsure.NotIllegal(program)
        if isinstance(program, list):
            if isinstance(program[0], list):
                return self.__executeSequence(program, usage)
            else:
                return self.__executeOperation(program)
        else:
            return program

    def __executeSequence(self, sequence: list, usage: str | None) -> any:
        PyTerpreterEnsure.Sequence(sequence)
        above: PyTerpreterEnvironment = self.environment.lowest()
        environment: PyTerpreterEnvironment = PyTerpreterEnvironment(
            usage or "sequence", above
        )
        for program in sequence:
            if environment.kill:
                break
            self.execute(program)
        returnValue: any = None
        if usage == "function" and environment.exists("return"):
            returnValue = environment.retrieve("return")
        environment.destroy()
        return returnValue

    def __executeOperation(self, program: list) -> any:
        operator: str = program[0]
        PyTerpreterEnsure.Type(operator, str)
        PyTerpreterEnsure.Includes(operator, self.__operations)
        return self.__operations[operator](self, program[1:])


if __name__ == "__main__":
    PyTerpreter(sys.argv)

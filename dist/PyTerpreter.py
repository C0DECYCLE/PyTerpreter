from __future__ import annotations
import json
import sys

Illegal = "illegal"


class PyTerpreterUtils:
    @staticmethod
    def Ensure(condition: bool, message: str) -> None:
        if not condition:
            raise SystemExit(f"PyTerpreter: {message}")

    @staticmethod
    def NotIllegal(value: any) -> None:
        PyTerpreterUtils.Ensure(value != Illegal, "Illegal value occurred.")

    @staticmethod
    def Length(value: any, should: any) -> None:
        actual: int = len(value)
        if type(should) is tuple:
            PyTerpreterUtils.Ensure(
                any(actual == possibility for possibility in should),
                f"Invalid length occurred ({actual} -> {should})",
            )
            return actual
        PyTerpreterUtils.Ensure(
            actual == should, f"Invalid length occurred ({actual} -> {should})."
        )

    @staticmethod
    def Type(value: any, should: any) -> None:
        actual: any = type(value)
        if type(should) is tuple:
            possibilities: list[str] = [possibility.__name__ for possibility in should]
            return PyTerpreterUtils.Ensure(
                any(actual == possibility for possibility in should),
                f"Invalid type occurred ({type(value).__name__} -> {possibilities}).",
            )
        PyTerpreterUtils.Ensure(
            actual == should,
            f"Invalid type occurred ({type(value).__name__} -> {should.__name__}).",
        )

    @staticmethod
    def Sequence(value: any) -> None:
        PyTerpreterUtils.Ensure(
            type(value) is list and type(value[0]) is list,
            f"No sequence where a sequence has to be",
        )

    @staticmethod
    def Includes(value: any, multi: any) -> None:
        PyTerpreterUtils.Ensure(
            value in multi, f"Non-existent property occurred ({value} -> {multi})."
        )


class PyTerpreterVariable:
    @staticmethod
    def Set(interpreter: PyTerpreter, args: list) -> Illegal:
        PyTerpreterUtils.Length(args, 2)
        name: str = args[0]
        PyTerpreterUtils.Type(name, str)
        PyTerpreterUtils.NotIllegal(name)
        value: any = interpreter.execute(args[1])
        PyTerpreterUtils.NotIllegal(value)
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
        PyTerpreterUtils.Length(args, 1)
        name: str = args[0]
        PyTerpreterUtils.Type(name, str)
        PyTerpreterUtils.NotIllegal(name)
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
        PyTerpreterUtils.Length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterUtils.NotIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterUtils.NotIllegal(b)
        return a + b

    @staticmethod
    def Subtract(interpreter: PyTerpreter, args: list) -> any:
        PyTerpreterUtils.Length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterUtils.NotIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterUtils.NotIllegal(b)
        return a - b

    @staticmethod
    def Multiply(interpreter: PyTerpreter, args: list) -> any:
        PyTerpreterUtils.Length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterUtils.NotIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterUtils.NotIllegal(b)
        return a * b

    @staticmethod
    def Divide(interpreter: PyTerpreter, args: list) -> any:
        PyTerpreterUtils.Length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterUtils.NotIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterUtils.NotIllegal(b)
        return a / b

    @staticmethod
    def Power(interpreter: PyTerpreter, args: list) -> any:
        PyTerpreterUtils.Length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterUtils.NotIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterUtils.NotIllegal(b)
        return a**b

    @staticmethod
    def Absolute(interpreter: PyTerpreter, args: list) -> any:
        PyTerpreterUtils.Length(args, 1)
        a: any = interpreter.execute(args[0])
        PyTerpreterUtils.NotIllegal(a)
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
        PyTerpreterUtils.Length(args, 1)
        value: any = interpreter.execute(args[0])
        PyTerpreterUtils.NotIllegal(value)
        print(value)
        return Illegal

    Operations: dict = {
        "print": Print,
    }


class PyTerpreterBoolean:
    @staticmethod
    def And(interpreter: PyTerpreter, args: list) -> bool:
        PyTerpreterUtils.Length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterUtils.NotIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterUtils.NotIllegal(b)
        return a and b

    @staticmethod
    def Or(interpreter: PyTerpreter, args: list) -> bool:
        PyTerpreterUtils.Length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterUtils.NotIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterUtils.NotIllegal(b)
        return a or b

    @staticmethod
    def Not(interpreter: PyTerpreter, args: list) -> bool:
        PyTerpreterUtils.Length(args, 1)
        a: any = interpreter.execute(args[0])
        PyTerpreterUtils.NotIllegal(a)
        return not a

    @staticmethod
    def Equal(interpreter: PyTerpreter, args: list) -> bool:
        PyTerpreterUtils.Length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterUtils.NotIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterUtils.NotIllegal(b)
        return a == b

    @staticmethod
    def Less(interpreter: PyTerpreter, args: list) -> bool:
        PyTerpreterUtils.Length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterUtils.NotIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterUtils.NotIllegal(b)
        return a < b

    @staticmethod
    def Greater(interpreter: PyTerpreter, args: list) -> bool:
        PyTerpreterUtils.Length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterUtils.NotIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterUtils.NotIllegal(b)
        return a > b

    @staticmethod
    def LessEqual(interpreter: PyTerpreter, args: list) -> bool:
        PyTerpreterUtils.Length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterUtils.NotIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterUtils.NotIllegal(b)
        return a <= b

    @staticmethod
    def GreaterEqual(interpreter: PyTerpreter, args: list) -> bool:
        PyTerpreterUtils.Length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterUtils.NotIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterUtils.NotIllegal(b)
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
        length = PyTerpreterUtils.Length(args, (2, 3))
        b = args[0]
        PyTerpreterUtils.NotIllegal(b)
        b = interpreter.execute(b)
        if b:
            ifTrue = args[1]
            PyTerpreterUtils.NotIllegal(ifTrue)
            PyTerpreterUtils.Sequence(ifTrue)
            interpreter.execute(ifTrue)
        elif length == 3:
            ifFalse = args[2]
            PyTerpreterUtils.NotIllegal(ifFalse)
            PyTerpreterUtils.Sequence(ifFalse)
            interpreter.execute(ifFalse)

        return Illegal

    Operations: dict = {"if": If}


class PyTerpreterEnvironment:
    def __init__(
        self, usage: str, previous: PyTerpreterEnvironment | None = None
    ) -> None:
        self.__usage: str = usage
        self.__previous: PyTerpreterEnvironment | None = None
        self.__next: PyTerpreterEnvironment | None = None
        self.__fields: dict = {}
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

    def setPrevious(self, previous: PyTerpreterEnvironment | None) -> None:
        self.__previous = previous

    def setNext(self, next: PyTerpreterEnvironment | None) -> None:
        self.__next = next

    def __insertIntoTree(self, previous: PyTerpreterEnvironment | None):
        self.setPrevious(previous)
        self.setNext(None)
        if self.previous is None:
            return
        PyTerpreterUtils.Ensure(
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
        PyTerpreterUtils.Type(name, str)
        PyTerpreterUtils.NotIllegal(name)
        PyTerpreterUtils.NotIllegal(value)
        self.__fields[name] = value

    def exists(self, name: str) -> bool:
        self.__notDestroyed()
        PyTerpreterUtils.Type(name, str)
        PyTerpreterUtils.NotIllegal(name)
        return name in self.__fields

    def retrieve(self, name: str) -> any:
        self.__notDestroyed()
        PyTerpreterUtils.Type(name, str)
        PyTerpreterUtils.NotIllegal(name)
        PyTerpreterUtils.Includes(name, self.__fields)
        return self.__fields[name]

    def destroy(self) -> None:
        self.__notDestroyed()
        self.__isDestroyed = True
        self.__removeFromTree()
        self.__fields.clear()

    def __removeFromTree(self):
        PyTerpreterUtils.Ensure(
            self.next is None,
            "Illegal environment tree removal.",
        )
        self.previous.setNext(None)
        self.setPrevious(None)

    def __notDestroyed(self) -> None:
        PyTerpreterUtils.Ensure(
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
        }
        self.execute(self.__load(cliArgs))

    def __load(self, cliArgs: list[str]) -> any:
        PyTerpreterUtils.Length(cliArgs, 2)
        with open(sys.argv[1], "r") as reader:
            return json.load(reader)

    def execute(self, program: any) -> any:
        PyTerpreterUtils.NotIllegal(program)
        if isinstance(program, list):
            if isinstance(program[0], list):
                self.__executeSequence(program)
            else:
                return self.__executeOperation(program)
        else:
            return program

    def __executeSequence(self, sequence: list) -> None:
        above: PyTerpreterEnvironment = self.environment.lowest()
        environment: PyTerpreterEnvironment = PyTerpreterEnvironment("sequence", above)
        for program in sequence:
            self.execute(program)
        environment.destroy()

    def __executeOperation(self, program: list) -> any:
        operator: str = program[0]
        PyTerpreterUtils.Type(operator, str)
        PyTerpreterUtils.Includes(operator, self.__operations)
        return self.__operations[operator](self, program[1:])


if __name__ == "__main__":
    PyTerpreter(sys.argv)

from __future__ import annotations
import json
import sys

Illegal = "illegal"


class PyTerpreterUtils:
    @staticmethod
    def ensure(condition: bool, message: str) -> None:
        if not condition:
            raise SystemExit(f"PyTerpreter: {message}")

    @staticmethod
    def notIllegal(value: any) -> None:
        PyTerpreterUtils.ensure(value != Illegal, "Illegal value occurred.")

    @staticmethod
    def length(value: any, should: int) -> None:
        actual: int = len(value)
        PyTerpreterUtils.ensure(
            actual == should, f"Invalid length occurred ({actual} -> {should})."
        )

    @staticmethod
    def type(value: any, should: any) -> None:
        actual: any = type(value)
        if type(should) is tuple:
            possibilities: list[str] = [possibility.__name__ for possibility in should]
            return PyTerpreterUtils.ensure(
                any([actual == possibility for possibility in should]),
                f"Invalid type occurred ({type(value).__name__} -> {possibilities}).",
            )
        PyTerpreterUtils.ensure(
            actual == should,
            f"Invalid type occurred ({type(value).__name__} -> {should.__name__}).",
        )

    @staticmethod
    def includes(value: any, multi: any) -> None:
        PyTerpreterUtils.ensure(
            value in multi, f"Non-existent property occurred ({value} -> {multi})."
        )


class PyTerpreterVariable:
    @staticmethod
    def set(interpreter: PyTerpreter, args: list) -> Illegal:
        PyTerpreterUtils.length(args, 2)
        name: str = args[0]
        PyTerpreterUtils.type(name, str)
        PyTerpreterUtils.notIllegal(name)
        value: any = interpreter.execute(args[1])
        PyTerpreterUtils.notIllegal(value)
        return PyTerpreterVariable.__storeDownwards(
            name, value, interpreter.environment
        )

    @staticmethod
    def __storeDownwards(name: str, value: any, top: PyTerpreterEnvironment) -> Illegal:
        if top.exists(name) or top.next is None:
            top.store(name, value)
            return Illegal
        return PyTerpreterVariable.__storeDownwards(name, value, top.next)

    @staticmethod
    def get(interpreter: PyTerpreter, args: list) -> any:
        PyTerpreterUtils.length(args, 1)
        name: str = args[0]
        PyTerpreterUtils.type(name, str)
        PyTerpreterUtils.notIllegal(name)
        return PyTerpreterVariable.__retrieveUpwards(
            name, interpreter.environment.lowest()
        )

    @staticmethod
    def __retrieveUpwards(name: str, bottom: PyTerpreterEnvironment) -> any:
        if bottom.exists(name) or bottom.previous is None:
            return bottom.retrieve(name)
        return PyTerpreterVariable.__retrieveUpwards(name, bottom.previous)


class PyTerpreterMath:
    @staticmethod
    def add(interpreter: PyTerpreter, args: list) -> any:
        PyTerpreterUtils.length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterUtils.notIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterUtils.notIllegal(b)
        return a + b


class PyTerpreterSystem:
    @staticmethod
    def print(interpreter: PyTerpreter, args: list) -> Illegal:
        PyTerpreterUtils.length(args, 1)
        value: any = interpreter.execute(args[0])
        PyTerpreterUtils.notIllegal(value)
        print(value)
        return Illegal

class PyTerpreterBoolean:
    @staticmethod
    def boolAnd(interpreter: PyTerpreter, args: list) -> bool:
        PyTerpreterUtils.length(args, 2)
        a: bool = interpreter.execute(args[0])
        PyTerpreterUtils.notIllegal(a)
        PyTerpreterUtils.type(a, bool)
        b: bool = interpreter.execute(args[1])
        PyTerpreterUtils.notIllegal(b)
        PyTerpreterUtils.type(b, bool)
        return a and b

    @staticmethod
    def boolOr(interpreter: PyTerpreter, args: list) -> bool:
        PyTerpreterUtils.length(args, 2)
        a: bool = interpreter.execute(args[0])
        PyTerpreterUtils.notIllegal(a)
        PyTerpreterUtils.type(a, bool)
        b: bool = interpreter.execute(args[1])
        PyTerpreterUtils.notIllegal(b)
        PyTerpreterUtils.type(b, bool)
        return a or b

    @staticmethod
    def boolNot(interpreter: PyTerpreter, args: list) -> bool:
        PyTerpreterUtils.length(args, 1)
        a: bool = interpreter.execute(args[0])
        PyTerpreterUtils.notIllegal(a)
        PyTerpreterUtils.type(a, bool)
        return not a

    @staticmethod
    def boolEqual(interpreter: PyTerpreter, args: list) -> bool:
        PyTerpreterUtils.length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterUtils.notIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterUtils.notIllegal(b)
        return a == b

    @staticmethod
    def boolLess(interpreter: PyTerpreter, args: list) -> bool:
        PyTerpreterUtils.length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterUtils.notIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterUtils.notIllegal(b)
        return a < b

    @staticmethod
    def boolGreater(interpreter: PyTerpreter, args: list) -> bool:
        PyTerpreterUtils.length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterUtils.notIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterUtils.notIllegal(b)
        return a > b

    @staticmethod
    def boolLessEqual(interpreter: PyTerpreter, args: list) -> bool:
        PyTerpreterUtils.length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterUtils.notIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterUtils.notIllegal(b)
        return a <= b

    @staticmethod
    def boolGreaterEqual(interpreter: PyTerpreter, args: list) -> bool:
        PyTerpreterUtils.length(args, 2)
        a: any = interpreter.execute(args[0])
        PyTerpreterUtils.notIllegal(a)
        b: any = interpreter.execute(args[1])
        PyTerpreterUtils.notIllegal(b)
        return a >= b

class PyTerpreterEnvironment:
    def __init__(
        self, usage: str, previous: PyTerpreterEnvironment | None = None
    ) -> None:
        self.__usage: str = usage
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

    def setPrevious(self, previous: PyTerpreterVariable | None) -> None:
        self.__previous = previous

    def setNext(self, next: PyTerpreterVariable | None) -> None:
        self.__next = next

    def __insertIntoTree(self, previous: PyTerpreterEnvironment | None):
        self.setPrevious(previous)
        self.setNext(None)
        if self.previous is None:
            return
        PyTerpreterUtils.ensure(
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
        PyTerpreterUtils.type(name, str)
        PyTerpreterUtils.notIllegal(name)
        PyTerpreterUtils.notIllegal(value)
        self.__fields[name] = value

    def exists(self, name: str) -> bool:
        self.__notDestroyed()
        PyTerpreterUtils.type(name, str)
        PyTerpreterUtils.notIllegal(name)
        return name in self.__fields

    def retrieve(self, name: str) -> any:
        self.__notDestroyed()
        PyTerpreterUtils.type(name, str)
        PyTerpreterUtils.notIllegal(name)
        PyTerpreterUtils.includes(name, self.__fields)
        return self.__fields[name]

    def destroy(self) -> None:
        self.__notDestroyed()
        self.__isDestroyed = True
        self.__removeFromTree()
        self.__fields.clear()

    def __removeFromTree(self):
        PyTerpreterUtils.ensure(
            self.next is None,
            "Illegal environment tree removal.",
        )
        self.previous.setNext(None)
        self.setPrevious(None)

    def __notDestroyed(self) -> None:
        PyTerpreterUtils.ensure(
            not self.__isDestroyed, "Illegal use of destroyed environment."
        )


class PyTerpreter:
    def __init__(self, cliArgs: list[str]) -> None:
        self.environment: PyTerpreterEnvironment = PyTerpreterEnvironment("global")
        self.__operations: dict[str, callable] = {
            "set": PyTerpreterVariable.set,
            "get": PyTerpreterVariable.get,
            "add": PyTerpreterMath.add,
            "print": PyTerpreterSystem.print,
            "and": PyTerpreterBoolean.boolAnd,
            "or": PyTerpreterBoolean.boolOr,
            "not": PyTerpreterBoolean.boolNot,
            "equal": PyTerpreterBoolean.boolEqual,
            "less": PyTerpreterBoolean.boolLess,
            "greater": PyTerpreterBoolean.boolGreater,
            "lessEqual": PyTerpreterBoolean.boolLessEqual,
            "greaterEqual": PyTerpreterBoolean.boolGreaterEqual,
        }
        self.execute(self.__load(cliArgs))

    def __load(self, cliArgs: list[str]) -> any:
        PyTerpreterUtils.length(cliArgs, 2)
        with open(sys.argv[1], "r") as reader:
            return json.load(reader)

    def execute(self, program: any) -> any:
        PyTerpreterUtils.notIllegal(program)
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
        PyTerpreterUtils.type(operator, str)
        PyTerpreterUtils.includes(operator, self.__operations)
        return self.__operations[operator](self, program[1:])


if __name__ == "__main__":
    PyTerpreter(sys.argv)

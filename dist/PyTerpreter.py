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
    def length(value: any, length: int) -> None:
        actual: int = len(value)
        PyTerpreterUtils.ensure(
            actual == length, f"Invalid length occurred ({actual} -> {length})."
        )

    @staticmethod
    def type(value: any, should: any) -> None:
        actual: any = type(value)
        if type(should) is tuple:
            possibilities: list[str] = [possibility.__name__ for possibility in should]
            return PyTerpreterUtils.ensure(
                sum([1 if actual == possibility else 0 for possibility in should]) > 0,
                f"Invalid type occurred ({type(value).__name__} -> {possibilities}).",
            )
        PyTerpreterUtils.ensure(
            actual == should,
            f"Invalid type occurred ({type(value).__name__} -> {should.__name__}).",
        )

    @staticmethod
    def includes(value: any, multi: any) -> None:
        PyTerpreterUtils.ensure(
            value in multi, f"Nonexistent property occurred ({value} -> {multi})."
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
    def add(interpreter: PyTerpreter, args: list) -> int | float:
        PyTerpreterUtils.length(args, 2)
        a: int | float = interpreter.execute(args[0])
        PyTerpreterUtils.type(a, (int, float))
        b: int | float = interpreter.execute(args[1])
        PyTerpreterUtils.type(b, (int, float))
        return a + b


class PyTerpreterSystem:
    @staticmethod
    def print(interpreter: PyTerpreter, args: list) -> Illegal:
        PyTerpreterUtils.length(args, 1)
        value: any = interpreter.execute(args[0])
        PyTerpreterUtils.notIllegal(value)
        print(value)
        return Illegal


class PyTerpreterEnvironment:
    def __init__(
        self, usage: str, previous: PyTerpreterEnvironment | None = None
    ) -> None:
        self.__usage: str = usage
        self.__previous: PyTerpreterEnvironment | None = previous
        self.__next: PyTerpreterEnvironment | None = None
        self.__fields: dict = {}
        self.__isDestroyed: bool = False

    @property
    def usage(self) -> str:
        return self.__usage

    @property
    def previous(self) -> PyTerpreterEnvironment | None:
        return self.__previous

    def setPrevious(self, previous: PyTerpreterVariable | None) -> None:
        self.__previous = previous

    @property
    def next(self) -> PyTerpreterEnvironment | None:
        return self.__next

    def setNext(self, next: PyTerpreterVariable | None) -> None:
        self.__next = next

    def lowest(self) -> PyTerpreterEnvironment:
        self.__notDestroyed()
        if self.__next is None:
            return self
        return self.__next.lowest()

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
        self.__fields.clear()
        self.__next = None
        self.__previous = None

    def __notDestroyed(self) -> None:
        PyTerpreterUtils.ensure(
            not self.__isDestroyed, "Illegal use of destroyed environment."
        )


class PyTerpreter:
    def __init__(self, cliArgs: list[str]) -> None:
        self.environment: PyTerpreterEnvironment = PyTerpreterEnvironment("global")
        self.operations: dict[str, callable] = {
            "set": PyTerpreterVariable.set,
            "get": PyTerpreterVariable.get,
            "add": PyTerpreterMath.add,
            "print": PyTerpreterSystem.print,
        }
        self.execute(self.load(cliArgs))

    def load(self, cliArgs: list[str]) -> any:
        PyTerpreterUtils.length(cliArgs, 2)
        with open(sys.argv[1], "r") as reader:
            return json.load(reader)

    def execute(self, program: any) -> any:
        PyTerpreterUtils.notIllegal(program)
        if isinstance(program, list):
            if isinstance(program[0], list):
                self.executeSequence(program)
            else:
                return self.executeOperation(program)
        else:
            return program

    def executeSequence(self, sequence: list) -> None:
        above: PyTerpreterEnvironment = self.environment.lowest()
        environment: PyTerpreterEnvironment = PyTerpreterEnvironment("sequence", above)
        above.setNext(environment)
        for program in sequence:
            self.execute(program)
        above.setNext(None)
        environment.destroy()

    def executeOperation(self, program: list) -> any:
        operator: str = program[0]
        PyTerpreterUtils.type(operator, str)
        PyTerpreterUtils.includes(operator, self.operations)
        return self.operations[operator](self, program[1:])


if __name__ == "__main__":
    PyTerpreter(sys.argv)

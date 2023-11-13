from __future__ import annotations
import json
import sys
from copy import deepcopy
from uuid import uuid4

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

    @staticmethod
    def Operation(value: any, should: str) -> None:
        PyTerpreterEnsure.Type(value, list)
        actual: str = value[0]
        PyTerpreterEnsure.Type(actual, str)
        PyTerpreterEnsure.Ensure(
            actual == should, f"Illegal operation mismatch ({actual} -> {should})."
        )

    @staticmethod
    def Class(value: any) -> None:
        PyTerpreterEnsure.Sequence(value)
        [PyTerpreterEnsure.Operation(operation, "set") for operation in value]

    @staticmethod
    def Instance(value: any, should: any) -> None:
        PyTerpreterEnsure.Ensure(
            isinstance(value, should),
            f"Invalid type occurred ({type(value).__name__} -> {should.__name__}).",
        )


class PyTerpreterVariable:
    @staticmethod
    def Set(interpreter: PyTerpreter, args: list) -> Illegal:
        PyTerpreterEnsure.Length(args, 2)
        name: str = interpreter.execute(args[0])
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
        name: str = interpreter.execute(args[0])
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


class PyTerpreterDictionary:
    @staticmethod
    def Dictionary(interpreter: PyTerpreter, args: list) -> dict:
        PyTerpreterEnsure.Length(args, 0)
        return {}

    @staticmethod
    def DictionarySet(interpreter: PyTerpreter, args: list) -> Illegal:
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
    def ArraySet(interpreter: PyTerpreter, args: list) -> Illegal:
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
        function: list = deepcopy(interpreter.execute(args[0]))
        PyTerpreterEnsure.Operation(function, "function")
        arguments: list = args[1]
        PyTerpreterEnsure.Type(arguments, list)
        mountIndex, mount = PyTerpreterFunction.__FetchMount(interpreter, function[2])
        PyTerpreterFunction.__InjectArguments(
            interpreter, function, arguments, mountIndex
        )
        return interpreter.execute(function[2], "function", False, None, mount)

    @staticmethod
    def Mount(interpreter: PyTerpreter, args: list) -> Illegal:
        PyTerpreterEnsure.Length(args, 1)
        id: str = args[0]
        PyTerpreterEnsure.Type(id, str)
        PyTerpreterEnsure.NotIllegal(id)
        return Illegal

    @staticmethod
    def __FetchMount(
        interpreter: PyTerpreter, program: list
    ) -> tuple[int, PyTerpreterEnvironment | None]:
        mount: PyTerpreterEnvironment | None = None
        index: int | None = PyTerpreterFunction.__FetchMountIndex(program)
        if index is None:
            index = -1
        else:
            id: str = program[index][1]
            mount = PyTerpreterFunction.__FetchEnvironmentById(
                interpreter.environment, id
            )
        return index, mount

    @staticmethod
    def __FetchMountIndex(program: list) -> int | None:
        PyTerpreterEnsure.Sequence(program)
        for i in range(len(program)):
            operation: list = program[i]
            if operation[0] == "mount":
                return i
        return None

    @staticmethod
    def __FetchEnvironmentById(
        environment: PyTerpreterEnvironment, id: str
    ) -> PyTerpreterEnvironment | None:
        target: PyTerpreterEnvironment | None = environment.fetchById(id)
        if target is not None:
            return target
        if environment.next is not None:
            return PyTerpreterFunction.__FetchEnvironmentById(environment.next, id)
        return None

    @staticmethod
    def __InjectArguments(
        interpreter: PyTerpreter, function: list, arguments: list, mountIndex: int
    ) -> None:
        parameters: list[str] = function[1]
        PyTerpreterEnsure.Ensure(
            len(arguments) == len(parameters), "Illegal parameter argument missmatch."
        )
        program: list = function[2]
        for i in range(len(parameters)):
            value: any = interpreter.execute(arguments[i])
            operation: list = ["set", parameters[i], value]
            program.insert(mountIndex + 1, operation)

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
        environment.terminate()

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

    Operations: dict = {
        "function": Function,
        "call": Call,
        "mount": Mount,
        "return": Return,
    }


class PyTerpreterClass:
    @staticmethod
    def Class(interpreter: PyTerpreter, args: list) -> list:
        length: int = PyTerpreterEnsure.Length(args, (1, 2))
        program: list = args[-1]
        PyTerpreterEnsure.Class(program)
        if length == 2:
            ancestor: list = args[0]
            PyTerpreterEnsure.Type(ancestor, list)
            return ["class", ancestor, program]
        return ["class", program]

    @staticmethod
    def Inherit(interpreter: PyTerpreter, args: list) -> list:
        PyTerpreterEnsure.Length(args, 1)
        name: str = interpreter.execute(args[0])
        PyTerpreterEnsure.Type(name, str)
        PyTerpreterEnsure.NotIllegal(name)
        collisionCache: list | None = PyTerpreterClass.__RetrieveCacheUpwards(
            interpreter.environment.lowest()
        )
        PyTerpreterEnsure.Type(collisionCache, list)
        for item in collisionCache:
            if item[0] == name:
                return item[1]
        PyTerpreterEnsure.Ensure(
            False,
            f"Illegal inherit of unknown function name ({name} -> {collisionCache}).",
        )

    @staticmethod
    def __RetrieveCacheUpwards(environment: PyTerpreterEnvironment) -> list | None:
        if environment.cache is not None or environment.previous is None:
            return environment.cache
        return PyTerpreterClass.__RetrieveCacheUpwards(environment.previous)

    Operations: dict = {"class": Class, "inherit": Inherit}


class PyTerpreterObject:
    @staticmethod
    def Object(interpreter: PyTerpreter, args: list) -> PyTerpreterEnvironment:
        PyTerpreterEnsure.Length(args, 2)
        instantiate: list = interpreter.execute(args[0])
        PyTerpreterEnsure.Operation(instantiate, "class")
        program, collisionCache = PyTerpreterObject.__Inherit(interpreter, instantiate)
        PyTerpreterEnsure.Class(program)
        arguments: list = args[1]
        PyTerpreterEnsure.Type(arguments, list)
        environment: PyTerpreterEnvironment = interpreter.autoEnvironment("object")
        environment.setCache(collisionCache)
        PyTerpreterObject.__Mount(program, environment.id)
        interpreter.execute(program, "object", True, environment)
        # temporary save for mount of constructor to find object
        interpreter.environment.store(environment.id, environment)
        constructor: list | None = PyTerpreterObject.__GetConstructor(program)
        if constructor is not None:
            interpreter.execute(["call", constructor, arguments])
        interpreter.environment.delete(environment.id)
        return environment

    @staticmethod
    def __Inherit(interpreter: PyTerpreter, definition: list) -> tuple[list, list]:
        PyTerpreterEnsure.Operation(definition, "class")
        if len(definition) == 2:
            collisionCache: list = []
            return deepcopy(definition[1]), collisionCache
        ancestor: list = interpreter.execute(definition[1])
        return PyTerpreterObject.__MergeAncestor(
            PyTerpreterObject.__Inherit(interpreter, ancestor), deepcopy(definition[2])
        )

    @staticmethod
    def __MergeAncestor(
        ancestor: tuple[list, list], program: list
    ) -> tuple[list, list]:
        PyTerpreterEnsure.Class(program)
        ancestorProgram: list = ancestor[0]
        PyTerpreterEnsure.Class(ancestorProgram)
        result: list = program
        collisionCache: list = ancestor[1]
        ancestorProgram.reverse()
        for operation in ancestorProgram:
            name: str = operation[1]
            if PyTerpreterObject.__CollisionInClass(result, name):
                collisionCache.append((name, operation[2]))
                continue
            result.insert(0, operation)
        return result, collisionCache

    @staticmethod
    def __CollisionInClass(program: list, name: str) -> bool:
        PyTerpreterEnsure.Class(program)
        for operation in program:
            if (
                operation[1] == name
                and isinstance(operation[2], list)
                and operation[2][0] == "function"
            ):
                return True
        return False

    @staticmethod
    def __Mount(program: list, id: str) -> None:
        PyTerpreterEnsure.Class(program)
        for operation in program:
            value: any = operation[2]
            if isinstance(value, list) and value[0] == "function":
                function: list = value[2]
                function.insert(0, ["mount", id])

    @staticmethod
    def __GetConstructor(program: list) -> list | None:
        PyTerpreterEnsure.Class(program)
        constructor: list | None = None
        for operation in program:
            if operation[1] == "constructor":
                constructor = operation[2]
                PyTerpreterEnsure.Operation(constructor, "function")
        return constructor

    @staticmethod
    def ObjectSet(interpreter: PyTerpreter, args: list) -> Illegal:
        PyTerpreterEnsure.Length(args, 3)
        environment: PyTerpreterEnvironment = interpreter.execute(args[0])
        PyTerpreterEnsure.Instance(environment, PyTerpreterEnvironment)
        name: str = interpreter.execute(args[1])
        PyTerpreterEnsure.Type(name, str)
        PyTerpreterEnsure.NotIllegal(name)
        value: any = interpreter.execute(args[2])
        PyTerpreterEnsure.NotIllegal(value)
        environment.store(name, value)
        return Illegal

    @staticmethod
    def ObjectGet(interpreter: PyTerpreter, args: list) -> any:
        PyTerpreterEnsure.Length(args, 2)
        environment: PyTerpreterEnvironment = interpreter.execute(args[0])
        PyTerpreterEnsure.Instance(environment, PyTerpreterEnvironment)
        name: str = interpreter.execute(args[1])
        PyTerpreterEnsure.Type(name, str)
        PyTerpreterEnsure.NotIllegal(name)
        return environment.retrieve(name)

    Operations: dict = {
        "object": Object,
        "objectSet": ObjectSet,
        "objectGet": ObjectGet,
    }


class PyTerpreterEnvironment:
    def __init__(
        self, usage: str, previous: PyTerpreterEnvironment | None = None
    ) -> None:
        self.__id: str = str(uuid4())
        self.__usage: str = usage
        self.__previous: PyTerpreterEnvironment | None = None
        self.__next: PyTerpreterEnvironment | None = None
        self.__fields: dict = {}
        self.__cache: list | None = None
        self.__kill: bool = False
        self.__isDestroyed: bool = False
        self.attach(previous)

    @property
    def id(self) -> str:
        self.__notDestroyed()
        return self.__id

    @property
    def usage(self) -> str:
        self.__notDestroyed()
        return self.__usage

    @property
    def previous(self) -> PyTerpreterEnvironment | None:
        self.__notDestroyed()
        return self.__previous

    @property
    def next(self) -> PyTerpreterEnvironment | None:
        self.__notDestroyed()
        return self.__next

    @property
    def cache(self) -> list | None:
        self.__notDestroyed()
        return self.__cache

    @property
    def kill(self) -> bool:
        self.__notDestroyed()
        return self.__kill

    def setPrevious(self, previous: PyTerpreterEnvironment | None) -> None:
        self.__notDestroyed()
        self.__previous = previous

    def setNext(self, next: PyTerpreterEnvironment | None) -> None:
        self.__notDestroyed()
        self.__next = next

    def attach(self, previous: PyTerpreterEnvironment | None):
        self.__notDestroyed()
        self.setPrevious(previous)
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

    def delete(self, name: str) -> None:
        self.__notDestroyed()
        PyTerpreterEnsure.Type(name, str)
        PyTerpreterEnsure.NotIllegal(name)
        PyTerpreterEnsure.Includes(name, self.__fields)
        del self.__fields[name]

    def setCache(self, cache: list) -> None:
        self.__cache = cache

    def fetchById(self, id: str) -> PyTerpreterEnvironment | None:
        if self.id == id:
            return self
        for value in self.__fields.values():
            if isinstance(value, PyTerpreterEnvironment) and value.id == id:
                return value
        return None

    def detach(self) -> None:
        self.__notDestroyed()
        if self.previous is None:
            return
        self.previous.setNext(None)
        self.setPrevious(None)

    def terminate(self) -> None:
        self.__notDestroyed()
        self.__kill = True
        if self.next is not None:
            self.next.terminate()

    def destroy(self) -> None:
        self.__notDestroyed()
        self.detach()
        PyTerpreterEnsure.Ensure(
            self.next is None,
            "Illegal environment tree removal.",
        )
        # self.terminate()
        # if self.next is not None:
        #     self.next.destroy()
        self.__isDestroyed = True
        for value in self.__fields.values():
            if isinstance(value, PyTerpreterEnvironment):
                value.destroy()
        self.__fields.clear()

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
            **PyTerpreterDictionary.Operations,
            **PyTerpreterArray.Operations,
            **PyTerpreterLoop.Operations,
            **PyTerpreterFunction.Operations,
            **PyTerpreterClass.Operations,
            **PyTerpreterObject.Operations,
        }
        self.execute(self.__load(cliArgs))

    def __load(self, cliArgs: list[str]) -> any:
        PyTerpreterEnsure.Length(cliArgs, 2)
        with open(sys.argv[1], "r") as reader:
            return json.load(reader)

    def execute(
        self,
        program: any,
        usage: str | None = None,
        preserve: bool = False,
        environment: PyTerpreterEnvironment | None = None,
        mount: PyTerpreterEnvironment | None = None,
    ) -> any:
        PyTerpreterEnsure.NotIllegal(program)
        if isinstance(program, list):
            if isinstance(program[0], list):
                return self.__executeSequence(
                    program, usage, preserve, environment, mount
                )
            else:
                return self.__executeOperation(program)
        else:
            return program

    def autoEnvironment(self, usage: str | None) -> PyTerpreterEnvironment:
        return PyTerpreterEnvironment(usage or "sequence", self.environment.lowest())

    def __executeSequence(
        self,
        sequence: list,
        usage: str | None,
        preserve: bool,
        target: PyTerpreterEnvironment | None,
        mount: PyTerpreterEnvironment | None,
    ) -> any:
        PyTerpreterEnsure.Sequence(sequence)
        self.__mountEnvironment(mount)
        environment: PyTerpreterEnvironment = target or self.autoEnvironment(usage)
        for program in sequence:
            if environment.kill:
                break
            self.execute(program)
        if preserve:
            environment.detach()
            self.__unmountEnvironment(mount)
            return environment
        returnValue: any = None
        if usage == "function" and environment.exists("return"):
            returnValue = environment.retrieve("return")
        environment.destroy()
        self.__unmountEnvironment(mount)
        return returnValue

    def __mountEnvironment(self, mount: PyTerpreterEnvironment | None):
        if mount is not None:
            mount.attach(self.environment.lowest())

    def __unmountEnvironment(self, mount: PyTerpreterEnvironment | None):
        if mount is not None:
            mount.detach()

    def __executeOperation(self, program: list) -> any:
        operator: str = program[0]
        PyTerpreterEnsure.Type(operator, str)
        PyTerpreterEnsure.Includes(operator, self.__operations)
        return self.__operations[operator](self, program[1:])


if __name__ == "__main__":
    PyTerpreter(sys.argv)

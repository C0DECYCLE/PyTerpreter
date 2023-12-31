[
    ["print", "-------------------- System Fundamentals ----------------------"],

    ["print", "Hello World!"],
    ["set", "a", 2],
    ["print", ["get", "a"]],
    ["set", "b", ["add", 3, 4]],
    ["print", ["get", "b"]],
    ["set", "result", ["add", ["get", "a"], ["get", "b"]]],
    ["print", ["get", "result"]],
    ["set", "c", true],
    ["print", ["get", "c"]],

    ["print", "\n-------------------- Boolean Operations ----------------------"],

    ["set", "a", 4],
    ["set", "b", 5],
    ["set", "c", 4],
    ["set", "d", true],

    ["print", ["equal", ["get", "a"], ["get", "c"]]],
    ["print", ["and", ["get", "d"], false]],
    ["print", ["or", ["get", "d"], false]],
    ["print", ["not", true]],
    ["print", ["less", 5, 10]],
    ["print", ["greater", 5, 10]],
    ["print", ["lessEqual", 5, 5]],
    ["print", ["greaterEqual", 5, 10]],

    ["print", "\n-------------------- Math Operations ----------------------"],

    ["set", "a", 4],
    ["set", "b", -5],
    ["set", "c", 2],
    ["set", "d", 12.78],
    ["set", "e", "foo"],

    ["print", ["add", ["get", "a"], ["get", "c"]]],
    ["set", "g", ["multiply", ["get", "d"], 5]],
    ["print", ["get", "g"]],
    ["print", ["multiply", ["get", "d"], 7]],    
    ["print", ["subtract", ["get", "d"], ["get", "c"]]],
    ["print", ["absolute", ["get", "b"]]],
    ["print", ["divide", 10, 2]],
    ["print", ["power", 10 , ["get", "c"]]],
    ["print", ["add", ["get", "e"], "bar"]],

    ["print", "\n-------------------- Conditionals ----------------------"],

    ["set", "a", 4],
    ["set", "c", 4],

    ["if", true, [
        ["print", 3]
    ]],
    ["if", false, [
        ["print", 3]
    ], [
        ["print", 4]
    ]],
    ["if", false, [
        ["print", 3]
    ]],
    ["if", ["not", ["equal", ["get", "a"], ["get", "c"]]], [
        ["print", 3]
    ], [
        ["print", 4]
    ]],

    ["print", "\n-------------------- Arrays ----------------------"],

    ["set", "a", ["array", 5]],
    ["set", "b", ["array", 3]],
    ["arraySet", ["get", "a"], 1, "500"],
    ["arraySet", ["get", "b"], 2, "Hello"],
    ["arraySet", ["get", "a"], 3, ["get", "b"]],

    ["print", ["get", "a"]],
    ["print", ["arrayGet", ["get", "a"], 1]],
    ["print", ["arrayGet", ["arrayGet", ["get", "a"], 3], 2]],

    ["print", "\n-------------------- Dictionaries ----------------------"],

    ["set", "a", ["dictionary"]],
    ["set", "b", ["dictionary"]],
    ["dictionarySet", ["get", "a"], "Name", "James"],
    ["dictionarySet", ["get", "a"], "Age", 21],
    ["dictionarySet", ["get", "a"], "Location", "Hogwarts"],
    ["dictionarySet", ["get", "b"], "Name", "Geralt of Rivia"],
    ["dictionarySet", ["get", "b"], "Age", 99],

    ["print", ["get", "a"]],
    ["print", ["get", "b"]],
    ["print", ["dictionaryGet", ["get", "b"], "Name"]],
    ["print", ["dictionaryGet", ["get", "a"], "Age"]],
    ["set", "c", ["dictionaryMerge", ["get", "a"], ["get", "b"]]],
    ["print", ["get", "c"]],

    ["print", "\n-------------------- Loops ----------------------"],
    
    ["print", "while:"],
    ["set", "a", 0],
    ["while", ["lessEqual", ["get", "a"], 5], [
        ["print", ["get", "a"]],
        ["set", "a", ["add", ["get", "a"], 1]]
    ]],

    ["print", "repeat:"],
    ["set", "a", 0],
    ["repeat", 5, [
        ["print", ["get", "a"]],
        ["set", "a", ["add", ["get", "a"], 1]]
    ]],

    ["print", "\n-------------------- Functions ----------------------"],

    ["set", "greet", ["function", [], [
        ["print", "Hello World!"],
        ["print", "Function and Call worked!!!"]
    ]]],

    ["call", ["get", "greet"], []],

    ["call", ["function", [], [
        ["print", "anonymous function..."],
        ["print", "...got called"],
        ["print", "code executed instantly indirectly"]
    ]], []],

    ["set", "testParam", "iTryToFuckThingsUp"],

    ["call", ["function", ["testParam"], [
        ["print", "parameter argument test:"],
        ["print", ["get", "testParam"]],
        ["if", ["equal", ["get", "testParam"], "iAmAArgument"], [
            ["print", "parameter argument worked successfully"]
        ], [
            ["print", "damn! parameter argument failed"]
        ]],
        ["if", ["equal", ["get", "testParam"], "iTryToFuckThingsUp"], [
            ["print", "things got fucked up"]
        ]]
    ]], ["iAmAArgument"]],

    ["print", ["get", "testParam"]],

    ["set", "customAdd", ["function", ["x", "y"], [
        ["set", "result", ["add", ["get", "x"], ["get", "y"]]],
        ["return", ["get", "result"]],
        ["return", "wrong return"]
    ]]],

    ["print", ["call", ["get", "customAdd"], [10, 5]]],

    ["set", "customFuckUp", ["function", [], [
        ["set", "iiiii", 0],
        ["while", ["less", ["get", "iiiii"], 5], [
            ["if", ["equal", ["get", "iiiii"], 2], [
                ["return", "correct while"]
            ]],
            ["set", "iiiii", ["add", ["get", "iiiii"], 1]]
        ]],
        ["return", "wrong"]
    ]]],

    ["print", ["call", ["get", "customFuckUp"], []]],

    ["set", "customFuckUp", ["function", [], [
        ["set", "iiiii", 0],
        ["repeat", 6, [
            ["if", ["equal", ["get", "iiiii"], 2], [
                ["return", "correct repeat"]
            ]],
            ["set", "iiiii", ["add", ["get", "iiiii"], 1]]
        ]],
        ["return", "wrong"]
    ]]],

    ["print", ["call", ["get", "customFuckUp"], []]],

    ["print", "\n-------------------- Class Object ----------------------"],

    ["set", "Foo", ["class", [
        ["set", "aa", 3],
        ["set", "add", ["function", ["bb"], [
            ["return", ["add", ["get", "aa"], ["get", "bb"]]]
        ]]]
    ]]],

    ["set", "testFoo", ["object", ["get", "Foo"], []]],
    ["print", ["objectGet", ["get", "testFoo"], "aa"]],
    ["print", ["call", ["objectGet", ["get", "testFoo"], "add"], [7]]],

    ["set", "testFoo2", ["object", ["get", "Foo"], []]],
    ["objectSet", ["get", "testFoo2"], "aa", 4],
    ["print", ["objectGet", ["get", "testFoo2"], "aa"]],
    ["print", ["call", ["objectGet", ["get", "testFoo2"], "add"], [8]]],
    ["print", ["call", ["objectGet", ["get", "testFoo"], "add"], [8]]],

    ["set", "Bar", ["class", ["get", "Foo"], [
        ["set", "prefix", "hello "],
        ["set", "constructor", ["function", ["name"], [
            ["print", ["add", ["get", "prefix"], ["get", "name"]]]
        ]]],
        ["set", "something", ["function", [], [
            ["print", "something!"]
        ]]]
    ]]],

    ["set", "testBar", ["object", ["get", "Bar"], ["bob"]]],
    ["print", ["objectGet", ["get", "testBar"], "aa"]],
    ["call", ["objectGet", ["get", "testBar"], "something"], []],
    ["print", ["call", ["objectGet", ["get", "testBar"], "add"], [6]]],

    ["object", ["class", [
        ["set", "constructor", ["function", ["msg"], [
            ["print", ["get", "msg"]]
        ]]]
    ]], ["some wild shit"]],

    ["set", "Shape", ["class", ["get", "Bar"], [
        ["set", "size", 0],
        ["set", "aa", 2],
        ["set", "constructor", ["function", ["name", "shapeSize"], [
            ["call", ["inherit", "constructor"], [["get", "name"]]],
            ["set", "size", ["get", "shapeSize"]]
        ]]],
        ["set", "add", ["function", ["b"], [
            ["set", "old", ["call", ["inherit", "add"], [["get", "b"]]]],
            ["set", "result", ["add", ["get", "aa"], ["get", "old"]]],
            ["return", ["get", "result"]]
        ]]]
    ]]],

    ["set", "abc", ["object", ["get", "Shape"], ["john", 32]]],
    ["print", ["objectGet", ["get", "abc"], "size"]],
    ["print", ["objectGet", ["get", "abc"], "prefix"]],
    ["print", ["objectGet", ["get", "abc"], "aa"]],
    ["call", ["objectGet", ["get", "abc"], "something"], []],
    ["print", ["call", ["objectGet", ["get", "abc"], "add"], [10]]],

    ["set", "Window", ["class", [
        ["set", "size", 0],
        ["set", "constructor", ["function", ["windowSize"], [
            ["set", "size", ["get", "windowSize"]]
        ]]]
    ]]],
    ["set", "House", ["class", [
        ["set", "windows", ["array", 4]],
        ["set", "constructor", ["function", [], [
            ["arraySet", ["get", "windows"], 0, ["object", ["get", "Window"], [3]]],
            ["arraySet", ["get", "windows"], 1, ["object", ["get", "Window"], [7]]],
            ["arraySet", ["get", "windows"], 2, ["object", ["get", "Window"], [4]]],
            ["arraySet", ["get", "windows"], 3, ["object", ["get", "Window"], [5]]]
        ]]]
    ]]],
    ["set", "myHouse", ["object", ["get", "House"], []]],
    ["print", ["objectGet", ["arrayGet", ["objectGet", ["get", "myHouse"], "windows"], 1], "size"]]
]
[
    ["set", "Shape", ["class", [
        ["set", "name", ""],
        ["set", "constructor", ["function", ["shapeName"], [
            ["set", "name", ["get", "shapeName"]]
        ]]],
        ["set", "density", ["function", ["weight"], [
             ["return", ["divide", ["get", "weight"], ["call", ["get", "area"], []]]]
        ]]]
    ]]],

    ["set", "Square", ["class", ["get", "Shape"], [
        ["set", "side", 0],
        ["set", "constructor", ["function", ["squareName", "squareSide"], [
            ["call", ["inherit", "constructor"], [["get", "squareName"]]],
            ["set", "side", ["get", "squareSide"]]
        ]]],
        ["set", "area", ["function", [], [
            ["return", ["multiply", ["get", "side"], ["get", "side"]]]
        ]]]
    ]]],

    ["set", "Circle", ["class", ["get", "Shape"], [
        ["set", "radius", 0],
        ["set", "constructor", ["function", ["circleName", "circleRadius"], [
            ["call", ["inherit", "constructor"], [["get", "circleName"]]],
            ["set", "radius", ["get", "circleRadius"]]
        ]]],
        ["set", "area", ["function", [], [
            ["return", ["multiply", ["multiply", 3.142, ["get", "radius"]], ["get", "radius"]]]
        ]]]
    ]]],

    ["set", "squareObj", ["object", ["get", "Square"], ["sq", 3]]],
    ["set", "circleObj", ["object", ["get", "Circle"], ["ci", 2]]],

    ["print", ["add",
        ["call", ["objectGet", ["get", "squareObj"], "density"], [5]],
        ["call", ["objectGet", ["get", "circleObj"], "density"], [5]]
    ]]
]
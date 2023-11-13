[
    ["set", "get_cube_power", ["function", ["x"], [
        ["return", ["power", ["get", "x"], 3]]
    ]]],
    ["set", "add_cubes", ["function", ["a", "b"], [
        ["return",
            ["add",
                ["call", ["get", "get_cube_power"], [["get", "a"]]],
                ["call", ["get", "get_cube_power"], [["get", "b"]]]
            ]
        ]
    ]]],
    ["print", ["call", ["get", "add_cubes"], [3, 2]]]
]
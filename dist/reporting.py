import sys
from datetime import datetime
from typing import Dict, Union, List


class TraceReporter:
    def __init__(self, traceFile: str):
        self.traceFile: str = traceFile
        self.functions: Dict[str, Dict[str, Union[int, float, datetime]]] = {}

        lines: List[str] = self.__readFile()
        self.__processTraceData(lines)
        self.__generateReport()

    @staticmethod
    def __calculatePadding(maxSeperatorLength: int) -> tuple[int, int]:
        leftPadding: int = (maxSeperatorLength - len("Function Name")) // 2
        rightPadding: int = maxSeperatorLength - len("Function Name") - leftPadding

        if leftPadding + rightPadding != maxSeperatorLength:
            rightPadding += 1
        return leftPadding, rightPadding

    def __readFile(self) -> List[str]:
        with open(self.traceFile, "r") as file:
            lines: List[str] = file.readlines()

        return lines

    def __processTraceData(self, lines: List[str]) -> None:
        for line in lines:
            functionID, funtionName, event, timestampStr = map(
                str.strip, line.split(",")
            )

            timestamp: datetime = datetime.strptime(
                timestampStr, "%Y-%m-%d %H:%M:%S.%f"
            )

            if funtionName not in self.functions:
                self.functions[funtionName] = {
                    "calls": 0,
                    "totalTime": 0,
                    "startTime": None,
                }

            if event == "start":
                self.functions[funtionName]["startTime"] = timestamp
            elif event == "stop":
                startTime: datetime = self.functions[funtionName]["startTime"]
                elapsedTime: float = (timestamp - startTime).total_seconds() * 1000
                self.functions[funtionName]["totalTime"] += elapsedTime
                self.functions[funtionName]["calls"] += 1

    def __generateReport(self) -> None:
        maxNameLength: int = max(len(name) for name in self.functions.keys())
        maxSeperatorLength: int = max(maxNameLength, 13)

        leftPadding, rightPadding = self.__calculatePadding(maxSeperatorLength)

        print(
            f"|{' ' * leftPadding}Function Name{' ' * rightPadding} | Num. of calls  |  Total Time (ms) |  Average Time (ms)  |"
        )
        print(
            f"|{'-' * (maxSeperatorLength + 2)}|----------------|------------------|---------------------|"
        )

        for function_name, data in self.functions.items():
            numCalls: int = data["calls"]
            totalTime: float = data["totalTime"]
            averageTime: float = totalTime / numCalls

            print(
                f"| {function_name:<{maxNameLength}} | {numCalls:<14} | {totalTime:<16.3f} | {averageTime:<19.3f} |"
            )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python reporting.py trace_file.log")
    else:
        traceFile: str = sys.argv[1]
        reporter: TraceReporter = TraceReporter(traceFile)

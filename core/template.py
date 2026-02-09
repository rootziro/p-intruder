#Compile raW HTTP data for preproccessing injection representations
#This is a template for the preproccessing injection representation, which is used to compile raw HTTP data into a format that can be used for preproccessing injection representations. The templateddata is used to create a structured representation of the raw HTTP data, which can then be used for further processing and analysis.
from dataclasses import dataclass
from tkinter.font import names
from typing import List

MARKER_OPEN = "{{"
MARKER_CLOSE = "}}"

@dataclass(frozen=True)
class InjectionPoint:
    name: str
    index: int

@dataclass(frozen=True)
class CompiledTemplate:
    parts: List[str]
    injection_points: List[InjectionPoint]


def compiled_template(raw: str) -> CompiledTemplate:
        parts: List[str] = []
        injection_points: List[InjectionPoint] = []

        cursor = 0
        part_index = 0

        while cursor < len(raw):
            start = raw.find(MARKER_OPEN, cursor)
            if start == -1:
                parts.append(raw[cursor:])
                break
            end = raw.find(MARKER_CLOSE, start + 1)
            if end == -1:
                raise ValueError("Unclosed injection marker")
            
            parts.append(raw[cursor:start])

            name = raw[start + len(MARKER_OPEN):end]
            if not name:
                raise ValueError("Empty injection marker")
            
            if len(names) != len(set(names)):
                raise ValueError("Duplicate injection point names")
            
            injection_points.append(
                InjectionPoint(name=name, index=part_index + 1)
            )

            parts.append("")  # Placeholder for the injection point
            part_index += 2
            cursor = end + len(MARKER_CLOSE)

        if not injection_points:
            raise ValueError("No injection points found")
                                                                                                            
        return CompiledTemplate(parts, injection_points) d           
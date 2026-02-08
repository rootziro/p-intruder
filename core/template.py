#Compile raW HTTP data for preproccessing injection representations
#This is a template for the preproccessing injection representation, which is used to compile raw HTTP data into a format that can be used for preproccessing injection representations. The templateddata is used to create a structured representation of the raw HTTP data, which can then be used for further processing and analysis.
from dataclasses import dataclass
from typing import List

MAKER_OPEN = "{{"
MAKER_CLOSE = "}}"

@dataclass(frozen=True)
class InjectionPoint:
    name: str
    index: int

@dataclass(frozen=True)
class compiledTemplate:
    parts: List[str]
    injection_points: List[InjectionPoint]


def compiled_template(raw: str) -> compiledTemplate:
        parts: List[str] = []
        injection_points: List[InjectionPoint] = []

        cursor = 0
        part_index = 0

        while cursor < len(raw):
            start = raw.find(MAKER_OPEN, cursor)
            if start == -1:
                parts.append(raw[cursor:])
                break
            end = raw.find(MAKER_CLOSE, start + 1)
            if end == -1:
                raise ValueError("Unclosed injection marker")
            
            parts.append(raw[cursor:start])

            name = raw[start + 1:end]
            if not name:
                raise ValueError("Empty injection marker")
            
            injection_points.append(
                InjectionPoint(name=name, index=part_index + 1)
            )

            parts.append("")  # Placeholder for the injection point
            part_index += 2
            cursor = end + 1

        if not injection_points:
            raise ValueError("No injection points found")
        
        return compiledTemplate(parts, injection_points)
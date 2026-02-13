#Compile raW HTTP data for preproccessing injection representations
#This is a template for the preproccessing injection representation, which is used to compile raw HTTP data into a format that can be used for preproccessing injection representations. The templateddata is used to create a structured representation of the raw HTTP data, which can then be used for further processing and analysis.
from dataclasses import dataclass
from typing import List

from ibm_db import result

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

    def render(self, payloads_map: dict) -> str:
        result = list(self.parts)
        for point in self.injection_points:
            if point.name not in payloads_map:
                raise ValueError(f"Missing payload for injection point: {point.name}")
            result[point.index] = payloads_map[point.name]
        return "".join(result)

def compile_template(raw: str) -> CompiledTemplate:
    parts: List[str] = []
    injection_points: List[InjectionPoint] = []
    names: List[str] = []  # Track names for duplicate checking
    cursor = 0
    part_index = 0

    while cursor < len(raw):
        start = raw.find(MARKER_OPEN, cursor)
        if start == -1:
            parts.append(raw[cursor:])
            break
        
        end = raw.find(MARKER_CLOSE, start + len(MARKER_OPEN))
        if end == -1:
            raise ValueError("Unclosed injection marker")
        
        parts.append(raw[cursor:start])
        name = raw[start + len(MARKER_OPEN):end].strip()
        
        if not name:
            raise ValueError("Empty injection marker")
        
        # Check for duplicates
        if name in names:
            raise ValueError(f"Duplicate injection point name: {name}")
        
        names.append(name)
        injection_points.append(
            InjectionPoint(name=name, index=part_index + 1)
        )
        parts.append("")  # Placeholder for the injection point
        part_index += 2
        cursor = end + len(MARKER_CLOSE)
    
    if not injection_points:
        raise ValueError("No injection points found")
    
    return CompiledTemplate(parts, injection_points)

#Test
if __name__ == "__main__":
    raw_http = """POST /login HTTP/1.1 
    Host: juice-shop.herokuapp.com
    username={{user}}&password={{pass}}"""

    template = compile_template(raw_http)
    print(template.render({'user': 'admin', 'pass': 'password123'}))
from dataclasses import dataclass

@dataclass
class Perf:
    tb_code: str
    aggregate: bool
    language: str
    system: str
    perf: float
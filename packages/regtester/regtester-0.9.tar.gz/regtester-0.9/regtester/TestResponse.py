from dataclasses import dataclass
from typing import List

from TestItemResult  import TestItemResult
@dataclass
class TestResponse:
    all_good: bool
    regex_name: str
    success_count:int
    failure_count:int
    total:int
    successes : List[TestItemResult] 
    failures : List[TestItemResult]

if __name__ == "__main__":
    x = TestResponse(
        status=True,
        regex_name="lol",
        success_count=12,
        failure_count=2,
        successes = [TestItemResult("text","expected","expected")],
        failures = [TestItemResult("text","expected","got")]
    )
    print(x)
from dataclasses import dataclass

@dataclass
class TestItemResult:
    text: str
    expected_result: any
    actual_result:any
    success:bool

if __name__ == "__main__":
    x = TestItemResult("love","pol","lop",False)
    print(x)
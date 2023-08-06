from dataclasses import dataclass

@dataclass
class RegExTestItem:
    text: str
    expected_result: any

if __name__=="__main__":
    x = RegExTestItem("love","pol")
    print(x)
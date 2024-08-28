from enum import Enum

# Mapping of columns to ints for parsing purposes
class WgaTsv(Enum):
    author=0
    lifeInfo=1
    title=2
    date=3
    technique=4
    location=5
    url=6
    form=7
    type=8
    school=9
    timeframe=10
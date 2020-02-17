### Coding Test Instructions

Make a program that calculates and displays worker utilization over several weeks. It should take in entries from a log file in this format:

```
WORKER Alex "2019-10-10T12:00:00Z/2019-10-10T13:00:00Z"
WORKER Derick "2019-10-10T12:00:00Z/2019-10-10T15:00:00Z"
WORKER Alex "2019-10-10T13:00:00Z/2019-10-10T14:00:00Z"
```

Above, Alex has two entries of an hour each, and Derick has one entry that is 3 hours long.
Worker utilization is calculated like so: `hours_worked_during_given_week / 40`.
A manager might use something like this to see which employees should be given more work based on what percentage of the 40-hour workweek they have been working. The output should be formatted something like this:

```
Alex 5%
Derick 7.5%
```

Alex was only utilized 5% because `2 / 40 = 0.05`.

Additionally, workers who were utilized more than 100% should float to the top. If a worker goes over 8 hours in a single day, than any amount of time over 8 hours should count as double utilization. This way, a manager can easily see who is working overtime.

### Usage Instructions

After downloading and extracting the `tar` file, ensure you have Python 3.6+ on your system.

1. From inside the `/CompanyCodingTest` dir, run `pip install -r requirements.txt`.
   > Note that if you have multiple Python installations on your system, this command may not work. If this occurs, try setting up a virtual environment with the correct Python version and trying the command again.
2. From inside the `/CompanyCodingTest` dir, run `python program.py input.txt`. To specify your own input file, simply change `input.txt` to the path of your desired input file.

#### Tests

From inside the `/CompanyCodingTest` dir, run `pytest`.

### Implementation Details

Mission: Get average utilization over several weeks.

> Note: Most of the documentation is kept close to the code it describes, where it should be. In this document, you'll find high-level descriptions of design decisions and problem-solving techniques I applied in the program. The documentation by the code is more granular.

### Architecture

I designed the program with an MVC-style approach.

Model: `database.py`

View: `program.py`

Controller: also `program.py`

### Problem-Solving

#### program.py

I used `pathlib` and `argparse` so as not to reinvent the wheel with `os`. The resulting code is much cleaner. Additionally, `pathlib` automatically formats the path correctly for the user's operating system.

#### database.py

Declaring a database and putting all of our information in it is far more explicit than an 'invisible database' made of dictionaries and lists floating around in memory. I used SQLite because that's all we really need here.

### Tests

- I used `pytest` to avoid all the boilerplate that `unittest` requires.
- Since `program.py` mainly just calls functions made elsewhere and formats things for display, I focused on testing `database.py` and `utils.py`.
- The `conftest.py` file holds my fixtures (stuff that makes it easier for me to set up the right test conditions).

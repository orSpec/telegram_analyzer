# Telegram Analyzer
This OSINT tool is for the analysis of Telegram channels. You can feed the tool by providing a JSON file created by Jordan Wildon's [Telepathy](https://github.com/jordanwildon/Telepathy). The JSON contains a dump of all messages of a Telegram Channel.

## Installation
Clone the repo and install all requirements.
```
git clone https://github.com/orSpec/telegram_analyzer
cd telegram_analyzer
pip install -r requirements.txt
```
## Usage
```
python analyzer.py [-h] [-t] [-dh [UserID ...]] [-w] [-s] file
```
with these arguments:
```
  file                  JSON file containing the telegram data

options:
  -h, --help            show this help message and exit
  -t, --time            Create chart of posting times
  -dh [UserID ...], --daysHours [UserID ...]
                        Create heatmap of posting days vs. times for all users or certain UserIDs
  -w, --weekday         Create chart of messages per weekday
  -s, --statistics      Show statistics (#members, #messages, #mean nr of messages etc.)
  -ma n, --mostActive n
                        Show the top n members by messages and their message count. Need to pass n > 0 as input
```


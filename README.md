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

## Examples
```
-s
```
![image](https://user-images.githubusercontent.com/59450716/157318093-edef0288-38f9-444b-b35f-a398c87113ad.png)


```
-ma
```
![image](https://user-images.githubusercontent.com/59450716/157317931-1b7203bf-e6b2-4c1e-869e-a1e789ba5901.png)

```
-w
```
<img src="https://user-images.githubusercontent.com/59450716/157318289-d6b6c08f-b3d0-46c0-b5da-5f28430185ed.png" width="700">

```
-t
```
<img src="https://user-images.githubusercontent.com/59450716/157318617-4a9195d9-c8b8-4617-9156-bc21cf5e9314.png" width="800">

```
-dh
```
<img src="https://user-images.githubusercontent.com/59450716/157318706-f0e0de57-0994-45a5-bc1a-c0e3399f525e.png" width="900">

#Job Bot
Telegram bot for vacancies search. Implementation is based on HNSW algorithm 
from [hnswlib](https://github.com/nmslib/hnswlib).

Data was crawled from [HH api](https://github.com/hhru/api) and consist of 
117375 vacancies preferably from the fields of IT, medicine and marketing. 

1) The original crawled data in .JSON format is available at: https://yadi.sk/d/4p2kfG-1ilbH1g 
2) The preprocessed data is available at: https://yadi.sk/d/mrh5x9CzvmWq4w
3) The search index built is available at: https://yadi.sk/d/Kd-Q7A2UOyseLg

### Installation:
In order to run and test the bot, please follow the steps below:
1) Clone this repository into your local machine. You should have ```Python 3.6+``` and ```pip``` installed.
2) Insert following commands in the terminal: ```pip install -r requirements.txt```
3) Register yours unique Telegram bot, then in the root directory of the repository  

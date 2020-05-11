# Job Bot
Telegram bot for vacancies search. Implementation is based on HNSW algorithm 
from [hnswlib](https://github.com/nmslib/hnswlib).

Data was crawled from [HH api](https://github.com/hhru/api) and consist of 
117375 vacancies preferably from the fields of IT, medicine and marketing. 

1) The original crawled data in .JSON format is available at:   https://yadi.sk/d/4p2kfG-1ilbH1g 
2) The preprocessed data is available at:                       https://yadi.sk/d/mrh5x9CzvmWq4w
3) The search index built is available at:                      https://yadi.sk/d/Kd-Q7A2UOyseLg

### Installation:
In order to run and test the bot, please follow the steps below:
1) Clone this repository into your local machine. You should have ```Python 3.6+``` and ```pip``` installed.
2) Insert following commands in the Bash terminal: ```pip install -r requirements.txt```
3) Download pre-built [Search Index and all additional data structures](https://yadi.sk/d/Kd-Q7A2UOyseLg), 
then put it inside `ser_structures` directory, which is in the root of the 
repository.
4) Register your unique Telegram bot, then put your token in the `token.txt` file
 in the root of the repository.
5) Run launching script in the Bash terminal ``. run_bot.sh``.
That's all, after that you can find your bot in the Telegram and test it!

Instead of downloading pre-built index and structures you also can launch the 
Crawler and all the preprocessing pipeline in your machine. In this case you collects fresher vacancies, 
but of course be ready to wait, it is not fast process in general. Run  ``. run_pipeline.sh`` in your
terminal if you want to test the crawler and the pipeline. Finally, when the script finishes, 
search index and all the structures will build. Just put your token and run ``. run_bot.sh`` 
after that to test it.    


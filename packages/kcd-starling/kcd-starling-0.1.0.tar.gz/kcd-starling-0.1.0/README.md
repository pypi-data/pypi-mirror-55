# Starling
It consists of blueprint patterns and can be executed independently by developing only the required logic for each topic.

## Blueprint details

### Blueprint for scrapper
#### tasks
Specify the logic that defines the tasks that will actually work

#### actions
specify the actions to activate.

#### authenticate 
Create a topic-specific authentication login. Return authenticated session to scrape credential data.

### Blueprint for action
#### fetch
Create a topic-specific scrapping logic. The drivers(bs4, selenium, and so on) are already in place.

#### transform
If you need any transform for saving, write a transform logic.

#### interval
If you need to slow down the fetch speed, specify the seconds.

## How to run
Development Environment
```sh
export STARLING_PROFILE=development
python3 sample_naver_poi.py 
```

Production Environment
```sh
export STARLING_PROFILE=production
python3 sample_naver_poi.py 
```
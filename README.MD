# Post crawler

Post crawler for Twitter, Reddit.

## Getting Started

This project running tested on Python3 

### Prerequisites

chromedriver (https://chromedriver.chromium.org/downloads) must be located in project root folder (`~/UWA_post_cralwer/`). 

You can install related packages using `requirements.txt`

```
pip3 -r requirements.txt
```

`API_keys.ini` is not used for now.

### Database

You can make database using `*.sql` file. 

sql file was written for `mysql`



## Running the tests

You can run this project using `python` 

```shell
python3 crawler.py 
```

There are some options for running.  more detail options can see by typing `--help` option.  

#### Twitter

For crawling Twitter. you need a valid account's headers information for each keyword.

You can update header file in `headers.ini` file.



## Authors

* **Hanbin jang** - *Initial work* - [email](espoirnoa09@gmail.com)

## License

This project is licensed under the UWA, SKKU License 




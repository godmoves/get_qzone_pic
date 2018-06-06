# get_qzone_pic
Download pictures form a target Qzone

## Dependencies
- python 3.x  
- selenium  
- chromedriver 

If you need reference for selenium and chromedriver installation, please check it [here](https://christopher.su/2015/selenium-chromedriver-ubuntu/)

## Usage
Change the `user QQ id`, `password`, `target QQ id` and `process number` in the python file.

## Possible issue  
Only test the code on Ubuntu 17.10, maybe you need add `.encode('utf-8')` to get correct info on a Windows machine. 

## Credit  
This code originally comes from [here](https://www.zh30.com/python-selenium-qqzone-album.html), and I just wrap it into python3 version and add the functions for downloading.

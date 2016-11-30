import requests
import json

import datetime
import time

uri = "http://207.251.86.229/nyc-links-cams/LinkSpeedQuery.txt"
def get():
    response = requests.get(uri)
    content = response.content.decode("ascii").split("\n")
    return (line for line in content)
def test():
    content = get()
    while True:
        for line in content:
            yield line
        yield 

def main():
    a = get()
    while True:
        aa = next(a)
        if aa:
            print(aa)
if __name__ == "__main__":
    main()
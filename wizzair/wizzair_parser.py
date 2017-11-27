import requests
headers = {
    'origin': 'https://wizzair.com'
    ,'accept-encoding': 'gzip, deflate, br'
    ,'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
    ,'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
    ,'content-type': 'application/json'
    ,'accept': 'application/json, text/plain, */*'
    ,'referer': 'https://wizzair.com/ru-ru/rejsy/raspisanie/VKO/DEB'
    ,'authority': 'be.wizzair.com'
    ,'cookie': 'ak_bmsc=DDF3200FDCDC8E988D2391FDBCFD1FA85F65857C851C0000AEFE1B5AA04E4057~plCgZGErB/9lXPu3igrnD+MAiNyRAG0L6Nl+kx/96lSDYK6Xsh/jRTFyePgZmqh2Ezv2P2L9KWrGUpn1rGbBeqQQK0Bm5R4xZ9/pjuqeVnXRuGA3o8NPDgSb7cJsWp/jLP4iC7pNVLxlLV3c6mMevJHw+7p8hrHR33Ma447an6bb5Prncin0De24gVAkeOp/I5CJ1tHCThR8nIbOwRnXZWTbw8IUv1mLKa2+OOABFobG8=; ASP.NET_SessionId=3viri0wu0ixaivx5kmnbtogj; bm_sv=FC4746AB380FC43C6C7187028C8B5B6C~1Pul1Lldd6gbCabCt4DqKVkYlM3PgWotq2UN4N1vwnViFuZvwpiWO+qOYbFdZ+GsPbdYom/dHgjfXNF6dhJIb95hqv6kW9hs75JdThbqn85l8vir79rjSb35PF4j+g6tLH1KEDm/8fJaApuHZhELS6kN9v3pyQ0SFh5SghyrVFg='
}

data= '{"flightList":[{"departureStation":"VKO","arrivalStation":"DEB","from":"2018-07-30","to":"2018-09-02"},{"departureStation":"DEB","arrivalStation":"VKO","from":"2018-06-25","to":"2018-08-05"}],"priceType":"wdc"}'

url = 'https://be.wizzair.com/7.6.1/Api/search/timetable'
resp = requests.post(url, headers=headers, data=data)

resp.json()

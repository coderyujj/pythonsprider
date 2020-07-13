import requests
import re, json


# 请求网页，返回响应体
def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(response)
        return response.text
    return None


# 使用正则将需要的数据剥离
def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)"'
        + '.*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>'
        + '.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>'
        + '.*?fraction.*?>(.*?)</i>.*?</dd>',
        re.S)
    res = re.findall(pattern, html)

    for i in res:
        yield {
            '排名': i[0],
            '封面': i[1],
            '影片名称': i[2],
            '主演': i[3].strip()[3:],
            '上映时间': i[4].strip()[5:],
            '评分': i[5].strip() + i[6].strip(),
        }


# 将结果写入到文件
def write_to_file(content):
    with open('猫眼电影排行TOP100.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 10)

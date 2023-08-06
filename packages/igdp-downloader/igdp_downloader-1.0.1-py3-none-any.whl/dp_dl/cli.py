import argparse
import requests
import bs4
import re
import json
import os

cwd = os.getcwd() + '/'


def _geturl(username):
    url = 'https://www.instagram.com/{}'.format(username)
    page = requests.get(url)
    if page.status_code == 200:
        soup = bs4.BeautifulSoup(page.text,'lxml')
        scrpt = soup.find('script',text= re.compile("window._sharedData")).text.replace('window._sharedData = ','')
        scrpt = json.loads(scrpt.replace(';',''))['entry_data']['ProfilePage'][0]['graphql']['user']
        print("***ACCOUNT DETAILS***\n\nFull name: {}\nFollowers: {}\nFollowing: {}\nPrivate: {}\n".format(scrpt['full_name'],scrpt['edge_followed_by']['count'],scrpt['edge_follow']['count'],scrpt['is_private']))
        return scrpt['profile_pic_url_hd']
    else:
        pass


def _getdp(url, fname):
    img = requests.get(url, stream=True)
    with open(fname, 'wb') as f:
        f.write(img.content)


def execute(username, foldername):
    if foldername == None:
        filename = cwd + username + '.jpg'
    else:
        filename = foldername + username + '.jpg'
    url = _geturl(username)
    if url != None:
        dp = _getdp(url,filename)
        print("SUCCESS! Image saved in file: {}\n".format(filename))
    else:
        print('USER DOES NOT EXISTS')


def main():
    parser = argparse.ArgumentParser(description='Instagram DP Downloader: A Python module to download DP of Instagram Profiles in the best quality possible')
    parser.add_argument('-u', '--username', help='Username of Instagram profile',type=str, required=True)
    parser.add_argument('-o', '--output', help='Specify output folder', nargs='?')
    args = parser.parse_args()
    execute(args.username, foldername=args.output)


if __name__ == "__main__":
    main()
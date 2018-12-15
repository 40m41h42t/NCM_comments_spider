import requests
import re
import json
import pprint

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'}
session = requests.session()


def get_songlists_list(limit, user_id):
    playlist_id = []
    playlist_name = []
    user_url = 'http://music.163.com/api/user/playlist?offset=0&limit={}&uid={}'.format(
        limit, user_id)
    r = session.get(user_url, headers=headers)
    playlist_id.extend(re.findall(r'"id":(.+?)}', r.text))
    playlist_name.extend(re.findall(r'"name":"(.+?)"', r.text))
    return playlist_name, playlist_id


def get_songs_list(playlist_id):
    song_name = []
    comment_id = []     # 所有歌单的 comment id
    for i in playlist_id:
        # add song titles
        r = requests.get(
            'http://music.163.com/playlist?id={}'.format(i), headers=headers)
        song_titles = re.findall(
            r'song\?id=\d+?">(.+?)</a>', r.text.replace('\xa0', ' '))
        song_name.append(song_titles)
        # add comment id
        r = requests.get(
            'http://music.163.com/api/playlist/detail?id={}'.format(i),
            headers=headers)
        commentThread = re.findall(r'R_SO_4_(\d+?)"', r.text)
        comment_id.append(commentThread)    # 单个歌单的 comment id
        # FIXME: delete break to get all playlist
        break
    return song_name, comment_id


def get_songs_comments(comment_id):
    comment_str = []
    for i in comment_id:    # 单个歌单的 id
        single_comment_list = []
        for j in i:         # 每首歌的 id
            url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_{}'.format(j)
            r = requests.get(url, headers=headers)
            hot_comment_list = re.findall(r'hotComments(.+?)comments', r.text)
            hot_comment = ''.join(hot_comment_list)
            hot_comment_list = re.findall(r'"content":"(.+?)"', hot_comment)
            # FIXME: delete break to get all comments
            single_comment_list.append(hot_comment_list)
            break
        comment_str.append(single_comment_list)
        break
    return comment_str

def output_information(playlist_name, song_name, comments_str):
    for i in range(len(playlist_name)):
        print("playlist: "+playlist_name[i])
        for j in range(len(song_name[i])):
            print("song name: "+song_name[i][j])
            for k in comments_str[i][j]:
                print(k+"\n")
            # FIXME: delete break to output all comments
            break
        break

if __name__ == '__main__':
    user_id = "37682214"

    playlist_name, playlist_id = get_songlists_list(60, user_id)
    if len(playlist_id)!=len(playlist_name):
        print("len(playlist_id)!=len(playlist_name) error")
        print("len(playlist_id): "+str(len(playlist_id)))
        print("len(playlist_name): "+str(len(playlist_name)))
        exit(0)
    song_name, comment_id = get_songs_list(playlist_id)
    comments_str = get_songs_comments(comment_id)
    output_information(playlist_name, song_name, comments_str)

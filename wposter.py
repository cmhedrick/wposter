import sys
import json
import urllib.parse
import urllib.request

from lxml.etree import HTML

# config for lazy testing
import config

# colors
# blue special notice
NOTICE = '\033[94m'
# red is important
ALERT = '\033[91m'
# green is Good
SUCCESS = '\033[92m'
# you need the end encoding after the message
END = '\033[0m'

# set basic globals
cmd = ''
base_url = ''
api_url = 'wp-json/'

# modest lil banner
print('\n-------------------')
print('Welcome to WPoster!')
print('-------------------')

def clean_json_response(dirty_json):
    '''
    Takes the HTTPResponse that is actually JSON and makes it to a string
    so that it can be decoded by json.loads()
    :param dirty_json: HTTPResponse Object
    :return: json string
    '''

    # set encoding
    encoding = dirty_json.info().get_content_charset('utf-8')
    return dirty_json.read().decode(encoding)

def get_posts():
    '''
    Prints a list of posts and IDs in format 'ID: title: author ID'
    :return: None
    '''

    clean_json = clean_json_response(
        urllib.request.urlopen(api_url + 'wp/v2/posts')
    )
    posts = json.loads(clean_json)
    for post in posts:
        print(SUCCESS + '[+]' + END + '{0}: {1}: {2}'.format(
            post['id'], post['title']['rendered'], post['author'])
        )

def read_post(post_id):
    '''
    Gets information on selected post
    :param post_id: int
    :return:
    '''

    try:
        clean_json = clean_json_response(
            urllib.request.urlopen(api_url + 'wp/v2/posts/' + str(post_id))
        )
        post = json.loads(clean_json)
        local_post = open('local_post.html', "w")
        local_post.write(post['content']['rendered'])
        local_post.close()
        print(
            SUCCESS + '[+]' + END + 'Post: {0} | Downloaded'.format(
                post['title']['rendered']
            )
        )

    except urllib.error.HTTPError as e:
        print(
            '{0}{1}'.format(
                ALERT + '[!]' + END,
                e.code
            )
        )
    except urllib.error.URLError as e:
        print(
            '{0}{1}'.format(
                ALERT + '[!]' + END,
                e.code
            )
        )

def get_users():
    try:
        clean_json = clean_json_response(
            urllib.request.urlopen(api_url + 'wp/v2/users')
        )
        posts = json.loads(clean_json)
        for post in posts:
            print(SUCCESS + '[+]' + END + '{0}: {1}'.format(
                post['id'], post['name'])
            )

    except urllib.error.HTTPError as e:
        print(
            '{0}{1}'.format(
                ALERT + '[!]' + END,
                e.code
            )
        )
    except urllib.error.URLError as e:
        print(
            '{0}{1}'.format(
                ALERT + '[!]' + END,
                e.code
            )
        )

def get_media():
    try:
        clean_json = clean_json_response(
            urllib.request.urlopen(api_url + 'wp/v2/media')
        )
        posts = json.loads(clean_json)
        #import pdb; pdb.set_trace()
        for post in posts:
            print(SUCCESS + '[+]' + END + 'Author:{0} Link:{1} Title:{2}'.format(
                post['author'], post['link'], post['title'])
                  )

    except urllib.error.HTTPError as e:
        print(
            '{0}{1}'.format(
                ALERT + '[!]' + END,
                e.code
            )
        )
    except urllib.error.URLError as e:
        print(
            '{0}{1}'.format(
                ALERT + '[!]' + END,
                e.code
            )
        )


# menu
while cmd != 'q'.lower():
    # display menu and get cmd
    print('\nenter a command:')
    print('set | set url of wordpress site')
    print('users | get users')
    print('posts | get post info')
    print('read | read post by id')
    print('media | get media files')
    print('q | kill session')
    cmd = input('==> ')

    if cmd == 'set'.lower():
        try:
            if config.URL and config.URL.strip() != '':
                base_url = config.URL
            else:
                base_url = input('URL==> ')

        except:
            base_url = input('URL==> ')

        api_url = base_url + api_url
        print(SUCCESS + '[+]' + END + 'URLS set')

    elif cmd == 'read'.lower():
        read_post(input('ID of post==> '))

    elif cmd == 'media'.lower():
        get_media()

    elif cmd == 'posts'.lower():
        get_posts()

    elif cmd == 'users':
        get_users()

    elif cmd == 'q'.lower():
        print(NOTICE + '[<3]' + END + 'Thanks for playing!')

    else:
        print(ALERT + '[!]' + END + 'INVALID COMMAND')
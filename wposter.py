import json
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

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


def request(url):
    return urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})


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
    try:
        clean_json = clean_json_response(
            urllib.request.urlopen(request(api_url + 'wp/v2/posts'))
        )
        posts = json.loads(clean_json)
        for post in posts:
            print(SUCCESS + '[+]' + END + '{0}: {1}: {2}'.format(
                post['id'], post['title']['rendered'], post['author'])
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
                e.reason.strerror
            )
        )

def read_post(post_id):
    '''
    makes local copy of the site, prints line to indicate title of download
    :param post_id: int
    :return: None
    '''

    try:
        clean_json = clean_json_response(
            urllib.request.urlopen(
                request(api_url + 'wp/v2/posts/' + str(post_id))
            )
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
                e.reason.strerror
            )
        )

def get_users():
    '''
    prints lines of users in format: id, name
    :return:
    '''
    try:
        clean_json = clean_json_response(
            urllib.request.urlopen(
                request(api_url + 'wp/v2/users')
            )
        )
        posts = json.loads(clean_json)
        for post in posts:
            print(SUCCESS + '[+]' + END + '{0}: user:{1} name:{2}'.format(
                post['id'], post['slug'], post['name'])
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
                e.reason.strerror
            )
        )

def get_media():
    '''
    prints lines containing information on uploaded media in format: 'author link title'
    :return:
    '''
    try:
        clean_json = clean_json_response(
            urllib.request.urlopen(
                request(api_url + 'wp/v2/media')
            )
        )
        posts = json.loads(clean_json)
        #import pdb; pdb.set_trace()
        for post in posts:
            print(SUCCESS + '[+]' + END + 'Author:{0} Link:{1} Title:{2}'.format(
                post['author'], post['link'], post['title']['rendered'])
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
                e.reason.strerror
            )
        )

def get_uploads():
    '''
    Will do a lazy scan and print directories to check for uploads.
    Attempts to connect to default then common routes
    :return:
    '''
    attempts = 0
    while attempts < 2:
        try:
            if attempts == 0:
                html = urllib.request.urlopen(
                        request(base_url + 'content/uploads/')
                )
            if attempts == 1:
                html = urllib.request.urlopen(
                        request(base_url + 'wp-content/uploads/')
                )
                
            parsed_html = BeautifulSoup(html, 'html.parser')

            for upload_dir in parsed_html.find_all('a')[5:]:
                print(
                    SUCCESS + '[+]' + END + '{0}{1}'.format(
                        base_url, upload_dir.get('href')
                    )
                )

        except urllib.error.HTTPError as e:
            attempts += 1
            print(
                '{0}{1}'.format(
                    ALERT + '[!]' + END,
                    e.code
                )
            )
        except urllib.error.URLError as e:
            attempts += 1
            print(
                '{0}{1}'.format(
                    ALERT + '[!]' + END,
                    e.reason.strerror
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
    print('uploads | get uploaded files')
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

    elif cmd == 'uploads'.lower():
        get_uploads()

    elif cmd == 'posts'.lower():
        get_posts()

    elif cmd == 'users':
        get_users()

    elif cmd == 'q'.lower():
        print(NOTICE + '[<3]' + END + 'Thanks for playing!')

    else:
        print(ALERT + '[!]' + END + 'INVALID COMMAND')

from steem.post import Post
import sys

def get_winner_data(winner):
    index = 0
    photo_index = 0
    string = winner.split(" ")
    permlink = string[0]

    if len(string)>1:
        photo_index = string[1]

    for c in permlink:
        if c == '@':
            return (permlink[index:], int(photo_index))
        index += 1

def run():
    filename = sys.argv[-1]
    url_list = open(filename).read().splitlines()

    header = "<center>\n# Test selection\n***\n"
    body = ""
    footer = "End of test selection\n</center>"

    for n in range(0,len(url_list)):
        permlink , photo_index = get_winner_data(url_list[n])
        post = Post(permlink)
        author = post['author']
        title = post['title']
        image = post['json_metadata']['image'][photo_index]

        body += "Title: {}<br>Author: @{}<br>Permlink: {}<br>Image:{}\n***\n".format(title, author, permlink, image)

    print (header + body + footer)


if __name__ == '__main__':
    run()

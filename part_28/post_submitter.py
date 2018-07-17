from steem import Steem

import exif
import imgur
import sys
import os
import textwrap
import json


class Post_submitter():
    def __init__(self):
        # Steem RPC Node settings
        self.nodes = ['https://api.steemit.com']
        self.steemPostingKey = os.environ.get('steemPostingKey')
        self.steem = Steem(wif=self.steemPostingKey, nodes=self.nodes)

    def submit_post(self, account, filename):
        # Load post data
        post = json.load(open(filename))
        title = post['title']
        tags = post['tags']
        caption = post['caption']
        image = post['image']

        # upload the image and retrieve the url
        url = imgur.upload_image(image)

        # process the iamge for EXIF data to construct a table
        table = exif.process_image(image)

        # Use template to construct a body for the post
        body = textwrap.dedent(
            f"""
            <center>
            {caption}
            ---
            [![image]({url})]({url})
            ---

            {table}

            </center>
            """)

        # Submit post to the Steem Blockchain
        self.steem.post(title=title, body=body, author=account, tags=tags)


if __name__ == '__main__':
    try:
        account = sys.argv[1]
        filename = sys.argv[2]
        post_submitter = Post_submitter()
        post_submitter.submit_post(account, filename)
    except Exception as e:
        print("Takes two arguments: accountname filename")

from imgurpython import ImgurClient

# account settings, register your application here:
# https://api.imgur.com/oauth2/addclient
client_id = ''
client_secret = ''

client = ImgurClient(client_id, client_secret)


def upload_image(filename):
    # upload the image as anonymous
    image = client.upload_from_path(filename, anon=True)

    # retrieve only the image url from the retrieved json data
    # return the url
    url = image['link']
    return url

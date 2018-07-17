import exifread


def create_table(tags):
    # extract required data
    brand = tags['Image Make']
    model = tags['Image Model']
    date = tags['Image DateTime']
    shutterspeed = tags['EXIF ExposureTime']
    focallength = tags['EXIF FocalLength']
    aperture = tags['EXIF FNumber']
    iso = tags['EXIF ISOSpeedRatings']
    lens = tags['EXIF LensModel']

    # generate a htlm table
    table = f"""
            <table>
            <tr><td>Settings</td><td><b>ISO {iso} {focallength}
            mm f/{aperture} {shutterspeed} sec </b></td></tr>
            <tr><td>Camera</td><td><b>{brand} {model}</b></td></tr>
            <tr><td>Lens</td><td><b>{lens}</b></td></tr>
            <tr><td>Date</td><td><b>{date}</b></td></tr>
            </table>"""

    return table


def process_image(filename):
    # Open image file for reading (binary mode)
    f = open(filename, 'rb')

    # Return Exif tags
    tags = exifread.process_file(f)
    return create_table(tags)

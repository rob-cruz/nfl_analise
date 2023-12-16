import requests

url = 'https://b.fssta.com/uploads/application/nfl/headshots/327297.vresize.72.72.medium.68.png'

r = requests.get(url)
with open('img.png', 'wb') as f:
    f.write(r.content)
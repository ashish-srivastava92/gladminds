from httplib2 import Http
from _pyio import open

h=Http()

POST_URL = 'http://api-qa.gladmindsplatform.co/api/v1/bajaj/feed/'
#POST_URL = 'http://127.0.0.1:8000/api/v1/bajaj/feed/'
def main():
    files = ['service_advisor_feed.xml', 'product_dispatch_feed.xml', 'product_purchase_feed.xml']
    for file in files:
        data = open(file, 'r')
        response = h.request(POST_URL, method="POST", body=str(data.read()))
        data.close()

if __name__ == '__main__':
    main()
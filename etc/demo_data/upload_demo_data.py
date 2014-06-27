from httplib2 import Http

def main():
    h = Http()

    POST_URL = 'http://api-qa.gladmindsplatform.co/api/v1/bajaj/feed/'
    # POST_URL = 'http://127.0.0.1:8000/api/v1/bajaj/feed/'
    files = ['etc/demo_data/service_advisor_feed.xml', 'etc/demo_data/product_dispatch_feed.xml', 'etc/demo_data/product_purchase_feed.xml']
    for file in files:
        data = open(file, 'r')
        response = h.request(POST_URL, method="POST", body=str(data.read()))
        data.close()
    print 'Success installed the data.'

if __name__ == '__main__':
    main()

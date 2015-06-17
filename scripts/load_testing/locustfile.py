from locust import HttpLocust, TaskSet, task
import logging, json

HEADER = {}
class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
#         response = self.login()
#         access_token = json.loads(response.content)['access_token']
#         global HEADER
#         HEADER = {"access_token": access_token}
        #coupons = self.get_coupons({"status":1,"limit":40})
        #print coupons
        pass

#     def login(self):
#         return self.client.post("/v1/gm-users/login/", json={"username":"bajaj", "password":"bajaj"})
#     
#     def get_coupons(self, filters):
#         filters.update(HEADER)
#         response = self.client.get("/v1/coupons/", params=filters)
#         coupons = json.loads(response.content)
#         return coupons

    @task(1)
    def messages(self):
        self.client.get("/v1/messages/", params={"cli":"+919953804414", "msg": "LOAD-ACTIVATES"})

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    host = "http://staging.bajaj.gladminds.co"
    min_wait=5000
    max_wait=9000
from locust import HttpUser, task, between
from random import randint as rand
from termcolor import colored


class WebsiteBlogger(HttpUser):
    
    wait_time = between(1,5)
    
    @task(4)
    def view_blogs_of_other_bloggers(self):
        print(colored("view blogs",'yellow'))
        id = rand(1, 18)
        self.client.get(
            f'/blogapp/blogger/{id}/blog/',
            name='blogger/:pk/blogs/'
        )

    @task(2)
    def view_blog_details(self):
        print(colored("view blog-details",'red'))
        blogger_id = rand(1, 18)
        blog_id = rand(1, 26)
        self.client.get(
            f'/blogapp/blogger/{id}/blog/{blog_id}',
            name='blogger/:blogger_pk/blog/:pk'
        )

    # def on_start(self):
    #     response = self.client.po
    def on_start(self):
        return super().on_start()
from locust import HttpUser, task, between
from random import choice, randint as rand
from termcolor import colored
# from blogapp.models import Blog


class WebsiteBlogger(HttpUser):
    
    wait_time = between(5,15)
    
    @task(4)
    def view_blogs_of_other_bloggers(self):
        print(colored("view blogs",'yellow'))
        id = rand(1, 18)
        self.client.get(
            f'/blogapp/bloggers/{id}/blog/',
            name='blogger/:blogger_pk/blog/'
        )

    @task(2)
    def view_blog_details(self):
        print(colored("view blog-details",'red'))
        blogger_id = rand(1, 18)
        # blog_id = choice(Blog.objects.select_related('creator').filter(creator__id=blogger_id).only('id'))
        blog_id = choice([26,27,28])
        # self.client.force_authorize()
        self.client.get(
            # f'/blogapp/bloggers/{blogger_id}/blog/{blog_id}',
            f'/blogapp/bloggers/{16}/blog/{blog_id}',
            name='blogger/:blogger_pk/blog/:pk'
        )

    # def on_start(self):
    #     response = self.client.po
    def on_start(self):
        self.client.headers.update({
            'Authorization':
            "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ2NDkxNzkxLCJqdGkiOiI4NzEwNTBmOTA3NmM0YjYzYTc1M2IxNDZlNzlkMWRjNSIsInVzZXJfaWQiOjE2fQ.Jzw14_TLXPFk2mx6jYT-2-jyrdD0WZMUs3_kiwCwwHg"
        })
        # self.blogger_id = self.client.user.id
        # http://localhost:8000
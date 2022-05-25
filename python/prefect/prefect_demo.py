# -*- coding: utf-8 -*-
"""
Created on Sat May 21 19:29:15 2022

@author: garym
"""

import prefect
from prefect import task, Flow
from prefect.tasks.notifications.email_task import  EmailTask

@task
def hello_task():
    logger = prefect.context.get("logger")
    logger.info("Hello world!")
    EmailTask(subject='API Stuff', msg='Test', email_to= 'garymanley@gmail.com', email_from="notifications@prefect.io", smtp_server="smtp.gmail.com", smtp_port=465, smtp_type="SSL")

flow = Flow("hello-flow", tasks=[hello_task])

flow.run()

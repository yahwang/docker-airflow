from airflow.models import BaseOperator
from airflow.plugins_manager import AirflowPlugin
from airflow.utils.decorators import apply_defaults
from airflow.hooks.http_hook import HttpHook
from airflow.contrib.hooks.slack_webhook_hook import SlackWebhookHook

class SlackWebhookHookFixed(SlackWebhookHook):
    def __init__(self,
                 http_conn_id=None,
                 webhook_token=None,
                 message="",
                 attachments=None,
                 channel=None,
                 username=None,
                 icon_emoji=None,
                 link_names=False,
                 proxy=None,
                 *args,
                 **kwargs
                 ):
        HttpHook.__init__(self, http_conn_id=http_conn_id, *args, **kwargs)
        self.webhook_token = self._get_token(webhook_token, http_conn_id)
        self.message = message
        self.attachments = attachments
        self.channel = channel
        self.username = username
        self.icon_emoji = icon_emoji
        self.link_names = link_names
        self.proxy = proxy

class SlackMsgOperator(BaseOperator):

    @apply_defaults
    def __init__(self, channel, username, user_msg, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel = channel
        self.username = username or 'airflow_bot'
        self.message = user_msg
        self.hook = SlackWebhookHookFixed(
            http_conn_id="slack_conn",
            channel=self.channel,
            username=self.username,
            message = self.message
        )

    def execute(self, context):
        self.hook.execute()
'''
# usage example
t1 = SlackMsgOperator(task_id="msg_test", 
        username='yahwang!!',
        channel='#airflow',
        user_msg='Hello world',
        dag=dag)
'''

class SlackPlugin(AirflowPlugin):
    name = "slack_plugin"
    hooks = [SlackWebhookHookFixed]
    operators = [SlackMsgOperator]


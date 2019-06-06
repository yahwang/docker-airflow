from airflow.hooks.base_hook import BaseHook
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator
from utils.slack_webhook_hook_fixed import SlackWebhookHookFixed
#from airflow.contrib.hooks.slack_webhook_hook import SlackWebhookHook


class SlackWebhookOperatorFixed(SlackWebhookOperator):
    def execute(self, context):
        self.hook = SlackWebhookHookFixed(
            self.http_conn_id,
            self.webhook_token,
            self.message,
            self.attachments,
            self.channel,
            self.username,
            self.icon_emoji,
            self.link_names,
            self.proxy
        )
        self.hook.execute()

class SlackAlert:
    def __init__(self, channel):
        self.channel = channel
        #self.webhook_token = BaseHook.get_connection('slack_conn').password

    def slack_fail_alert(self, context):
        alert = SlackWebhookOperatorFixed(
            task_id="slack_failed",
            http_conn_id="slack_conn",
            channel=self.channel,
            username='airflow_bot',
            message = """
                :red_circle: Task Failed. 
                *Task*: {task}  
                *Dag*: {dag} 
                *Execution Time*: {exec_date}  
                *Log Url*: {log_url} 
                """.format(
                task=context.get('task_instance').task_id,
                dag=context.get('task_instance').dag_id,
                ti=context.get('task_instance'),
                exec_date=context.get('execution_date'),
                log_url=context.get('task_instance').log_url,
            )
        )
        return alert.execute(context=context)
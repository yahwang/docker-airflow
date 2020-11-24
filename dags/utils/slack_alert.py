from airflow.hooks import SlackWebhookHookFixed

class SlackAlert:
    def __init__(self, channel):
        self.channel = channel

    def slack_fail_alert(self, context):
        alert = SlackWebhookHookFixed(
            http_conn_id="slack-conn",
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
        return alert.execute()
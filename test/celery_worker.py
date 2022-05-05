import celery
import time
backend = 'redis://:redispasswd@172.16.0.150:30993/9'
broker = 'redis://:redispasswd@172.16.0.150:30993/9'
cel = celery.Celery('test', backend=backend, broker=broker)
cel.conf.update(
    broker_transport_options={'visibility_timeout': 60 * 60 * 24 * 30},
)
@cel.task
def send_email(name):
    print("向%s发送邮件..."%name)
    time.sleep(10)
    print("向%s发送邮件完成"%name)
    return "ok"



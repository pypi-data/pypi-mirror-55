import requests, json, heapq
from operator import itemgetter
from mg_app_framework import get_logger
from .port_detect import is_port_open
from .weixin_alarm import send_alarm


def get_rabbitmq_url(ip: str, port: str) -> str:
    return "http://" + ip + ":" + port


async def start_detect_rabbitmq_cluster(cluster_name: str, cluster_ip_port: str, rabbitmq_user: str,
                                        rabbitmq_password: str, max_msg_num: str, is_product_env: str = True) -> None:
    await detect_rabbitmq_cluster_port_status(cluster_name, cluster_ip_port)
    await get_rabbitmq_cluster_overview_info(cluster_name, cluster_ip_port, rabbitmq_user, rabbitmq_password,
                                             max_msg_num, is_product_env=is_product_env)


async def detect_rabbitmq_cluster_port_status(cluster_name: str, cluster_ip_port: str) -> None:
    # 检测集群端口状态
    for ip, port_list in cluster_ip_port.items():
        for port in port_list:
            if await is_port_open(ip, port):
                alarm_message = '{}{}节点端口{}服务正常'.format(cluster_name, ip, port)
            else:
                alarm_message = '{}{}节点端口{}服务异常'.format(cluster_name, ip, port)
                await send_alarm(alarm_message)
            get_logger().info(alarm_message)


async def get_rabbitmq_cluster_overview_info(cluster_name: str, cluster_ip_port: str, rabbitmq_user: str,
                                             rabbitmq_password: str, max_msg_num: str,
                                             is_product_env: str = True) -> None:
    for ip, port_list in cluster_ip_port.items():
        url = get_rabbitmq_url(ip, '15672') + "/api/overview"
        get_logger().info('url:%s', url)
        res = requests.get(url, auth=(rabbitmq_user, rabbitmq_password))
        overview = json.loads(res.text)
        messages_ready = overview['queue_totals']['messages_ready']

        if int(messages_ready) > max_msg_num:
            alarm_message = '{}{}节点未消费消息数大于{}'.format(cluster_name, ip, max_msg_num)
            await send_alarm(alarm_message)
            if not is_product_env:
                await delete_max_msg_queue(cluster_name, ip, rabbitmq_user, rabbitmq_password)


async def delete_max_msg_queue(cluster_name: str, ip: str, rabbitmq_user: str, rabbitmq_password: str) -> None:
    '''
    删除没有消费者的队列，生产环境慎用！！！
    :param cluster_name:
    :param ip:
    :param rabbitmq_user:
    :param rabbitmq_password:
    :return:
    '''
    url = get_rabbitmq_url(ip, '15672') + "/api/queues"
    res = requests.get(url, auth=(rabbitmq_user, rabbitmq_password))
    queue_overview = json.loads(res.text)

    for q in heapq.nlargest(3, queue_overview, key=itemgetter('messages_ready', 'consumers')):
        if not q['consumers']:
            name, messages_ready = q['name'], q['messages_ready']
            url1 = get_rabbitmq_url(ip, '15672') + "/api/queues/%2F/" + name
            para = {'mode': "delete", 'name': name, 'vhost': "/"}
            res = requests.delete(url1, params=para, auth=(rabbitmq_user, rabbitmq_password))
            if res.status_code == 204:
                alarm_message = '{}{}节点队列{}未消费消息数{},已删除'.format(cluster_name, ip, name, messages_ready)
                get_logger().info('delete queue:%s', q)
                await send_alarm(alarm_message)
                break

import traceback
from datetime import datetime as dt
from tornado.httpclient import AsyncHTTPClient
from mg_app_framework import get_store, get_logger, HttpClient


async def send_alarm(alarm_message: str):
    get_logger().warn(alarm_message)
    await send_msg_to_proxy('1000017', alarm_message)


async def send_msg_to_proxy(agent_id: str, content: str, content_type: str = 'text') -> None:
    data = {'agent_id': agent_id, 'msg_type': 'weixin', 'content_type': content_type, 'content': {'text': content}}
    get_logger().info('send http msg to proxy. data: {}'.format(data))
    client = HttpClient(AsyncHTTPClient(max_clients=1000, force_instance=True))
    url = get_store().get_monitor_proxy_msg_url()
    try:
        await client.post(url, data=data, connect_timeout=5, request_timeout=5)
    except:
        traceback.print_exc()
        get_logger().warn('send wx msg to proxy fail, url:%s', url)

    client.close()


async def send_daily_status(cluster_name: str, app_name: str) -> None:
    # 每天06:00报告ａｐｐ状态
    if '0600' == dt.now().strftime('%H%M'):
        msg = '{} {} app 正常工作中'.format(cluster_name, app_name)
        await send_alarm(msg)

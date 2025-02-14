"""
Date: 2023-11-13 20:29:19
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2023-11-13 20:29:58
"""
import asyncio

from utils.api.login import Login
from utils.api.sign import BaseSign
from utils.config import ConfigManager
from utils.logger import log, get_message
from utils.request import notify_me
from utils.utils import get_token
from utils.system_info import print_info

_conf = ConfigManager.data_obj


async def main():
    print_info()
    for account in _conf.accounts:
        login_obj = Login(account)
        if (cookies := await login_obj.login()) and (token := await get_token(cookies["cUserId"])):
            sign_obj = BaseSign(cookies)
            daily_tasks = await sign_obj.check_daily_tasks()
            sign_task_obj = sign_obj.AVAILABLE_SIGNS  # 签到任务对象合集
            for task in daily_tasks:
                if not task.showType:
                    log.info(f"开始执行{task.name}任务")
                    if task_obj := sign_task_obj.get(task.name):  # 签到任务对象
                        await task_obj(cookies, token).sign()
                    else:
                        log.error(f"未找到{task.name}任务")
                else:
                    log.info(f"{task.name}任务已完成")
    notify_me(get_message())


if __name__ == "__main__":
    asyncio.run(main())

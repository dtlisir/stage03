# -*- coding: utf-8 -*-
# 该示例中使用云API V2版本

from home_application.models import CapacityData
from config import APP_CODE, SECRET_KEY


def get_job_instance_id(client, biz_id, ip, job_id=0, script_id=0):  # 作业ID和脚本ID二选一
    """
    执行Job作业/script脚本
    """
    if job_id:
        # 获取作业模板参数详情
        kwargs = {
            'bk_app_code': APP_CODE,
            'bk_app_secret': SECRET_KEY,
            'bk_biz_id': biz_id,
            'bk_job_id': job_id,
        }
        resp = client.job.get_job_detail(kwargs)

        steps_args = []
        if resp.get('result'):
            data = resp.get('data', {})
            steps = data.get('steps', [])
            # 组装步骤参数
            for _step in steps:
                steps_args.append(
                    {
                        'step_id': int(_step.get('step_id')),
                        'ip_list': [{
                            'bk_cloud_id': 0,
                            'ip': ip,
                        }],
                    }
                )

        # 执行作业
        kwargs = {
            'bk_app_code': APP_CODE,
            'bk_app_secret': SECRET_KEY,
            'bk_biz_id': biz_id,
            'bk_job_id': job_id,
            'steps': steps_args,
        }
        resp = client.job.execute_job(kwargs)
        if resp.get('result'):
            job_instance_id = resp.get('data').get('job_instance_id')
        else:
            job_instance_id = -1

        return resp.get('result'), job_instance_id

    if script_id:
        kwargs = {
            'bk_app_code': APP_CODE,
            'bk_app_secret': SECRET_KEY,
            'bk_biz_id': biz_id,
            'script_id': script_id,
            'account': "root",
            'ip_list': [{"bk_cloud_id": 0, "ip": ip}]
        }
        resp = client.job.fast_execute_script(kwargs)
        if resp.get('result'):
            job_instance_id = resp.get('data').get('job_instance_id')
        else:
            job_instance_id = -1

        return resp.get('result'), job_instance_id


def get_host_capaticy(client, biz_id, job_instance_id, ip):
    """
    获取磁盘容量数据
    """
    kwargs = {
        'bk_app_code': APP_CODE,
        'bk_app_secret': SECRET_KEY,
        'bk_biz_id': biz_id,
        'job_instance_id': job_instance_id,
    }
    resp = client.job.get_job_instance_log(kwargs)

    is_finish = False
    capacity_data = []
    if resp.get('result'):
        data = resp.get('data')
        logs = ''
        for _d in data:
            if _d.get('is_finished'):
                is_finish = True
                logs = _d['step_results'][0].get('ip_logs')[0].get('log_content')
                break

        logs = logs.split('\n')
        logs = [_l.split(' ') for _l in logs]

        for log in logs[2:]:
            _l_new = [_l for _l in log if _l != '']
            if _l_new and len(_l_new) >= 5:
                capacity_data.append({
                    'ip': ip,
                    'Filesystem': _l_new[0],
                    'Size': _l_new[1],
                    'Used': _l_new[2],
                    'Avail': _l_new[3],
                    'Use%': _l_new[4],
                    'Mounted': _l_new[5],

                })
                # 数据入库
                _l_new.append(ip)
                CapacityData.objects.save_data(_l_new)
    return is_finish, capacity_data

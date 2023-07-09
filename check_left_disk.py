from airflow.decorators import task

@task
def check_left_dist_and_send_to_slack(error_msg, pass_msg):
    from airflow.models import Variable
    import psutil
    import requests
    import json
    import logging

    logging.info("disk_check_start")

    # 디스크 사용량 확인
    disk_usage = psutil.disk_usage('/')

    # 전체와 사용 가능한 디스크 공간 계산
    total_disk = disk_usage.total / (1024**2)  # MB 단위로 변환
    used_disk = disk_usage.used / (1024**2)  # MB 단위로 변환

    percentage_used = (used_disk / total_disk) * 100

    print(f"Total disk: {total_disk:.2f}MB, Used disk: {used_disk:.2f}MB, Percentage used: {percentage_used:.2f}%")

    slack_webhook_url = Variable.get("gm_slack_url")
    headers = {'Content-type': 'application/json'}

    # 디스크 사용량이 90% 이상일 때 슬랙으로 알림 보내기
    if percentage_used >= 90:
        if error_msg == None:
            error_msg = f":warning: Warning: Disk usage is {percentage_used:.2f}%!!, GCP 인스턴스 확인 바람"
        
        data = {'text': error_msg}
        response = requests.post(slack_webhook_url, headers=headers, data=json.dumps(data))
    else:
        if pass_msg == None:
            pass_msg = f":smile: good: Disk usage is {percentage_used:.2f}"

        data = {'text': pass_msg}
        response = requests.post(slack_webhook_url, headers=headers, data=json.dumps(data))


    logging.info("disk_check_end")

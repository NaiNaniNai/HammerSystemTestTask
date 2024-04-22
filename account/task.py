from project_root.celery import app


@app.task
def send_sms_code():
    print("Имитация отправки сообщения")

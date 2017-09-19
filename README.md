# celery

安装
```
	python3 setup.py install
```


关于启动
```
celery -A proj worker -l info -n worker.%h -Q celery
```
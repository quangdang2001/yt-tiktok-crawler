from crontab import CronTab

cron = CronTab(tabfile="test.txt")
job = cron.new(command="echo hello_world")
job.minute.every(1)
cron.write()
cron.remove_all()

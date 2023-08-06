from fabric import Connection


result=Connection('10.1.143.179',user='ubuntu').run('sudo fdisk -l',hide=True)
msg="Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
print(msg.format(result))

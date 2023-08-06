from fabric import Connection
from lgblkb_tools.common.proxies import RecursiveProxy

class FabricConnection(RecursiveProxy):
	def __init__(self,host,user=None,port=None,config=None,gateway=None,forward_agent=None,
	             connect_timeout=None,connect_kwargs=None,inline_ssh_env=None,):
		wrapped=Connection(host,user=user,port=port,config=config,gateway=gateway,forward_agent=forward_agent,
		                   connect_timeout=connect_timeout,connect_kwargs=connect_kwargs,inline_ssh_env=inline_ssh_env,)
		super(FabricConnection,self).__init__(wrapped=wrapped)
	
	pass

result=FabricConnection('10.1.143.179',user='ubuntu').run('sudo fdisk -l',hide=True)
msg="Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
print(msg.format(result))

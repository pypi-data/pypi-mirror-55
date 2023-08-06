import wrapt

basic_excludes=(int,float,str,bool)

def _wrap_make_out():
	@wrapt.decorator
	def wrapper(wrapped,instance,args,kwargs):
		return instance.make_out(wrapped(*args,**kwargs))
	
	return wrapper

# noinspection PyAbstractClass
class RecursiveProxy(wrapt.ObjectProxy):
	exclude=()
	wrap_only=()
	
	def __init__(self,wrapped,*setup_args,**setup_kwargs):
		super().__init__(wrapped)
		self._self_exclude=tuple({*basic_excludes,*self.exclude})
		self._self_wrap_only=tuple(self.wrap_only)
		self.proxy_setup(*setup_args,**setup_kwargs)
	
	def proxy_setup(self,*args,**kwargs):
		pass
	
	def __call__(self,*args,**kwargs):
		return self.__make_out(self.__wrapped__.__call__(*args,**kwargs))
	
	def make_out(self,out):
		return out
	
	@_wrap_make_out()
	def __make_out(self,out):
		if self._self_wrap_only:
			if isinstance(out,self._self_wrap_only):
				return self._class_(out)
			else:
				return out
		elif isinstance(out,self._self_exclude):
			return out
		else:
			return type(self)(out)
	
	def __getattr__(self,item):
		if item.startswith('_self_'):
			return super().__getattr__(item)
		else:
			return self.__make_out(getattr(self.__wrapped__,item))
	
	@property
	def the_obj(self):
		return self.__wrapped__
	
	def __reduce_ex__(self,protocol):
		args=(self.__wrapped__,)
		return type(self),args

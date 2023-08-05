import builtins
from collections.abc import Iterable


class Template:
	def __init__(self, builtin_function):
		self.builtin_function = builtin_function

	def __call__(self, *args):
		return self.builtin_function(*args)

	def __getitem__(self, args):
		if isinstance(args, Iterable):
			old = self.builtin_function(*args)
			new = self.builtin_function(old.start, old.stop + 1, old.step)
		else:
			old = self.builtin_function(args)
			new = self.builtin_function((old.start or 0) + 1, old.stop + 1, old.step)
		return new


range = Template(builtins.range)
slice = Template(builtins.slice)

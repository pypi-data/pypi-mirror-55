import markovify

def load_from_filename(filename,cls=markovify.Text,*args,**kwargs):
	with open(filename) as f:
		return cls(f.read(),*args,**kwargs)

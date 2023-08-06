from IPython.core.display import display, HTML

d = lambda _response: display(HTML(_response.content.decode('utf-8')))
pt = lambda _x: print(type(x))
pd = lambda _x: print(dir(x))

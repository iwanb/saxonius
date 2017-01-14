# Python 3 bindings for Saxon using pyJNIus

It loosely mirrors the Saxon API objects but with Python style, starting with the [Processor](http://www.saxonica.com/documentation9.5/javadoc/net/sf/saxon/s9api/Processor.html) class.

Example:

```python
from saxonius import Processor

p = Processor()
doc = p.document_build('''
<document>
  <node>Hello</node>
  <node>world</node>
</document>
''')
r = p.xquery_compile('/document/node/text()').evaluate(context_item=doc)
print(str(r[0]))
```

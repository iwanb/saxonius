from jnius import autoclass, java_method, PythonJavaClass, JavaException, cast

# Exceptions
class SaxonApiError(Exception):
    pass

# Java interfaces
class _catch(object):
    def __enter__(self):
        pass
    def __exit__(self, exc_type, e, traceback):
        if exc_type is not JavaException:
            return None
        if e.classname == "java.lang.IndexOutOfBoundsException":
            raise IndexError
        if e.classname != "net.sf.saxon.s9api.SaxonApiException":
            raise RuntimeError('JNI error') from e
        raise SaxonApiError(e.innermessage) from e
_catcher = _catch()

_Processor = autoclass('net.sf.saxon.s9api.Processor')
_File = autoclass('java.io.File')
_StreamSource = autoclass('javax.xml.transform.stream.StreamSource')
_StringReader = autoclass('java.io.StringReader')

# Python API
class Processor(object):
    def __init__(self, config=None, licensedEdition=False):
        if config is not None:
            # TODO
            raise NotImplementedError
        else:
            self._processor = _Processor(licensedEdition)
    def xquery_compiler(self, **kwargs):
        """Create an XQueryCompiler."""
        compiler = self._processor.newXQueryCompiler()
        return XQueryCompiler(compiler, **kwargs)
    def xquery_compile(self, query, **kwargs):
        """Shortcut for xquery_compiler().compile()."""
        return self.xquery_compiler(**kwargs).compile(query)
    def document_builder(self, **kwargs):
        """Create a DocumentBuilder."""
        db = self._processor.newDocumentBuilder(**kwargs)
        return DocumentBuilder(db)
    def document_build(self, xml, **kwargs):
        """Shortcut for document_builder().build()."""
        return self.document_builder(**kwargs).build(xml)
    def document_build_file(self, filename, **kwargs):
        """Shortcut for document_builder().build_file()."""
        return self.document_builder(**kwargs).build_file(filename)

# XQuery processor
class XQueryCompiler(object):
    def __init__(self, compiler):
        self._compiler = compiler
    def compile(self, query):
        """Compile a query supplied as a string."""
        with _catcher:
            executable = self._compiler.compile(query)
        return XQueryExecutable(executable)

class XQueryExecutable(object):
    def __init__(self, executable):
        self._executable = executable
    def load(self, **kwargs):
        """"Load the stylesheet to prepare it for execution."""
        evaluator = self._executable.load()
        return XQueryEvaluator(evaluator, **kwargs)
    def evaluate(self, **kwargs):
        """Evaluate a query."""
        return self.load(**kwargs).evaluate()
    def evaluate_single(self, **kwargs):
        """Evaluate a query, returning a single XDMItem."""
        return self.load(**kwargs).evaluate_single()
class XQueryEvaluator(object):
    def __init__(self, evaluator, **kwargs):
        self._evaluator = evaluator
        for (k, v) in kwargs.items():
            setattr(self, k, v)
    def evaluate(self):
        """Perform the query, returning the results as an XdmValue."""
        with _catcher:
            value = self._evaluator.evaluate()
        return XdmValue(value)
    def evaluate_single(self):
        """Perform the query, returning the results as an XdmValue."""
        with _catcher:
            item = self._evaluator.evaluateSingle()
        return XdmItem(item)
    @property
    def context_item(self):
        item = self._evaluator.getContextItem()
        if item is None:
            return None
        return XdmItem(item)
    @context_item.setter
    def context_item(self, item):
        self._evaluator.setContextItem(item._value)

# Document builder
class DocumentBuilder(object):
    def __init__(self, docbuilder, **kwargs):
        self._docbuilder = docbuilder
        for (k, v) in kwargs.items():
            setattr(self, k, v)
    def build(self, xml):
        s = _StreamSource(cast('java.io.Reader', _StringReader(xml)))
        with _catcher:
            node = self._docbuilder.build(s)
        return XdmNode(node)
    def build_file(self, filename):
        with _catcher:
            jfname = _File(filename)
            node = self._docbuilder.build(jfname)
        return XdmNode(node)
    @property
    def dtd_validation(self):
        return self._evaluator.getDTDValidation()
    @dtd_validation.setter
    def dtd_validation(self, validation):
        self._evaluator.setDTDValidation(validation)

# Xdm types
class XdmValue(object):
    def __init__(self, value):
        self._value = value
    def __len__(self):
        return self._value.size()
    def __iter__(self):
        return XdmSequenceIterator(self._value.iterator())
    def __getitem__(self, key):
        if key < 0:
            key = len(self) + key
        with _catcher:
            item = self._value.itemAt(key)
        return XdmItem(item)
    def __str__(self):
        return self._value.toString()
class XdmItem(XdmValue):
    def __str__(self):
        return self._value.getStringValue()
    @property
    def atomic(self):
        return self._value.isAtomic()
class XdmNode(XdmItem):
    pass
class XdmSequenceIterator(object):
    def __init__(self, iterator):
        self._iterator = iterator
    def __iter__(self):
        return self
    def __next__(self):
        if not self._iterator.hasNext():
            raise StopIteration
        return XdmItem(self._iterator.next())

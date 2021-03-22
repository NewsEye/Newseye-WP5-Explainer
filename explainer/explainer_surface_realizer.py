from explainer.core.surface_realizer import SurfaceRealizer


class ExplainerBodySurfaceUnorderedRealizer(SurfaceRealizer):
    doc_start = "<ul>"
    doc_end = "</ul>"
    paragraph_start = "<li>"
    paragraph_end = "</li>"
    sentence_end = " "
    sentence_start = ""
    fail_on_empty = False


class ExplainerBodySurfaceOrderedRealizer(SurfaceRealizer):
    doc_start = "<ol>"
    doc_end = "</ol>"
    paragraph_start = "<li>"
    paragraph_end = "</li>"
    sentence_end = " "
    sentence_start = ""
    fail_on_empty = False

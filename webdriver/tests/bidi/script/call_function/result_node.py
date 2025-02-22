import pytest
from webdriver.bidi.modules.script import ContextTarget

from ... import any_string, recursive_compare


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "function_declaration, expected",
    [
        (   # basic
            """
                () => document.querySelector("br")
            """,
            {
                "type": "node",
                "sharedId": any_string,
                "value": {
                    "attributes": {},
                    "childNodeCount": 0,
                    "children": [],
                    "localName": "br",
                    "namespaceURI": "http://www.w3.org/1999/xhtml",
                    "nodeType": 1,
                },
            },
        ),
        (   # attributes
            """
                () => document.querySelector("svg")
            """,
            {
                "type": "node",
                "sharedId": any_string,
                "value": {
                    "attributes": {
                        "svg:foo": "bar",
                    },
                    "childNodeCount": 0,
                    "children": [],
                    "localName": "svg",
                    "namespaceURI": "http://www.w3.org/2000/svg",
                    "nodeType": 1,
                },
            },
        ),
        (   # all children including non-element nodes
            """
                () => document.querySelector("#with-text-node")
            """,
            {
                "type": "node",
                "sharedId": any_string,
                "value": {
                    "attributes": {"id": "with-text-node"},
                    "childNodeCount": 1,
                    "children": [{
                        "type": "node",
                        "sharedId": any_string,
                        "value": {
                            "childNodeCount": 0,
                            "nodeType": 3,
                            "nodeValue": "Lorem",
                        }
                    }],
                    "localName": "div",
                    "namespaceURI": "http://www.w3.org/1999/xhtml",
                    "nodeType": 1,
                },
            },
        ),
        (   # children limited due to max depth
            """
                () => document.querySelector("#with-children")
            """,
            {
                "type": "node",
                "sharedId": any_string,
                "value": {
                    "attributes": {"id": "with-children"},
                    "childNodeCount": 2,
                    "children": [{
                        "type": "node",
                        "sharedId": any_string,
                        "value": {
                            "attributes": {},
                            "childNodeCount": 1,
                            "localName": "p",
                            "namespaceURI": "http://www.w3.org/1999/xhtml",
                            "nodeType": 1
                        }
                    }, {
                        "type": "node",
                        "sharedId": any_string,
                        "value": {
                            "attributes": {},
                            "childNodeCount": 0,
                            "localName": "br",
                            "namespaceURI": "http://www.w3.org/1999/xhtml",
                            "nodeType": 1
                        }
                    }],
                    "localName": "div",
                    "namespaceURI": "http://www.w3.org/1999/xhtml",
                    "nodeType": 1,
                },
            },
        ),
        (   # not connected
            """
                () => document.createElement("div")
            """,
            {
                "type": "node",
                "sharedId": any_string,
                "value": {
                    "attributes": {},
                    "childNodeCount": 0,
                    "children": [],
                    "localName": "div",
                    "namespaceURI": "http://www.w3.org/1999/xhtml",
                    "nodeType": 1,
                },
            },
        ),
    ], ids=[
        "basic",
        "attributes",
        "all_children",
        "children_max_depth",
        "not_connected",
    ]
)
async def test_element_node(
    bidi_session, get_test_page, top_context, function_declaration, expected
):
    await bidi_session.browsing_context.navigate(
        context=top_context['context'], url=get_test_page(), wait="complete"
    )

    result = await bidi_session.script.call_function(
        function_declaration=function_declaration,
        target=ContextTarget(top_context["context"]),
        await_promise=False,
    )

    recursive_compare(expected, result)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "function_declaration, expected",
    [
        (
            """
                () => document.querySelector("input#button").attributes[0]
            """,
            {
                "type": "node",
                "sharedId": any_string,
                "value": {
                    "childNodeCount": 0,
                    "children": [],
                    "localName": "id",
                    "namespaceURI": None,
                    "nodeType": 2,
                    "nodeValue": "button",
                },
            },
        ), (
            """
                () => document.querySelector("svg").attributes[0]
            """,
            {
                "type": "node",
                "sharedId": any_string,
                "value": {
                    "childNodeCount": 0,
                    "children": [],
                    "localName": "foo",
                    "namespaceURI": "http://www.w3.org/2000/svg",
                    "nodeType": 2,
                    "nodeValue": "bar",
                },
            },
        ),
    ], ids=[
        "basic",
        "namespace",
    ]
)
async def test_attribute_node(
    bidi_session, get_test_page, top_context, function_declaration, expected
):
    await bidi_session.browsing_context.navigate(
        context=top_context['context'], url=get_test_page(), wait="complete"
    )

    result = await bidi_session.script.call_function(
        function_declaration=function_declaration,
        target=ContextTarget(top_context["context"]),
        await_promise=False,
    )

    recursive_compare(expected, result)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "function_declaration, expected",
    [
        (
            """
                () => document.querySelector("#with-text-node").childNodes[0]
            """,
            {
                "type": "node",
                "sharedId": any_string,
                "value": {
                    "childNodeCount": 0,
                    "children": [],
                    "nodeType": 3,
                    "nodeValue": "Lorem",
                }
            }
        ),
    ], ids=[
        "basic",
    ]
)
async def test_text_node(
    bidi_session, get_test_page, top_context, function_declaration, expected
):
    await bidi_session.browsing_context.navigate(
        context=top_context['context'], url=get_test_page(), wait="complete"
    )

    result = await bidi_session.script.call_function(
        function_declaration=function_declaration,
        target=ContextTarget(top_context["context"]),
        await_promise=False,
    )

    recursive_compare(expected, result)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "function_declaration, expected",
    [
        (
            """
                () => document.querySelector("foo").childNodes[1]
            """,
            {
                "type": "node",
                "sharedId": any_string,
                "value": {
                    "childNodeCount": 0,
                    "children": [],
                    "nodeType": 4,
                    "nodeValue": " < > & ",
                }
            }
        ),
    ], ids=[
        "basic",
    ]
)
async def test_cdata_node(bidi_session, inline, new_tab, function_declaration, expected):
    xml_page = inline("""<foo>CDATA section: <![CDATA[ < > & ]]>.</foo>""", doctype="xml")

    await bidi_session.browsing_context.navigate(
        context=new_tab['context'], url=xml_page, wait="complete"
    )

    result = await bidi_session.script.call_function(
        function_declaration=function_declaration,
        target=ContextTarget(new_tab["context"]),
        await_promise=False,
    )

    recursive_compare(expected, result)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "function_declaration, expected",
    [
        (
            """
                () => document.createProcessingInstruction("xml-stylesheet", "href='foo.css'")
            """,
            {
                "type": "node",
                "sharedId": any_string,
                "value": {
                    "childNodeCount": 0,
                    "children": [],
                    "nodeType": 7,
                    "nodeValue": "href='foo.css'",
                }
            }
        ),
    ], ids=[
        "basic",
    ]
)
async def test_processing_instruction_node(
    bidi_session, inline, new_tab, function_declaration, expected
):
    xml_page = inline("""<foo></foo>""", doctype="xml")

    await bidi_session.browsing_context.navigate(
        context=new_tab['context'], url=xml_page, wait="complete"
    )

    result = await bidi_session.script.call_function(
        function_declaration=function_declaration,
        target=ContextTarget(new_tab["context"]),
        await_promise=False,
    )

    recursive_compare(expected, result)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "function_declaration, expected",
    [
        (
            """
                () => document.querySelector("#with-comment").childNodes[0]
            """,
            {
                "type": "node",
                "sharedId": any_string,
                "value": {
                    "childNodeCount": 0,
                    "children": [],
                    "nodeType": 8,
                    "nodeValue": " Comment ",
                }
            }
        ),
    ], ids=[
        "basic",
    ]
)
async def test_comment_node(
    bidi_session, get_test_page, top_context, function_declaration, expected
):
    await bidi_session.browsing_context.navigate(
        context=top_context['context'], url=get_test_page(), wait="complete"
    )

    result = await bidi_session.script.call_function(
        function_declaration=function_declaration,
        target=ContextTarget(top_context["context"]),
        await_promise=False,
    )

    recursive_compare(expected, result)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "function_declaration, expected",
    [
        (
            """
                () => document
            """,
            {
                "type": "node",
                "sharedId": any_string,
                "value": {
                    "childNodeCount": 2,
                    "children": [{
                        "type": "node",
                        "sharedId": any_string,
                        "value": {
                            "childNodeCount": 0,
                            "nodeType": 10
                        }
                    }, {
                        "type": "node",
                        "sharedId": any_string,
                        "value": {
                            "attributes": {},
                            "childNodeCount": 2,
                            "localName": "html",
                            "namespaceURI": "http://www.w3.org/1999/xhtml",
                            "nodeType": 1
                        }
                    }],
                    "nodeType": 9
                }
            }
        ),
    ], ids=[
        "basic",
    ]
)
async def test_document_node(
    bidi_session, get_test_page, top_context, function_declaration, expected
):
    await bidi_session.browsing_context.navigate(
        context=top_context['context'], url=get_test_page(), wait="complete"
    )

    result = await bidi_session.script.call_function(
        function_declaration=function_declaration,
        target=ContextTarget(top_context["context"]),
        await_promise=False,
    )

    recursive_compare(expected, result)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "function_declaration, expected",
    [
        (
            """
                () => document.doctype
            """,
            {
                "type": "node",
                "sharedId": any_string,
                "value": {
                    "childNodeCount": 0,
                    "children": [],
                    "nodeType": 10,
                }
            }
        ),
    ], ids=[
        "basic",
    ]
)
async def test_doctype_node(
    bidi_session, get_test_page, top_context, function_declaration, expected
):
    await bidi_session.browsing_context.navigate(
        context=top_context['context'], url=get_test_page(), wait="complete"
    )

    result = await bidi_session.script.call_function(
        function_declaration=function_declaration,
        target=ContextTarget(top_context["context"]),
        await_promise=False,
    )

    recursive_compare(expected, result)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "function_declaration, expected",
    [
        (
            """
                () => document.querySelector("#custom-element").shadowRoot
            """,
            {
                "type": "node",
                "sharedId": any_string,
                "value": {
                    "childNodeCount": 1,
                    "children": [{
                        "type": "node",
                        "sharedId": any_string,
                        "value": {
                            "attributes": {"id": "in-shadow-dom"},
                            "childNodeCount": 1,
                            "localName": "div",
                            "namespaceURI": "http://www.w3.org/1999/xhtml",
                            "nodeType": 1
                        }
                    }],
                    "nodeType": 11
                }
            }
        ),
        (
            """
                () => document.createDocumentFragment()
            """,
            {
                "type": "node",
                "sharedId": any_string,
                "value": {
                    "childNodeCount": 0,
                    "children": [],
                    "nodeType": 11,
                }
            }
        ),
    ], ids=[
        "shadow root",
        "not connected",
    ]
)
async def test_document_fragment_node(
    bidi_session, get_test_page, top_context, function_declaration, expected
):
    await bidi_session.browsing_context.navigate(
        context=top_context['context'], url=get_test_page(), wait="complete"
    )

    result = await bidi_session.script.call_function(
        function_declaration=function_declaration,
        target=ContextTarget(top_context["context"]),
        await_promise=False,
    )

    recursive_compare(expected, result)


@pytest.mark.asyncio
async def test_node_within_object(bidi_session, get_test_page, top_context):
    await bidi_session.browsing_context.navigate(
        context=top_context['context'], url=get_test_page(), wait="complete"
    )

    result = await bidi_session.script.call_function(
        function_declaration="""() => ({"elem": document.querySelector("img")})""",
        target=ContextTarget(top_context["context"]),
        await_promise=False,
    )

    expected = {
        "type": "object",
        "value": [
            ["elem", {
                "type": "node",
                "sharedId": any_string,
                "value": {
                    "attributes": {},
                    "childNodeCount": 0,
                    "localName": "img",
                    "namespaceURI": "http://www.w3.org/1999/xhtml",
                    "nodeType": 1
                }
            }]
        ]
    }

    recursive_compare(expected, result)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "function_declaration, expected",
    [
        (
            "() => document.getElementsByTagName('img')",
            {
                "type": "htmlcollection",
                "value": [
                    {
                        "type": "node",
                        "sharedId": any_string,
                        "value": {
                            "attributes": {},
                            "childNodeCount": 0,
                            "localName": "img",
                            "namespaceURI": "http://www.w3.org/1999/xhtml",
                            "nodeType": 1
                        }
                    },
                ]
            }
        ),
        (
            "() => document.querySelectorAll('img')",
            {
                "type": "nodelist",
                "value": [
                    {
                        "type": "node",
                        "sharedId": any_string,
                        "value": {
                            "attributes": {},
                            "childNodeCount": 0,
                            "localName": "img",
                            "namespaceURI": "http://www.w3.org/1999/xhtml",
                            "nodeType": 1
                        }
                    },
                ]
            }
        ),
    ], ids=[
        "htmlcollection",
        "nodelist"
    ]
)
async def test_node_within_dom_collection(
    bidi_session,
    get_test_page,
    top_context,
    function_declaration,
    expected
):
    await bidi_session.browsing_context.navigate(
        context=top_context['context'], url=get_test_page(), wait="complete"
    )

    result = await bidi_session.script.call_function(
        function_declaration=function_declaration,
        target=ContextTarget(top_context["context"]),
        await_promise=False,
    )

    recursive_compare(expected, result)

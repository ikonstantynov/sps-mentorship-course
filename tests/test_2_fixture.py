import uuid

from examples_for_testing.simple import check_log


def test_fixture(simple_fixture):
    """Basic (static) fixture."""

    assert 1 == simple_fixture


def test_fixture_with_param(api_gateway_request):
    """Fixture with takes parameters."""

    get_request = api_gateway_request()

    assert get_request == {
            'body': {},
            'pathParameters': None,
            'queryStringParameters': None
        }
    post_request = api_gateway_request({'key': 'value'})
    assert post_request == {
               'body': {'key': 'value'},
               'pathParameters': None,
               'queryStringParameters': None
           }


def test_param(positive_integer):
    """Fixture which generate parameters, will be called multiple times."""
    assert positive_integer > 0


def test_build_in_fixture_monkeypatch(monkeypatch):
    """Using monkeypatch."""
    def mockreturn():
        return '1234-1234-1234-1234'
    monkeypatch.setattr(uuid, 'uuid4', mockreturn)
    x = uuid.uuid4()
    assert x == '1234-1234-1234-1234'


def test_build_in_fixture_tmpdir(tmpdir):
    """Using temporary directory."""
    p = tmpdir.mkdir("sub").join("hello.txt")
    p.write("content")
    assert p.read() == "content"
    assert len(tmpdir.listdir()) == 1


def test_build_in_fixture_caplog(caplog):
    """Access and control log capturing."""
    check_log()
    logs = caplog.records
    assert logs[0].levelname == 'WARNING'
    assert logs[0].msg == 'Wrong action.'

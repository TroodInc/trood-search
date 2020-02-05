from search.parsers import RQL2SQLParser, RQL2SphinxQLParser


def test_rql2sql():
    parser = RQL2SQLParser("eq(a,1)")
    sql_query = parser.make_query()
    assert sql_query == "a = 1"

    parser = RQL2SQLParser("eq(a,тест поиска)")
    sql_query = parser.make_query()
    assert sql_query == "a = 'тест поиска'"

    parser = RQL2SQLParser("eq(a,xxx yyy)")
    sql_query = parser.make_query()
    assert sql_query == "a = 'xxx yyy'"

    parser = RQL2SQLParser("ne(a,1)")
    sql_query = parser.make_query()
    assert sql_query == "a <> 1"

    parser = RQL2SQLParser("gt(a,1)")
    sql_query = parser.make_query()
    assert sql_query == "a > 1"

    parser = RQL2SQLParser("in(a,(1,2))")
    sql_query = parser.make_query()
    assert sql_query == "in(a,1,2)"

    parser = RQL2SQLParser("and(eq(a,1),eq(b,1))")
    sql_query = parser.make_query()
    assert sql_query == "(a = 1 and b = 1)"

    parser = RQL2SQLParser("or(eq(a,1),eq(b,1))")
    sql_query = parser.make_query()
    assert sql_query == "(a = 1 or b = 1)"

    parser = RQL2SQLParser("and(eq(a,1),eq(b,1),or(eq(a,1),eq(b,1)))")
    sql_query = parser.make_query()
    assert sql_query == "(a = 1 and b = 1 and (a = 1 or b = 1))"


def test_rql2sphinxql():
    parser = RQL2SphinxQLParser("eq(a,xxx)")
    sql_query = parser.make_query()
    assert sql_query == "(@a xxx)"

    parser = RQL2SphinxQLParser("ne(a,1)")
    sql_query = parser.make_query()
    assert sql_query == "(@a !1)"

    parser = RQL2SphinxQLParser("and(eq(a,1),eq(b,1))")
    sql_query = parser.make_query()
    assert sql_query == "((@a 1) (@b 1))"

    parser = RQL2SphinxQLParser("or(eq(a,1),eq(b,1))")
    sql_query = parser.make_query()
    assert sql_query == "((@a 1) | (@b 1))"

    parser = RQL2SphinxQLParser("and(eq(a,1),eq(b,1),or(eq(a,1),eq(b,1)))")
    sql_query = parser.make_query()
    assert sql_query == "((@a 1) (@b 1) ((@a 1) | (@b 1)))"

from typing import Union, Any


class CStatement:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return str(self.name)

    def __and__(self, other):
        return CStatement(f'{self.name} AND {other.name}')

    def __or__(self, other):
        return CStatement(f'{self.name} OR {other.name}')


class Column:
    '''
        Create column\n
        name - name of column\n
        c_type - column type (str, int)
    '''

    def __init__(self, name: str, c_type: Union[str, int]):
        self.name = name
        self.c_type = c_type

    def _check_tp(self, what: Any):
        if self.c_type == str:
            return _escape(what)
        else:
            return str(what)

    def __repr__(self) -> str:
        return f'{self.name}'

    def __hash__(self) -> str:
        return hash(self.name)

    def __eq__(self, what: Any) -> CStatement:
        return CStatement(f'`{self.name}`={self._check_tp(what)}')

    def __ne__(self, what: Any) -> CStatement:
        return CStatement(f'`{self.name}`<>{self._check_tp(what)}')

    def __lt__(self, what: Any) -> CStatement:
        return CStatement(f'`{self.name}`<{self._check_tp(what)}')

    def __gt__(self, what: Any) -> CStatement:
        return CStatement(f'`{self.name}`>{self._check_tp(what)}')

    def __le__(self, what: Any) -> CStatement:
        return CStatement(f'`{self.name}`<={self._check_tp(what)}')

    def __ge__(self, what: Any) -> CStatement:
        return CStatement(f'`{self.name}`>={self._check_tp(what)}')

    def __add__(self, what: Any) -> CStatement:
        return CStatement(f'`{self.name}`+{self._check_tp(what)}')

    def __sub__(self, what: Any) -> CStatement:
        return CStatement(f'`{self.name}`-{self._check_tp(what)}')

    def __mul__(self, what: Any) -> CStatement:
        return CStatement(f'`{self.name}`*{self._check_tp(what)}')

    def __div__(self, what: Any) -> CStatement:
        return CStatement(f'`{self.name}`/{self._check_tp(what)}')

    def __mod__(self, what: Any) -> CStatement:
        return CStatement(f'`{self.name}`%{self._check_tp(what)}')


class Table:
    '''
        Create table object.\n
        t_name - table name\n
        *columns - list/tuple of columns
    '''

    def __init__(self, t_name: str, *columns: Column):
        self._t_name = t_name
        self.attrs = {}

        for column in columns:
            self.attrs[column.name] = column

    def __getattr__(self, attr: str):
        return self.attrs[attr]

    def __repr__(self) -> str:
        return self._t_name


class Command:
    '''
        Set name and argv for SQL function\n
        Like a: Command('concat', 'SQL', 'is', 'cool')\n
        Will be translated to: CONCAT('SQL', 'is', 'cool')
    '''

    def __init__(self, name: str, *argv):
        self.name = name.upper()+'('
        self.name += ', '.join(map(self._command, argv)) + ')'

    def _command(self, value: Any) -> str:
        if isinstance(value, str):
            return _escape(value)
        else:
            return str(value)

    def __repr__(self) -> str:
        return self.name


class Query:
    def __init__(self, query: str):
        self.query = query

    def __repr__(self) -> str:
        return str(self.query)


class WHERE:
    def __init__(self, *pairs: CStatement):
        pairs = map(str, pairs)

        self.where = 'WHERE '
        self.where += ' AND '.join(pairs)

    def __repr__(self) -> str:
        return str(self.where)


class ORDER_BY:
    '''
        *columns - paste columns (Ex. tbl.id, tbl.name...)\n
        by - sort by (ASC or DESC)
    '''

    def __init__(self, *columns: Column, by: str = 'ASC'):
        columns = map(str, columns)

        self.cmd = 'ORDER BY '
        self.cmd += f"`{'`, `'.join(columns)}` {by}"

    def __repr__(self) -> str:
        return str(self.cmd)


def _escape(value: str) -> str:
    value = value.replace("'", "''")
    return f"'{value}'"


def _prepare_string(pairs: dict) -> list:
    statements = []

    for name, value in pairs.items():
        if not isinstance(name, str):
            if name.c_type == str:
                value = _escape(value)
        else:
            value = _escape(value) if isinstance(value, str) else str(value)

        statements.append(
            f"`{name}`={value}"
        )

    return statements

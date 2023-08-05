import sqlalchemy

from apistellar import validators
from apistellar.types import PersistentTypeMeta, PersistentType

__version__ = "0.0.1"

TypeMapping = {
    validators.Integer: lambda validator: sqlalchemy.Integer(),
    validators.String:
        lambda validator: sqlalchemy.String(length=validator.max_length),
    validators.FormatDateTime: lambda validator: sqlalchemy.DateTime(),
    validators.Boolean: lambda validator: sqlalchemy.Boolean(),
    validators.DateTime: lambda validator: sqlalchemy.DateTime(),
    validators.Date: lambda validator: sqlalchemy.Date(),
    validators.Time: lambda validator: sqlalchemy.Time(),
}


class SqlAlchemyTypeMeta(PersistentTypeMeta):

    def __new__(mcs, name, bases, attrs):
        cls = super(SqlAlchemyTypeMeta, mcs).__new__(mcs, name, bases, attrs)
        if not cls.validator.properties:
            return cls

        assert hasattr(cls, "TABLE"), \
            f"{cls} with SqlAlchemyTypeMeta need provide a 'TABLE' prop!"
        columns = []
        for name, validator in cls.validator.properties.items():
            kwargs = dict()
            for key, val in validator.kwargs.items():
                if key.startswith("orm_"):
                    kwargs[key.replace("orm_", "")] = val
            col_factory = TypeMapping.get(validator.__class__)
            assert col_factory is not None, f"Un support type: {validator.__class__}"
            columns.append(sqlalchemy.Column(name, col_factory(validator), **kwargs))
        table_name = getattr(cls, "TABLE")
        cls.model = sqlalchemy.Table(
            table_name,
            sqlalchemy.MetaData(),
            *columns
        )
        return cls


class SqlAlchemyType(PersistentType, metaclass=SqlAlchemyTypeMeta):
    """
    继承这个type，使用self.model获取orm的能力，可配合databases使用
    """
    pass


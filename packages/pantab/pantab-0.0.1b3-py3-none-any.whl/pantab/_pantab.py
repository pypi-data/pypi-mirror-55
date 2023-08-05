import collections
import pathlib
import shutil
import tempfile
import uuid
from typing import Dict, List, Union

import numpy as np
import pandas as pd
import tableauhyperapi as tab_api

__all__ = ["frame_to_hyper", "frame_from_hyper", "frames_from_hyper", "frames_to_hyper"]


# The Hyper API as of writing doesn't offer great hashability for column comparison
# so we create out namedtuple for that purpose
_ColumnType = collections.namedtuple("_ColumnType", ["type_", "nullability"])

_column_types = {
    "int16": _ColumnType(tab_api.SqlType.small_int(), tab_api.Nullability.NOT_NULLABLE),
    "int32": _ColumnType(tab_api.SqlType.int(), tab_api.Nullability.NOT_NULLABLE),
    "int64": _ColumnType(tab_api.SqlType.big_int(), tab_api.Nullability.NOT_NULLABLE),
    "Int16": _ColumnType(tab_api.SqlType.small_int(), tab_api.Nullability.NULLABLE),
    "Int32": _ColumnType(tab_api.SqlType.int(), tab_api.Nullability.NULLABLE),
    "Int64": _ColumnType(tab_api.SqlType.big_int(), tab_api.Nullability.NULLABLE),
    "float32": _ColumnType(tab_api.SqlType.double(), tab_api.Nullability.NULLABLE),
    "float64": _ColumnType(tab_api.SqlType.double(), tab_api.Nullability.NULLABLE),
    "bool": _ColumnType(tab_api.SqlType.bool(), tab_api.Nullability.NOT_NULLABLE),
    "datetime64[ns]": _ColumnType(
        tab_api.SqlType.timestamp(), tab_api.Nullability.NULLABLE
    ),
    "datetime64[ns, UTC]": _ColumnType(
        tab_api.SqlType.timestamp_tz(), tab_api.Nullability.NULLABLE
    ),
    "timedelta64[ns]": _ColumnType(
        tab_api.SqlType.interval(), tab_api.Nullability.NULLABLE
    ),
    "object": _ColumnType(tab_api.SqlType.text(), tab_api.Nullability.NULLABLE),
}


# Invert this, but exclude float32 as that does not roundtrip
_pandas_types = {v: k for k, v in _column_types.items() if k != "float32"}


TableType = Union[str, tab_api.Name, tab_api.TableName]


def _pandas_to_tableau_type(typ: str) -> _ColumnType:
    try:
        return _column_types[typ]
    except KeyError:
        raise TypeError("Conversion of '{}' dtypes not supported!".format(typ))


def _tableau_to_pandas_type(typ: tab_api.TableDefinition.Column) -> str:
    try:
        return _pandas_types[typ]
    except KeyError:
        return "object"


# The Hyper API doesn't expose these functions directly and wraps them with
# validation; we can skip the validation because the column dtypes enforce that
_insert_functions = {
    tab_api.SqlType.bool(): "_Inserter__write_bool",
    tab_api.SqlType.big_int(): "_Inserter__write_big_int",
    tab_api.SqlType.small_int(): "_Inserter__write_small_int",
    tab_api.SqlType.int(): "_Inserter__write_int",
    tab_api.SqlType.double(): "_Inserter__write_double",
    tab_api.SqlType.text(): "_Inserter__write_text",
    tab_api.SqlType.interval(): "_Inserter__write_interval",
    tab_api.SqlType.timestamp(): "_Inserter__write_timestamp",
    tab_api.SqlType.timestamp_tz(): "_Inserter__write_timestamp",
}


def _timedelta_to_interval(td: pd.Timedelta) -> tab_api.Interval:
    """Converts a pandas Timedelta to tableau Hyper API implementation."""
    days = td.days
    without_days = td - pd.Timedelta(days=days)
    total_seconds = int(without_days.total_seconds())
    microseconds = total_seconds * 1_000_000

    return tab_api.Interval(months=0, days=days, microseconds=microseconds)


def _interval_to_timedelta(interval: tab_api.Interval) -> pd.Timedelta:
    """Converts a tableau Hyper API Interval to a pandas Timedelta."""
    if interval.months != 0:
        raise ValueError("Cannot read Intervals with month componenets.")

    return pd.Timedelta(days=interval.days, microseconds=interval.microseconds)


def _insert_frame(
    df: pd.DataFrame, *, connection: tab_api.Connection, table: TableType
) -> None:
    if isinstance(table, str):
        table = tab_api.TableName(table)

    table_def = tab_api.TableDefinition(table)
    insert_funcs: List[str] = []

    for col_name, dtype in df.dtypes.items():
        column_type = _pandas_to_tableau_type(dtype.name)
        col = tab_api.TableDefinition.Column(
            name=col_name, type=column_type.type_, nullability=column_type.nullability
        )
        insert_funcs.append(_insert_functions[column_type.type_])
        table_def.add_column(col)

    if isinstance(table, tab_api.TableName) and table.schema_name:
        connection.catalog.create_schema_if_not_exists(table.schema_name)

    connection.catalog.create_table_if_not_exists(table_def)

    # Special handling for conversions
    df = df.copy()
    for index, (_, content) in enumerate(df.items()):
        if content.dtype == "timedelta64[ns]":
            df.iloc[:, index] = content.apply(_timedelta_to_interval)

    with tab_api.Inserter(connection, table_def) as inserter:
        for row in df.itertuples(index=False):
            for index, val in enumerate(row):
                # Missing value handling
                if val is None or val != val:
                    inserter._Inserter__write_null()
                else:
                    getattr(inserter, insert_funcs[index])(val)

        inserter.execute()


def _read_table(*, connection: tab_api.Connection, table: TableType) -> pd.DataFrame:
    if isinstance(table, str):
        table = tab_api.TableName(table)

    table_def = connection.catalog.get_table_definition(table)
    columns = table_def.columns

    dtypes: Dict[str, str] = {}
    for column in columns:
        column_type = _ColumnType(column.type, column.nullability)
        dtypes[column.name.unescaped] = _tableau_to_pandas_type(column_type)

    with connection.execute_query(f"SELECT * from {table}") as result:
        df = pd.DataFrame(result)

    df.columns = dtypes.keys()
    # The tableauhyperapi.Timestamp class is not implicitly convertible to a datetime
    # so we need to run an apply against applicable types
    for key, val in dtypes.items():
        if val == "datetime64[ns]":
            df[key] = df[key].apply(lambda x: x._to_datetime())
        elif val == "datetime64[ns, UTC]":
            df[key] = df[key].apply(lambda x: x._to_datetime()).dt.tz_localize("UTC")
        elif val == "timedelta64[ns]":
            df[key] = df[key].apply(_interval_to_timedelta)

    df = df.astype(dtypes)
    df = df.fillna(value=np.nan)  # Replace any appearances of None

    return df


def frame_to_hyper(
    df: pd.DataFrame, database: Union[str, pathlib.Path], *, table: TableType
) -> None:
    """
    Convert a DataFrame to a .hyper extract.

    Parameters
    ----------
    df : DataFrame
        Data to be written out.
    database : str
        tab_api.Name / location of the Hyper file to be written to.
    table : str, tab_api.Name or tab_api.TableName
        tab_api.Name of the table to write to. Must be supplied as a keyword argument.
    """
    with tab_api.HyperProcess(
        tab_api.Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU
    ) as hpe:
        tmp_db = pathlib.Path(tempfile.gettempdir()) / f"{uuid.uuid4()}.hyper"

        with tab_api.Connection(
            hpe.endpoint, tmp_db, tab_api.CreateMode.CREATE
        ) as connection:
            _insert_frame(df, connection=connection, table=table)

        shutil.move(tmp_db, database)


def frame_from_hyper(
    database: Union[str, pathlib.Path], *, table: TableType
) -> pd.DataFrame:
    """
    Extracts a DataFrame from a .hyper extract.

    Parameters
    ----------
    database : str
        tab_api.Name / location of the Hyper file to be read.
    table : str
        tab_api.Name of the table to read. Must be supplied as a keyword argument.

    Returns
    -------
    DataFrame
    """
    with tempfile.TemporaryDirectory() as tmp_dir, tab_api.HyperProcess(
        tab_api.Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU
    ) as hpe:
        tmp_db = shutil.copy(database, tmp_dir)
        with tab_api.Connection(hpe.endpoint, tmp_db) as connection:
            return _read_table(connection=connection, table=table)


def frames_to_hyper(
    dict_of_frames: Dict[TableType, pd.DataFrame], database: Union[str, pathlib.Path]
) -> None:
    """See api.rst for documentation."""
    with tab_api.HyperProcess(
        tab_api.Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU
    ) as hpe:
        tmp_db = pathlib.Path(tempfile.gettempdir()) / f"{uuid.uuid4()}.hyper"

        with tab_api.Connection(
            hpe.endpoint, tmp_db, tab_api.CreateMode.CREATE
        ) as connection:
            for table, df in dict_of_frames.items():
                _insert_frame(df, connection=connection, table=table)

        shutil.move(tmp_db, database)


def frames_from_hyper(
    database: Union[str, pathlib.Path]
) -> Dict[tab_api.TableName, pd.DataFrame]:
    """See api.rst for documentation."""
    result: Dict[TableType, pd.DataFrame] = {}
    with tempfile.TemporaryDirectory() as tmp_dir, tab_api.HyperProcess(
        tab_api.Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU
    ) as hpe:
        tmp_db = shutil.copy(database, tmp_dir)
        with tab_api.Connection(hpe.endpoint, tmp_db) as connection:
            for schema in connection.catalog.get_schema_names():
                for table in connection.catalog.get_table_names(schema=schema):
                    result[table] = _read_table(connection=connection, table=table)

    return result

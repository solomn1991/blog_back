import datetime

def format_row(record):
    d = {}
    for column in record.__table__.columns:
        value = getattr(record, column.name)

        if isinstance(value,datetime.datetime):
            value = str(value)[:19]

        d[column.name] = value
    return d



def format_result_set(result_set):
    l = [];
    for record in result_set:
        d = format_row(record)
        l.append(d);

    return l
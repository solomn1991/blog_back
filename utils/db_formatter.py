
def format_row(record):
    d = {}
    for column in record.__table__.columns:
        d[column.name] = str(getattr(record, column.name))
    return d



def format_result_set(result_set):
    l = [];
    for record in result_set:
        d = format_row(record)
        l.append(d);

    return l
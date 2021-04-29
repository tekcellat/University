def make_valid(entry):
    entry.setStyleSheet("background:#fff;")


def make_invalid(entry):
    entry.setStyleSheet("background:#f88;")


def get_valid(entry, type, is_wrong):
    try:
        res = type(entry.text())
        if is_wrong(res):
            raise ValueError()
    except ValueError:
        make_invalid(entry)
        raise ValueError()

    make_valid(entry)
    return res

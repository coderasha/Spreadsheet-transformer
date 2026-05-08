ALLOWED_EXTENSIONS = ["xlsx", "xls", "csv"]


def validate_extension(filename):
    ext = filename.split(".")[-1]
    return ext in ALLOWED_EXTENSIONS
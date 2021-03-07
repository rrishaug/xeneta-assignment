CODE_KEY = "error_code"
MSG_KEY = "error_msg"

DATE_FROM_INVALID_FORMAT = {
    CODE_KEY: "DATE_FROM_INVALID_FORMAT",
    MSG_KEY: "Invalid format for date_from"
}
DATE_TO_INVALID_FORMAT = {
    CODE_KEY: "DATE_TO_INVALID_FORMAT",
    MSG_KEY: "Invalid format for date_to"
}
DATE_FROM_AFTER_DATE_TO = {
    CODE_KEY: "DATE_FROM_AFTER_DATE_TO",
    MSG_KEY: "date_from can't be after date_to"
}
ORIGIN_NULL = {
    CODE_KEY: "ORIGIN_NULL",
    MSG_KEY: "origin required/can't be null"
}
DESTINATION_NULL = {
    CODE_KEY: "DESTINATION_NULL",
    MSG_KEY: "destination required/can't be null"
}
ORIGIN_AND_DESTINATION_SAME = {
    CODE_KEY: "ORIGIN_AND_DESTINATION_SAME",
    MSG_KEY: "origin and destination can't be the same value"
}
PRICE_NULL = {
    CODE_KEY: "PRICE_NULL",
    MSG_KEY: "price is required/can't be null"
}
PRICE_UNKNOWN_CURRENCY = {
    CODE_KEY: "PRICE_UNKNOWN_CURRENCY",
    MSG_KEY: "unable to do conversion with given currency"
}
PRICE_INVALID = {
    CODE_KEY: "PRICE_INVALID",
    MSG_KEY: "price must be a integer"
}
PRICE_NEGATIVE = {
    CODE_KEY: "PRICE_NEGATIVE",
    MSG_KEY: "price can't be negative"
}
INTERNAL_SERVER_ERROR = {
    CODE_KEY: "INTERNAL_SERVER_ERROR",
    MSG_KEY: "Internal server error"
}

class ApiException(Exception):

    def __init__(self, error, status_code=400):
        Exception.__init__(self)
        self.error = error
        self.status_code = status_code

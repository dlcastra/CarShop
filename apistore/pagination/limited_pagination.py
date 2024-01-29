import rest_framework.pagination


class LimitedPagination(rest_framework.pagination.LimitOffsetPagination):
    max_limit = 100

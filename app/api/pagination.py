from rest_framework.pagination import PageNumberPagination

class DefaultPagination(PageNumberPagination):
    """
    Permite que o cliente defina o tamanho da página usando o parâmetro 'page_size'.
    """
    page_size_query_param = 'page_size'
    max_page_size = 50

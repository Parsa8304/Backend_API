from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
       page_size = 3  # Default page size
       page_size_query_param = 'page_size'  # Allow client to set page size
       max_page_size = 100  # Maximum page size allowed

       
       def get_paginated_response(self, data):
              return super().get_paginated_response(data)  # Call the parent method to get the paginated response
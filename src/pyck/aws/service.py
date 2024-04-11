class Service:
    def get(self, client, operation, key):
        """Get results with paginator"""
        paginator = client.get_paginator(operation)
        page_iterator = paginator.paginate()
        results = []
        for page in page_iterator:
            results += page[key]
        return results

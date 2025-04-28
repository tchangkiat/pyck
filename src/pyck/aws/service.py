class Service:
    def get(self, client, operation, key, **kwargs):
        """Get results with paginator"""
        paginator = client.get_paginator(operation)
        page_iterator = paginator.paginate(**kwargs)
        results = []
        for page in page_iterator:
            results += page[key]
        return results

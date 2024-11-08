import logging
from django.utils.timezone import now
from django.core.cache import cache

# Set up logging
logger = logging.getLogger(__name__)

class RequestCacheLoggingMiddleware:
    """
    Middleware that logs request details and cache operations (hits/misses).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request details
        self.log_request(request)

        # Log cache activity before the response is returned
        response = self.get_response(request)
        self.log_cache_activity(request)

        return response

    def log_request(self, request):
        """
        Logs details about the incoming request.
        """
        logger.info(f"Request received: {request.method} {request.path} from {request.META.get('REMOTE_ADDR')}")
    
    def log_cache_activity(self, request):
        """
        Logs cache hits and misses. You can also log cache set and delete operations if needed.
        """
        # Example: Log cache hit/miss for a product
        if 'product_list' in cache:
            logger.info(f"Cache hit for 'product_list' at {now()}")
        else:
            logger.info(f"Cache miss for 'product_list' at {now()}")

        # Add similar logic for other cache keys if needed.
        # Example:
        # if f'product_{request.GET.get("product_id")}' in cache:
        #     logger.info(f"Cache hit for product_{request.GET.get('product_id')} at {now()}")
        # else:
        #     logger.info(f"Cache miss for product_{request.GET.get('product_id')} at {now()}")

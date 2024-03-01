def timing_decorator(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        total_time = end - start
        print(f"{func.__name__} took {total_time:.4f} seconds to run.")
        return result

    return wrapper


def debug_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

# 3. Memoization for Performance
# Code Snippet:
def memoize_decorator(func):
    memo = {}
    def wrapper(*args):
        if args in memo:
            return memo[args]
        result = func(*args)
        memo[args] = result
        return result
    return wrapper
# Reflection:
# Applying this decorator to recursive functions drastically improved their performance by storing previously computed results.
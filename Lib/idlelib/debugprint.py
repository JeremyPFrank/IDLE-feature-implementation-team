def debug_print(*args, **kwargs):
    import sys
    sys.stdout.write('__DEBUG__:' + ' '.join(str(a) for a in args))
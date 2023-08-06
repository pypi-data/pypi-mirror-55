def within_contexts(contexts, iterator):
    curr_context = None
    for line in iterator:
        if line.startswith('*'):
            l = line.lower()
            curr_context = next((context for context in contexts if l.startswith(context)), None)
            continue
        elif curr_context in contexts:
            yield curr_context, line

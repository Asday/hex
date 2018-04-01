def lerp(value_from, value_to, proportion):
    return value_from + ((value_to - value_from) * proportion)


def lazy_set_generator(iterable):
    seen = set()
    for item in iterable:
        if item in seen:
            continue

        seen.add(item)

        yield item

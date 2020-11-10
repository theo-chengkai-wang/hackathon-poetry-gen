def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


# test
if __name__ == '__main__':
    print(list(chunks('qwerty', 5)))

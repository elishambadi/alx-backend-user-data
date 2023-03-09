#!/usr/bin/python3
""" Check response
"""

if __name__ == "__main__":
    from api.v1.auth.auth import Auth

    a = Auth()
    res = a.authorization_header()
    if res is not None:
        print("authorization_header must return None")
        exit(1)
    print("OK", end="")


import robocrypt


def test_decryption_is_inverse_encryption():
    original = b"""Youngblood thinks there's always tomorrow
I miss your touch on nights when I'm hollow
I know you crossed a bridge that I can't follow

Since the love that you left is all that I get
I want you to know that if I can't be close to you
I'll settle for the ghost of you
I miss you more than life (More than life)

And if you can't be next to me
Your memory is ecstasy
I miss you more than life
I miss you more than life

Youngblood thinks there's always tomorrow (Woo)
I need more time, but time can't be borrowed
I leave it all behind if I could follow

Since the love that you left is all that I get
I want you to know that if I can't be close to you
I'll settle for the ghost of you
I miss you more than life, yeah

And if you can't be next to me
Your memory is ecstasy
I miss you more than life
I miss you more than life

Whoa, oh, oh-oh
More than life
Oh-oh

So if I can't get close to you
I'll settle for the ghost of you
I miss you more than life

And if you can't be next to me
Your memory is ecstasy
I miss you more than life
I miss you more than life"""

    pw = b'mah big strong amazing pee dub'
    encrypted = robocrypt.encrypt(original, pw)
    assert robocrypt.decrypt(encrypted, pw) == original

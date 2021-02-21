
import hypothesis
import hypothesis.strategies as st

import cb58ref


@hypothesis.given(st.binary())
def test_decode_inverts_encode(s):
    assert cb58ref.cb58decode(cb58ref.cb58encode(s)) == s

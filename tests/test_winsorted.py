# -*- coding: utf-8 -*-
"""
Testing for the windows sorting
"""
import platform

import natsort
import pytest


@pytest.mark.skipif(
    platform.system() != "Windows", reason="Windows-only features"
)
class TestWindowsExplorerSort:

    @pytest.mark.parametrize("x", [9, 5.4, b"a", (), None])
    def test_winsort_key_fails_for_non_integers(self, x):
        with pytest.raises(TypeError):
            natsort.winsort_key(x)

    def test_winsort_key(self):
        assert natsort.winsort_key("hello") < natsort.winsort_key("goodbye")

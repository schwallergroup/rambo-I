import pytest
from dotenv import load_dotenv

from rambo.tools import BOInitializer
from rambo.utils import init_dspy


@pytest.fixture
def suzuki_prompt():
    return (
        "I want to perform a Suzuki coupling with a new aryl halide, "
        "what would be the optimal conditions to start?"
    )


@pytest.fixture
def boinit():
    load_dotenv()
    init_dspy()
    return BOInitializer(5)


def test_boinit_suzuki(boinit, suzuki_prompt):
    resp = boinit(query=suzuki_prompt)

    temps = [
        resp.conditions[i].temperature for i in range(len(resp.conditions))
    ]
    solvents = [
        resp.conditions[i].solvent for i in range(len(resp.conditions))
    ]

    assert len(resp.conditions) == 5
    assert 102.5 in temps
    assert 83.91 in temps

    assert "water" in solvents

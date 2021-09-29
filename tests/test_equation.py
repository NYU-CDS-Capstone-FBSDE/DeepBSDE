import sys
sys.path.append('../')
import pytest
import equation as eqn
from absl import flags
import munch

@pytest.fixture
def configured_eqn():
    eqn_config =   { "eqn_config": {
    "_comment": "HJB equation in PNAS paper doi.org/10.1073/pnas.1718942115",
    "eqn_name": "HJBLQ",
    "total_time": 1.0,
    "dim": 100,
    "num_time_interval": 20
  }}
    eqn_config = munch.munchify(eqn_config)
    bsde = getattr(eqn, eqn_config.eqn_config.eqn_name)(eqn_config.eqn_config)
    return bsde

def test_equation_setup(configured_eqn):
    assert configured_eqn.dim is not None
    assert configured_eqn.total_time is not None
    assert configured_eqn.num_time_interval is not None
    assert configured_eqn.delta_t is not None
    assert configured_eqn.sqrt_delta_t is not None
    assert configured_eqn.y_init is None

def test_hjblq_setup(configured_eqn):
    assert configured_eqn.x_init is not None
    assert configured_eqn.sigma is not None
    assert configured_eqn.lambd is not None

def test_hjblq_data_generation(configured_eqn):
    hjblq_sample = configured_eqn.sample(10)
    assert hjblq_sample[0].shape == (10, configured_eqn.dim, configured_eqn.num_time_interval)


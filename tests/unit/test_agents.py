from sla.agents.random_agent import RandomAgent


def test_random_agent_actions_in_range():
    agent = RandomAgent(4, seed=0)
    actions = {agent.act(None) for _ in range(200)}
    assert actions <= {0, 1, 2, 3} and len(actions) == 4


def test_random_agent_save_load_continues_same_sequence(tmp_path):
    agent = RandomAgent(3, seed=7)
    agent.act(None)
    agent.save(tmp_path / "ck")
    clone = RandomAgent.load(tmp_path / "ck")
    assert [agent.act(None) for _ in range(20)] == [clone.act(None) for _ in range(20)]

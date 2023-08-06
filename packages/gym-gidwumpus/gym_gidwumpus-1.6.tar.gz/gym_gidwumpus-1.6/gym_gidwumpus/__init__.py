from gym.envs.registration import registry, register, make, spec

register(
    id='gidwumpus-v0',
    entry_point='gym_gidwumpus.envs:GidWumpusEnv',
)

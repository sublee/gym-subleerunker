import time

import gym
from gym import spaces
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


__all__ = ['SubleerunkerEnv']


class SubleerunkerEnv(gym.Env):

    metadata = {'render.modes': ['human']}

    action_space = spaces.Discrete(3)
    observation_space = spaces.Box(low=0, high=256**3, shape=(320, 240))
    reward_range = (0, float('inf'))

    driver = None

    def reset(self):
        if self.driver is None:
            self.driver = webdriver.Remote(
                'http://127.0.0.1:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.CHROME)

        self.driver.get('http://nop.subl.ee/subleerunker/')
        self.started_at = time.time()
        self.tick(0)
        self.start()

    def step(self, action):
        if action == 0:
            self.idle()
        elif action == 1:
            self.left()
        elif action == 2:
            self.right()

        self.tick(time.time() - self.started_at)
        state = self.state()

        observation = state['pixels']
        reward = state['score']
        done = state['dead']
        info = {}

        return observation, reward, done, info

    def render(self, mode='human', close=False):
        pass

    # ---

    def js(self, code):
        return self.driver.execute_script(code)

    def start(self):
        self.js('game.startGameplay()')

    def tick(self, time=None):
        return
        if time is None:
            self.js('game.tick()')
        else:
            self.js('game.tick(%.3f)' % (time * 1000))

    def state(self):
        return self.js('''
        return {
            pixels: [],
            dead:   Boolean(game.player && game.player.dead),
            score:  game.scores.current,
        };
        ''')

    def left(self):
        self.js('''
        game.setInputBit(LEFT_PRESSED, true);
        game.setInputBit(RIGHT_PRESSED, false);
        ''')

    def right(self):
        self.js('''
        game.setInputBit(LEFT_PRESSED, false);
        game.setInputBit(RIGHT_PRESSED, true);
        ''')

    def idle(self):
        self.js('''
        game.setInputBit(LEFT_PRESSED, false);
        game.setInputBit(RIGHT_PRESSED, false);
        ''')

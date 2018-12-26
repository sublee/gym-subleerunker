from ghost import Ghost
import gym
from gym import spaces


LEFT  = 37
RIGHT = 38


class SubleerunkerEnv(gym.Env):

    metadata = {'render.modes': ['human']}

    action_space = spaces.Discrete(3)
    observation_space = spaces.Box(low=0, high=256**3, shape=(320, 240))
    reward_range = (0, float('inf'))

    def reset(self):
        self.session = Ghost().start(viewport_size=(480, 640)).__enter__()

        self.session.open('http://nop.subl.ee/subleerunker/?fps=0')
        self.session.wait_for_page_loaded()

        self.tick()
        self.start()

    def step(self, action):
        if action == 0:
            self.idle()
        elif action == 1:
            self.left()
        elif action == 2:
            self.right()

        self.tick()
        state = self.state()

        observation = state['pixels']
        reward = state['score']
        done = state['dead']
        info = {}

        print(done)

        return observation, reward, done, info

    def render(self, mode='human', close=False):
        if close:
            self.session.hide()
        else:
            self.session.show()

    # ---

    def js(self, code):
        return self.session.evaluate(code)

    def start(self):
        self.js('game.startGameplay()')

    def tick(self):
        self.js('game.tick()')

    def state(self):
        state, __ = self.js('''
        (function() { return {
            pixels: game.renderer.extract.pixels(game.renderer._lastObjectRendered),
            dead:   Boolean(game.player && game.player.dead),
            score:  game.scores.current,
        }; })();
        ''')
        return state

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

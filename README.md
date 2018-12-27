# gym-subleerunker

Run a Selenium WebDriver first at `localhost:4444`:

```bash
$ java -Dwebdriver.chrome.driver=chromedriver -jar selenium-server-standalone-3.141.59.jar
```

Then you can try this gym:

```python
import gym
import gym_subleerunker

env = gym.make('Subleerunker-v0')
env.reset()

while True:
    env.step(env.action_space.sample())
```

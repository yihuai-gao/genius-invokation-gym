# Genius Invokation Gym

A simple simulator of the Genius Invokation TCG in Genshin impact

API will be designed based on [rlcard](https://github.com/datamllab/rlcard)

Simulator framework references [fireplace](https://github.com/jleclanche/fireplace)

Package name `gisim` stands for both `Genshin Impact` and `Genius Invokation`

一个简易的七圣召唤仿真器（如果不弃坑的话）

希望可以实现类似openai-gym的API，用于训练ai&评估卡组强度


## Roadmap
- [ ] Encode the game status into a dictionary
- [ ] Enable `Judge` to judge validity of a proposed action
- [ ] Define all kinds of messages in the simulator
- [ ] Write message queue to buffer all messages
- [ ] Add respond method to every character, summon, status
- [ ] Put all parts together

## Logs

12.9 update: 应该会采用[rlcard](https://github.com/datamllab/rlcard)相近的API接口进行设计，参考[DouZero](https://github.com/kwai/DouZero)，目前正在调研中

12.10 update: 参考炉石传说模拟器[fireplace](https://github.com/jleclanche/fireplace)完成了卡牌及框架的初始化（目前仍为空文件）

顺便好奇一下为什么用invokation而不是invocation，求懂哥指点

新建QQ交流群613071650，欢迎感兴趣的同学入群

## Works Cited

[RLCard: A Toolkit for Reinforcement Learning in Card Games](https://github.com/datamllab/rlcard)  
[DouZero: Mastering DouDizhu with Self-Play Deep Reinforcement Learning](https://github.com/kwai/DouZero)

<!--
 Copyright (c) 2022 davidgao

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

# Genius Invokation Gym

A simple simulator of the Genius Invokation TCG in Genshin impact

API will be designed based on [rlcard](https://github.com/datamllab/rlcard)

Simulator framework references [fireplace](https://github.com/jleclanche/fireplace)

Package name `gisim` stands for both `Genshin Impact` and `Genius Invokation`

一个简易的七圣召唤仿真器（如果不弃坑的话）

希望可以实现类似openai-gym的API，用于训练ai&评估卡组强度


# Roadmap
- [x] Encode the game status into a dictionary
- [x] Define all kinds of messages for communication
- [x] Use message queue (with priority) to buffer all messages
- [ ] Enable judging validity of a proposed action
- [ ] Add message handler to every character, summon, status, ...
    - [x] Finish normal attack, elemental skill, elemental burst of KamisatoAyaka (as a template to generate more characters in the future)
    - [x] Add Summon and Elemental Infusion based on KamisatoAyaka


## Logs

应该会采用[rlcard](https://github.com/datamllab/rlcard)相近的API接口进行设计，参考[DouZero](https://github.com/kwai/DouZero)，目前正在调研中

参考炉石传说模拟器[fireplace](https://github.com/jleclanche/fireplace)完成了卡牌及框架的初始化（目前仍为空文件）

顺便好奇一下为什么用invokation而不是invocation，求懂哥指点

新建QQ交流群613071650，欢迎感兴趣的同学入群，欢迎成为Contributor！

## Works Cited

[RLCard: A Toolkit for Reinforcement Learning in Card Games](https://github.com/datamllab/rlcard)

[DouZero: Mastering DouDizhu with Self-Play Deep Reinforcement Learning](https://github.com/kwai/DouZero)

# About

OpenAI Gym Environment for Wechat game 跳一跳.

# Note

烂尾了。因为Android截屏太耗时导致获取state太耗时，满足不了强化学习的速度需求。

# Prerequirement

You should open Develop option on your Android phone, and enable 'USB debug' option. 
If it is a Xiaomi phone, you may also need to enable 'USB Debug(Safe)' option.

Currently I only test it on XiaomiMix2S. More devices support coming later.

Windows system is not supported right now. Pull request is welcome.

You should also have a working `adb` binary recognized by system.

It uses Python3.6+.

# How to use

```
pip install -e .
```

Then enter UI of 跳一跳,

```
python3 test.py
```



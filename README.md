TwitterForwardBot
===
- 🎯自动检查关注的推特更新内容  
- 🎯通过telegram机器人转发链接至群组  
- ✨无需Twitter API  

Requirements
---
- [twint](https://github.com/twintproject/twint)
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- [schedule](https://github.com/dbader/schedule)

TODO
---
- 解决重复发送问题  
    - 根本原因：触发Twitter滥用限制
    - 可能可行办法：数据库记录 去重
---
_为什么不用Twitter API：因为要写300字小作文申请信（懒），且一个账号申请失败就永久不能再申请_
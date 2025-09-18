# GeoIP2-CN 自动构建与更新方案

本项目提供自动下载与构建 MaxMind 官方 GeoLite2-Country.mmdb 数据库的脚本与配置，旨在为 Surge、Clash 、QuantumultX等网络工具提供可信、自控、定期更新的地理定位支持。

## 项目背景

在网络安全与策略分流配置中，GeoIP 数据库被广泛用于判断 IP 属地，辅助智能路由或访问控制。当前不少项目使用二手分发源，存在以下潜在问题：

- **缺乏信任链**：非官方源内容不可审计，存在被污染或篡改的风险；
- **可维护性差**：不可预测是否随时中断；
- **更新滞后**：间隔时间不可控。

为此，本项目实现完全自控化更新机制，确保数据源为 MaxMind 官方，结构可追溯、更新可控、逻辑可审计，适配 Surge、Clash 等配置使用。

## 项目优势

- **官方数据源：** 所有数据均直接来自 MaxMind，可信、安全；
- **自动更新：** 通过 GitHub Actions 每 3 天拉取最新版本，持续同步；
- **遵循授权机制：** 项目基于 GitHub Actions 自动拉取 MaxMind 数据，并根据其 [GeoLite2 使用协议](https://www.maxmind.com/en/geolite2/eula) 提供更新逻辑。建议用户自行申请 License Key 使用本项目，确保数据来源合规、安全、可追溯。
- **自定义可控：** 用户可根据实际需求自由配置输出路径、更新频率、目标分支等参数，满足个性化部署场景。

### 自动化更新

项目采用 GitHub Actions 实现自动更新机制，每隔 3 天拉取最新数据，确保始终保持最新状态，无需人工干预。

## 文件路径

| 文件名称     |                  构建后文件路径（仅供参考）                  | 示例用途                                                     |
| ------------ | :----------------------------------------------------------: | ------------------------------------------------------------ |
| Country.mmdb | [`data/Country.mmdb`](https://raw.githubusercontent.com/Thoseyearsbrian/GeoIP2-CN/main/data/Country.mmdb) | Surge、Clash、QuantumultX 等支持 GeoIP 的工具作为 CN 区域判断依据 |

## 配置方式

请参考项目 [Wiki](https://github.com/Thoseyearsbrian/GeoIP2-CN/wiki/Surge) 提供的文档教程，在各个工具中自定义 GeoIP2 数据库。

目前 Wiki 中已经添加了如下工具的配置教程，欢迎大家在 Issues 中补充：

* [Surge](https://github.com/Thoseyearsbrian/GeoIP2-CN/wiki/Surge)
  * Surge 配置文件修改
  * Surge for iOS 图形化配置
  * Surge for macOS 图形化配置
* [Quantumult X](https://github.com/Thoseyearsbrian/GeoIP2-CN/wiki/Quantumult-X)
* [Shadowrocket](https://github.com/Thoseyearsbrian/GeoIP2-CN/wiki/Shadowrocket)
* [Clash](https://github.com/Thoseyearsbrian/GeoIP2-CN/wiki/Clash)
  * ClashX / ClashX Pro (macOS)
  * Clash for Windows
  * OpenClash (OpenWRT)
  * Clash for Android
  * Stash (iOS)

## ⚠️ 注意事项
1. **禁用或删除** 与 **中国大陆 IP 地址段** 相关的规则或规则集
   
    ``` bash
    RULE-SET,https://raw.githubusercontent.com/Thoseyearsbrian/Aegis/main/SurgeAegis/rules/China.list, DIRECT # 禁用或删除类似规则
    GEOIP,CN,DIRECT # 与上一条类似的规则与本条规则不可共存
    ```
    
2.  GEOIP-CN 查询规则建议**紧随最终规则之上**，以避免域名规则被忽略导致判断错误。
    ``` bash
    # ... 省略其他规则 ...
    GEOIP,CN,DIRECT # 建议在这里使用规则
    FINAL,REJECT # 最终规则
    ```

3. 规则中**不可以**存在其他国家或地区的 `GEOIP` 查询规则，因为项目提供的数据库中**仅包含中国大陆地区的 IP 地址段记录**
    ``` bash
    GEOIP, US, PROXY # 错误，无法查询到相关记录
    GEOIP, AU, PROXY # 错误，无法查询到相关记录
    GEOIP, HK, PROXY # 错误，无法查询到相关记录
    GEOIP, CN, DIRECT # 正确
    ```

🔐 免责声明

本项目构建所得 `.mmdb` 文件仅用于测试与学习研究用途，**不得用于任何形式的商业用途**。

使用者需自行确保符合 [MaxMind EULA](https://www.maxmind.com/en/geolite2/eula) 协议及其地区相关法规，**本项目对因使用数据产生的任何行为或后果不承担任何法律责任**。

本项目**仅提供构建逻辑与脚本**，不直接分发原始数据。推荐用户通过 MaxMind 官网申请并使用专属 License Key。

**如您对授权合规性有疑问，建议联系 MaxMind 官方获取帮助。**

**本项目仅面向具备基础技术背景与合规意识的开发者群体使用。**

## 🏅 版权声明

- 本项目通过自动构建流程生成 `.mmdb` 文件供测试与研究用途，访问者请确保已阅读并接受 [MaxMind EULA](https://www.maxmind.com/en/geolite2/eula)。**本项目不对用户的任何用途或行为承担法律责任，使用者需自行确保合规；**
- 本项目使用 GitHub Actions 自动拉取 MaxMind 官方数据。**使用本项目前，用户需前往 MaxMind 官网注册并获取属于自己的 License Key**，以便合规运行脚本或自动更新流程；
- GeoLite2 数据版权归 [MaxMind, Inc.](https://www.maxmind.com/) 所有，遵循其 [GeoLite2 数据库许可协议](https://www.maxmind.com/en/geolite2/eula)；
- 本项目中所含脚本和配置文件遵循 [MIT License](https://raw.githubusercontent.com/Thoseyearsbrian/GeoIP2-CN/main/LICENSE)。

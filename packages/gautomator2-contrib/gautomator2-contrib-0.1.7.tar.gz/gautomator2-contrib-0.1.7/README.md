# GA2 (Android/iOS)
## Why GAutomator2
1. 便于发布和维护。作为库发布，有真正意义上的版本。用户不需要带着一堆源码上传平台测试。
2. 跨平台。接口统一iOS与android，也方便扩展其他平台。
3. 可扩展。用户能够扩展常用功能的自定义实现而不用修改库源码。
4. 增加UI定位方法。在原先GA引擎接口的基础上，增加平台原生控件以及模板图像定位支持。
5. 支持UI信息与逻辑分离。通过将UI元素定义在配置文件，脚本开发人员不需要关注UI元素的定位方式
	
## 框架结构
![](docs/pic/GA2.0.png)

# 使用说明
## 支持平台
- Android（Unity+UE4)
- iOS(Unity for now)

脚本语言：python2.7/3.4+

## 安装（公司内网可能需要设置代理）
- 基础包： pip install gautomator2
- 包含辅助包：pip install gautomator2-contrib 


## 环境准备
- android自动化需要PC安装adb并配置在环境变量中。
- iOS自动化需要Mac OS(10.13.6+),安装[libimobiledevice](https://github.com/libimobiledevice)，并且先在目标iOS设备上启动WebDriverAgent，并通过iproxy xxxx 8100做PC到设备的端口转发。
- 使用引擎交互需要游戏集成[GA SDK](https://github.com/Tencent/GAutomator/tree/master/GAutomatorSdk)

## 辅助工具
针对android的游戏引擎控件获取工图像具[GAutomatorView](http://cdn.wetest.qq.com/com/c/GAutomatorView.zip)
针对iOS的引擎控件录制工具[GA Recorder](https://github.com/Tencent/GAutomator/blob/master/GAutomatorIos/docs/GA%20Recorder.md)

## 接口文档
详见docs
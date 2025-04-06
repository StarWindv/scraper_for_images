# scraper_for_images 项目说明文档

**注意, 此分支不能直接运行，必须要安装好才可以使用**
**如果您想使用类似于`python fillname.py`的命令来使用，那么请移步[主分支](https://github.com/StarWindv/scraper_for_images/tree/main)**

## 项目简介

`scraper_for_images` 是一个用于下载图片的 Python 项目，可以从网络下载指定关键词的图片，并提供去重和重命名的功能。

## 功能亮点

- 🖼️ **下载图片**：支持根据关键词下载指定数量的图片
- 🧹 **去重功能**：自动删除重复图片
- ✏️ **重命名图片**：对下载的图片进行重命名，避免混乱
- 📖 **多语言支持**：使用locale库进行语言检测，并修改主要逻辑描述语言

## 文件结构

```
scraper_for_images
├── __init__.py
├── core
│   ├── WebProcessor.py
│   ├── __init__.py
│   └── stv_parse.py
├── main.py
└── utils
    ├── __init__.py
    ├── change_text.py
    ├── head.py
    ├── lic.py
    └── utils.py
```

## 安装与使用

### 安装依赖

在运行脚本之前，需要安装以下 Python 库：

```bash
pip install requests selenium stv_utils
```

### 运行脚本

使用以下命令运行 `bing_streaming.py` 脚本：

```bash
python main.py --keyword <关键词> --page <页数> --remove <是否去重> --window <窗口数量> --lines <线程数量>
```

### P.S. 第二种方法

从源码构建python程序，您可以使用项目自带的 [构建文件](./pyproject.toml) 或者是自己撰写。

首先克隆仓库
```bash
git clone -b package https://github.com/StarWindv/scraper_for_images.git
```

然后导航到项目内
```bash
cd scraper_for_images
```

安装项目
```bash
pip install .
```

#### 参数说明

| 参数          | 描述         | 默认值      |
| ----------- | ---------- | -------- |
| `--keyword` | 要下载的图片关键词  | 无        |
| `--page`    | 下载的页数      | 无        |
| `--remove`  | 是否去除重复图片   | `True`   |
| `--window`  | 最大窗口数      | `2`      |
| `--lines`   | 启用的线程数     | `16`     |
| `--time`    | 限制单张图片超时时间 | `4s`     |
| `--plate`   | 目标图片形状     | `All`    |
| `--path`    | 修改目标下载路径   | `当前工作目录` |
| `--license` | 查看项目许可证    | `MIT`    |
| `--version` | 查看项目版本     | `/`      |

## 功能描述

### 下载图片

- `bing.py` 脚本支持并行下载图片，并将其保存在以关键词命名的文件夹中。支持多线程和异步下载。

### 去重与重命名

- 程序会去除重复的图片。
- 程序会对剩余的图片进行重命名，避免文件命名冲突。

## 注意事项

- ⚠️ 请确保已安装所有依赖库。
- 📜 请遵守当地法律法规，避免下载版权受保护的图片。
- 🧳 脚本会在运行时创建 `keyword_images` 文件夹存储下载的图片，路径可修改。
- 🚫 本脚本没有错误处理，请谨慎使用。

## 许可证

该项目遵循 [MIT 许可证](./LICENSE)。

## 贡献者

- 项目由 [星灿长风v](https://github.com/StarWindv) 创建。
- 贡献者欢迎提交 Pull Requests。

## 声明

- Legal Disclaimer
  
  ```
  THE AUTHORS AND COPYRIGHT HOLDERS SHALL NOT BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
  WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH 
  THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. 
  ANY MODIFICATIONS MADE BY THIRD PARTIES ARE SOLELY THE RESPONSIBILITY OF THE MODIFIER.
  ```

- 衍生作品需在文档或启动界面注明原始项目来源

- 分发时需提供修改记录的摘要（如CHANGELOG文件）

- 修改后的代码必须在文件头部添加原项目署名（如注释`Based on [scraper_for_images] by [星灿长风v(Starwindv)]`）

- 明确禁止用原作者的名称/商标为衍生作品背书

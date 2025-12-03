# 难度选择功能文档更新

**日期**: 2025-12-03  
**更新内容**: 游戏难度选择功能的文档补充

## 更新概览

本次更新补充了当前游戏中已有的难度选择功能的详细文档说明，让用户能够充分了解如何使用这些功能。

## 当前实现总结

### 1. 启动时选择难度

**命令行方式**:
```bash
# 默认初级难度
python run_game.py

# 指定难度
python run_game.py --difficulty intermediate
python run_game.py --difficulty advanced

# 自定义设置
python run_game.py --difficulty custom --width 20 --height 20 --mines 50
```

**难度选项**:
- `beginner`: 9×9 棋盘，10个地雷
- `intermediate`: 16×16 棋盘，40个地雷
- `advanced`: 30×16 棋盘，99个地雷
- `custom`: 用户自定义尺寸和地雷数

### 2. 游戏中切换难度

**键盘快捷键**:
- **1键** → 切换到初级难度
- **2键** → 切换到中级难度
- **3键** → 切换到高级难度

**N键循环**:
- 按N键在三个预设难度间循环切换

### 3. UI显示

- **左上角**: 显示当前难度
- **屏幕底部**: 显示控制说明

## 更新的文档文件

### 1. `specs/001-minesweeper-game/quickstart.md`

**更新的部分**:

#### Starting the Game 部分
- ✅ 添加了所有难度选项的详细说明
- ✅ 补充了游戏内切换难度的说明
- ✅ 更正了命令行示例（从 `src/main.py` 改为 `run_game.py`）

#### Game Controls 部分
- ✅ 添加了 1/2/3 键的难度切换说明
- ✅ 每项说明都包含具体的棋盘尺寸和地雷数

**更新前**:
```markdown
### Game Controls

- **Left Click**: Reveal cell
- **Right Click**: Toggle flag on cell
- ...
- **N**: Start new game with current settings
- **ESC**: Exit game
```

**更新后**:
```markdown
### Game Controls

- **Left Click**: Reveal cell
- **Right Click**: Toggle flag on cell
- ...
- **N**: Start new game with current settings
- **1**: Change to Beginner difficulty (9×9, 10 mines)
- **2**: Change to Intermediate difficulty (16×16, 40 mines)
- **3**: Change to Advanced difficulty (30×16, 99 mines)
- **ESC**: Exit game
```

### 2. `README.md`

**更新的部分**:

#### Basic Usage 部分
- ✅ 更正了命令行示例（从 `src/main.py` 改为 `run_game.py`）
- ✅ 添加了难度选项的详细说明
- ✅ 补充了游戏内控制说明

**Controls 部分** (已存在，无需更新)
- ✅ 已经有完整的 1/2/3 键说明
- ✅ 已经有 N 键说明

## 文档改进亮点

1. **完整性**: 覆盖了从启动到游戏中的所有难度选择场景
2. **清晰性**: 每种方式都有具体的命令示例和说明
3. **一致性**: 更新了所有相关文档中的命令行示例
4. **用户友好**: 新手可以快速找到并学会如何使用难度选择

## 未实现的功能（待改进）

根据代码分析，以下功能仅部分实现或未完全实现：

1. **难度选择菜单**: `_show_difficulty_menu()` 方法只有注释，实际未实现菜单界面
2. **自定义设置UI**: 游戏内没有图形化界面让用户输入自定义设置
3. **F1帮助键**: 实现了但没有显示完整的帮助信息

## 建议的后续改进

1. 实现一个真正的难度选择菜单界面
2. 添加游戏内自定义设置的UI表单
3. 完善F1帮助系统，显示所有可用快捷键
4. 在屏幕上添加可见的难度选择按钮

## 总结

当前的难度选择功能通过键盘快捷键和命令行参数已经完全可用，本次文档更新让用户能够：
- 快速了解所有可用的难度选择方式
- 通过命令行为游戏设置初始难度
- 在游戏中快速切换不同难度
- 理解每个难度的具体参数

所有文档更新已完成，用户现在可以通过查看文档完全了解如何操作游戏！


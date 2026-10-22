# VoxelGenesis — Minecraft 1.21.10 程序化世界生成引擎

[English](README.md) | **简体中文**

> **⚠️ 版本锁定**：本项目专为 Minecraft Java 版 **1.21.10**（`DataVersion = 4556`，协议 `773`）开发。
> 生成器依赖该版本精确的方块 ID、方块状态属性与 NBT 区块格式，**不保证兼容其他版本**。
> 如需在其他版本上运行，须自行下载对应版本的 `minecraft-server.jar` 并处理方块更名/格式差异等兼容性问题。

不依赖任何模组、编辑器或游戏内工具，直接在 Minecraft Anvil 二进制区块层面进行体素级写入的程序化世界生成引擎。纯 Python 实现，零运行时依赖——从种子号到可游玩存档的端到端流水线，输出 **100% 字节级确定性**：重复构建的 SHA-256 哈希完全一致。

在数万体素的画布上构筑一整片现代世界——别墅群、滨海公园、海上邮轮、超跑展厅、水下餐厅与私人金库，全部由纯方块状态构成，**不生成任何实体与盔甲架**。每一盏吊灯、每一辆超跑、每一座雕塑皆为体素。

## 核心能力

- **Anvil 原生写入** — 直接序列化/反序列化 NBT 与非跨界 64 位区块位打包，绕过一切中间工具与游戏运行时
- **字节级确定性** — 固定时间戳、gzip mtime=0、坐标哈希确定性随机源；两次全量构建，全部区块 SHA-256 零差异
- **三重验证流水线** — 1.21.10 NBT 模式校验 → 3D 空间连通性可行走性审计 → 全量区块回读对比，确保零实体合规

## 目录结构

```
├── README.md                          # English documentation
├── README.zh-CN.md                    # 本文件（中文）
├── LICENSE                            # MIT License
├── .gitignore
├── generator_src/                     # 生成器源码
│   ├── config.py                      # 坐标边界、高程基准、材质调色板
│   ├── nbt_mca.py                     # 纯 Python NBT 读写与区块位打包
│   ├── world_canvas.py                # 内存体素画布与全局后处理
│   ├── arch_lib.py                    # 参数化建筑构件库
│   ├── zone_core_villa.py             # 核心别墅区
│   ├── zone_expansions.py             # 拓展区域（停机坪、高尔夫、农场）
│   ├── zone_seaside_park.py           # 海滨公园
│   ├── zone_cruise_ship.py            # 海上邮轮
│   ├── zone_v5_expansions.py          # V5 拓展区域
│   ├── zone_beach_park.py             # 海滨沙滩公园
│   ├── zone_sports_complex.py        # 体育运动综合体
│   ├── zone_urban_district.py        # 主城区
│   ├── generate_estate.py             # 主编排器
│   ├── verify_1_21_10_schema.py       # 1.21.10 NBT 合规校验器
│   ├── audit_spatial_connectivity.py  # 3D 空间连通性审计器
│   └── validate_and_render.py         # 全量回读验证 + 渲染
├── tools/
│   ├── pregen_seed_world.py           # 从种子号预生成原始世界模板
│   ├── regen_snapshot.py              # 按当前画布范围重建地形快照
│   └── refresh_baseline.py            # 端到端刷新验证基线并归档
└── (产物目录，不入库)
    ├── seed_world/                    # 由 tools/ 脚本生成
    └── TEST_BUILDINGS/                # 生成器输出的 Minecraft 存档
```

## 快速开始

### 环境要求

| 依赖 | 版本 | 用途 |
| :--- | :--- | :--- |
| Python | 3.10+ | 运行生成器 |
| matplotlib | 任意近期版本 | 仅渲染脚本需要 |
| Java | **21+** | 仅种子世界预生成需要 |
| minecraft-server.jar | **官方 1.21.10** | 自行获取，不入库 |

> **关于 server jar**：`minecraft-server.jar` 须从 [Minecraft 官网服务端下载页](https://www.minecraft.net/download) 自行获取，版本必须为 **1.21.10**。
> 该文件因体积与版权原因不入 `.gitignore`，不随仓库分发。
> 若使用其他版本的服务端，方块 ID 更名、区块格式差异等兼容性问题须由使用者自行处理。

### 构建全流程

```bash
# 0. 把官方 minecraft-server.jar（1.21.10）放入 tools/

# 1. 从种子号预生成原始世界模板（约 2 分钟，只需一次；种子号已内置在脚本中）
python tools/pregen_seed_world.py --accept-eula --out ./seed_world

# 2. 复制模板为工作存档
cp -r seed_world TEST_BUILDINGS          # Windows: Copy-Item -Recurse seed_world TEST_BUILDINGS

# 3. 运行生成器（约 25 秒）
python generator_src/generate_estate.py ./TEST_BUILDINGS

# 4. 验证与渲染（可选）
python generator_src/verify_1_21_10_schema.py ./TEST_BUILDINGS
python generator_src/audit_spatial_connectivity.py ./TEST_BUILDINGS
python generator_src/validate_and_render.py ./TEST_BUILDINGS .

# 5. 游玩：把 TEST_BUILDINGS 复制到 .minecraft/saves/ 下即可
```

要点：
- 第 1 步只需做一次；之后反复执行 2–3 即可幂等重建；
- `seed_world/`、`TEST_BUILDINGS/` 都是产物，随时可删；
- 生成器只接受包含 `level.dat` + `region/` 的世界目录作为输入。

## 设计方法论

### 确定性保证

- 所有 `.mca` 区块头使用固定时间戳；
- `level.dat` 与 `playerdata/*.dat` 使用 `gzip mtime=0`；
- 地形快照保存建造前的原始地表高程，保证重复运行幂等；
- 所有随机数生成器均绑定固定种子。

### 五阶段建造顺序

体素图元会覆盖先前放置的方块，每栋多层建筑严格遵循以下执行顺序：

1. **结构外壳与楼板** — 先填充各层楼板与外墙，再安装玻璃幕墙
2. **室内隔墙、吊顶与地毯** — 照明格栅、卫浴、地毯等室内构件
3. **垂直交通** — 楼梯与塔楼必须在所有楼板就位之后建造
4. **家具与门** — 在房间外壳与楼梯完成后放置
5. **全局后处理** — 双开门铰链规范化、玻璃板/栅栏自动连接、环境光补光

### Minecraft 1.21.10 合规

- 方块状态自动规范化（如 `chain` → `iron_chain`）；
- 非跨边界 64 位调色板打包；
- 零实体、零盔甲架。

### 扩展维护原则

- 楼板填充与门洞开凿永远先于楼梯建造；
- 楼梯层数必须等于上下层高差；
- 双开门统一使用专用函数，铰链贴外墙；
- 水下建筑须配置多层次水下照明；
- 树木生成须经过碰撞保护，禁止嵌入建筑；
- 一切随机必须使用固定种子随机源。

## 许可与致谢

本项目以 [MIT License](LICENSE) 开源。本项目为原创程序化生成工具。Minecraft 为 Mojang AB 商标，本项目不分发 Minecraft 服务端二进制，使用者须自行获取正版。

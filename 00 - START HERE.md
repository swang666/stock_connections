# 🧠 AI Supply-Chain Knowledge Base

A living map of who supplies, sells to, and benefits from whom across the AI value chain. Open the **Graph view** (left sidebar, the connected-dots icon) to see the whole network. Each `[[link]]` between pages is an edge in that graph.

## How to use this vault
1. **Drop raw material** (10-Ks, earnings transcripts, news) into the `sources/` folder.
2. **Run the extraction prompt** in `_prompts/Extraction Prompt.md` against that material with your LLM.
3. The LLM **updates company/theme pages** with new `[[links]]` and appends rows to the spreadsheet.
4. **Obsidian's graph view** redraws the network automatically. Open `AI Supply Chain Graph.html` for a richer interactive view.

## Layers (upstream → downstream)

**L1 — EDA & IP**
[[Arm Holdings]], [[Cadence]], [[Synopsys]]

**L2 — Semiconductor Equipment**
[[ASML]], [[Advanced Micro-Fabrication (AMEC)]], [[Applied Materials]], [[Camtek]], [[Entegris]], [[FormFactor]], [[Hanmi Semiconductor]], [[Hitachi]], [[KLA Corporation]], [[Lam Research]], [[Naura Technology]], [[Teradyne]], [[XLight]]

**L3 — Foundry / Manufacturing**
[[GlobalFoundries]], [[Intel]], [[SMIC]], [[Samsung Electronics]], [[TSMC]], [[X-FAB]]

**L4 — Chip Designers (Accelerators/Networking)**
[[AMD]], [[Broadcom]], [[Cambricon]], [[Cerebras Systems]], [[Huawei]], [[IBM]], [[Iluvatar CoreX]], [[Marvell]], [[MediaTek]], [[MetaX]], [[NVIDIA]], [[Qualcomm]], [[SambaNova Systems]]

**L5 — Memory (HBM/DRAM)**
[[ChangXin Memory (CXMT)]], [[Kioxia Holdings]], [[Micron]], [[Nanya Technology]], [[SK Hynix]], [[Sandisk]], [[Yangtze Memory (YMTC)]]

**L6 — Advanced Packaging / OSAT**
[[AUO Corporation]], [[Amkor Technology]], [[BOE Technology]], [[Corning]], [[Innolux]], [[Zhen Ding Technology]]

**L7 — Optical & Interconnect**
[[Alphawave Semi]], [[Amphenol]], [[Applied Optoelectronics]], [[Astera Labs]], [[Ayar Labs]], [[Ciena]], [[Coherent]], [[Credo Technology]], [[Fabrinet]], [[Furukawa Electric]], [[Largan Precision]], [[Lumentum]], [[Luxshare Precision]], [[POET Technologies]], [[STMicroelectronics]], [[Semtech]], [[Sivers Semiconductor]]

**L8 — Networking Systems**
[[ALL.SPACE]], [[Arista Networks]], [[Cisco]]

**L9 — Servers & ODM/OEM**
[[Celestica]], [[Dell Technologies]], [[Flex]], [[Foxconn (Hon Hai)]], [[Hewlett Packard Enterprise]], [[Supermicro]], [[Wiwynn]]

**L10 — Hyperscalers / Cloud**
[[Alphabet (Google)]], [[Amazon]], [[Apple]], [[ByteDance]], [[CoreWeave]], [[IREN]], [[Meta Platforms]], [[Microsoft]], [[Naver]], [[Nebius]], [[Oracle]], [[SpaceX (Colossus compute)]]

**L11 — AI Labs / Model Developers**
[[Anthropic]], [[OpenAI]], [[xAI]]

**L12 — Datacenter Infrastructure (REITs)**
[[Applied Digital]], [[Blackstone]], [[Cipher Mining]], [[Core Scientific]], [[Digital Realty]], [[Equinix]]

**L13 — Power & Cooling Equipment**
[[Analog Devices]], [[Bloom Energy]], [[Doosan]], [[Eaton]], [[Infineon]], [[Texas Instruments]], [[Vertiv]]

**L14 — Power Generation / Utilities**
[[Constellation Energy]], [[GE Vernova]], [[Vistra]]

## Demand drivers (themes)
[[AI Inference Demand]], [[AI Training Capex]], [[China Indigenous AI Buildout]], [[Co-Packaged Optics (CPO)]], [[CoWoS Advanced Packaging]], [[Datacenter Power Demand]], [[Glass Core Substrate]], [[HBM Demand]], [[Liquid Cooling Adoption]], [[Optical & Networking Buildout]]

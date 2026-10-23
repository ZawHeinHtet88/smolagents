# smolagents ကို local မှာ လေ့ကျင့်ရန်

ဒီ folder က Hugging Face Spaces / GPU မလိုဘဲ ကိုယ့် Windows computer မှာ lesson တွေကို တစ်ဆင့်ချင်း run လုပ်ဖို့ပါ။ `00` က အင်တာနက်နှင့် token မလိုတဲ့ simulation ဖြစ်ပါတယ်။ `01`–`05` က Hugging Face inference ကို တကယ်ခေါ်ပါတယ်။

## 1. Setup (PowerShell)

```powershell
cd D:\projects\smolagents
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

ဒီ computer မှာ Python 3.13 နဲ့ virtual environment ကို ဖန်တီးပြီး dependencies install လုပ်ထားပြီးပါပြီ။ နောက်တစ်ကြိမ် install ပြန်မလိုပါ။

Hugging Face မှာ [Access Token](https://huggingface.co/settings/tokens) တစ်ခု ဖန်တီးပြီး `.env` ထဲက `HF_TOKEN=...` ကို ကိုယ့် token နဲ့ပြောင်းပါ။ Token ကို chat, Git, screenshot ထဲ မတင်ပါနှင့်။ Token ရဲ့ permission က inference အတွက် လုံလောက်ရပါမယ်။ Account ရဲ့ inference quota / model availability ပေါ်မူတည်ပြီး online lessons တချို့ error ပေးနိုင်ပါတယ်။

## Gemini Pro ကိုသုံးရန်

Gemini Pro subscription က `gemini.google.com` အတွက်ဖြစ်ပြီး API အသုံးပြုခွင့်နဲ့ quota က သီးခြားဖြစ်ပါတယ်။ Agent script တွေမှာ Gemini သုံးရန် [Google AI Studio API key](https://aistudio.google.com/apikey) ယူပြီး `.env` ထဲမှာ အောက်ပါအတိုင်း ထည့်ပါ။ API key ကို မမျှဝေပါနှင့်။

```dotenv
MODEL_PROVIDER=gemini
GEMINI_API_KEY=AIzaSy_your_key_here
GEMINI_MODEL=gemini-2.5-flash
```

ပြီးရင် run ပါ—

```powershell
.\.venv\Scripts\python.exe 01_code_agent.py
```

API key မရှိသေးရင် Gemini Pro account ရှိတာတစ်ခုတည်းနဲ့ ဒီ Python script က Gemini ကို မခေါ်နိုင်ပါ။ Google AI Studio ရဲ့ API quota / billing setting အပေါ်မူတည်ပြီး free quota ရှိနိုင်သော်လည်း အမြဲတမ်း credit မလိုဘူးလို့ မယူဆပါနှင့်။

## 2. အစဉ်လိုက် run လုပ်ရန်

```powershell
.\.venv\Scripts\python.exe 00_observe_cycle.py
.\.venv\Scripts\python.exe 01_code_agent.py
.\.venv\Scripts\python.exe 02_tool_calling_agent.py
.\.venv\Scripts\python.exe 03_agentic_rag.py
.\.venv\Scripts\python.exe 04_multi_agent.py
```

| ဖိုင် | သင်ယူမယ့်အရာ |
| --- | --- |
| `00_observe_cycle.py` | Thought → Action → Observation → Answer ကို token မလိုဘဲမြင်ရန် |
| `01_code_agent.py` | `CodeAgent` က Python code ရေးပြီး tool သုံးပုံ |
| `02_tool_calling_agent.py` | `ToolCallingAgent` က structured tool call သုံးပုံ |
| `03_agentic_rag.py` | Local notes ထဲမှ BM25 search tool ခေါ်ပြီးမှဖြေပုံ |
| `04_multi_agent.py` | Manager က `venue_researcher` ကို အလုပ်ခွဲပေးပုံ |
| `05_vision_agent.py` | Image ကို vision model ဆီ ပို့ပြီး မေးပုံ |

`01` နှင့် `02` မှာ တူညီတဲ့ tools ကိုသုံးထားတာကြောင့် log ကိုယှဉ်ကြည့်ပါ။ `CodeAgent` မှာ generated Python code ကို မြင်ရမယ်။ `ToolCallingAgent` မှာ tool name နဲ့ arguments ကို မြင်ရမယ်။ `03` မှာ query ပြောင်းပြီး `search_party_notes()` က ဘယ် notes ကိုပြန်ပေးသလဲ စမ်းကြည့်ပါ။

## 3. Vision lesson

`.env` ထဲမှာ သင့် account က ခေါ်နိုင်တဲ့ vision model ကို `HF_VISION_MODEL=...` အဖြစ်ထည့်ပြီး ကိုယ့် image path ကို ပေးပါ။ Model က image input ကို support လုပ်ရပါမယ်။

```powershell
.\.venv\Scripts\python.exe 05_vision_agent.py "D:\path\to\photo.png"
```

## မကြာခဏတွေ့ရတဲ့ error

- `HF_TOKEN မတွေ့ပါ`: `.env` ဖိုင်ရှိမရှိနဲ့ token ထည့်ပြီးပြီလား စစ်ပါ။
- `401` / `403`: token မှားခြင်း၊ permission သို့မဟုတ် model access မရှိခြင်း ဖြစ်နိုင်ပါတယ်။
- `model unavailable` / `provider error`: `.env` ထဲ `HF_MODEL=` ကို account က inference ခေါ်နိုင်တဲ့ model ID နဲ့ သတ်မှတ်ပါ။ Tool calling lesson အတွက် tool calling support ရတဲ့ model ရွေးပါ။
- `rate limit` / `quota`: account limit ပြည့်နေပါတယ်။ ခဏစောင့်ပြီး ပြန်စမ်းပါ၊ သို့မဟုတ် အသုံးပြုခွင့်ရှိတဲ့ provider ကို ရွေးပါ။
- `.ps1` activation blocked: activation လုပ်ရန်မလိုပါ။ အထက်က `.\.venv\Scripts\python.exe` ကို တိုက်ရိုက်သုံးပါ။

စစ်ဆေးထားတာ: Python 3.13 ပေါ်မှာ package install, offline example, tool calls, syntax check အောင်မြင်ပါတယ်။ Token ထည့်ပြီး inference server ကို စမ်းခေါ်ရာမှာ Hugging Face က `402 Payment Required — no remaining credits` ပြန်ခဲ့ပါတယ်။ Online lessons တွေကို run ဖို့ account မှာ inference credits ရှိဖို့လိုပါတယ်။

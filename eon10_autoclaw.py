#!/usr/bin/env python3
"""EON10 DR DOOM — Autoclaw Bot. jev reasoning + gpt6 content via Explabs gateway."""

import os, json, time, requests
from datetime import datetime

BOT_TOKEN = os.environ.get("EON10_BOT_TOKEN", "8680913270:AAERwtVz1xpVz8xACgCZpWTeYmeNTqxZdn4")
ADMIN_CHAT_ID = int(os.environ.get("EON10_ADMIN_CHAT_ID", "6499054466"))
EXPLABS_KEY = os.environ.get("EXPLABS_API_KEY", "xpl_08b9a0678b55f04281447e9a993e538ffe1394c1")
ORG_ID = "69781319-690d-44d5-9ea1-ffebe31c0d8f"

VAULT = r"C:\Users\princ\Documents\Obsidian Vault\EON10Secrets"

EXPLABS_BASE = "https://api.experientiallabs.ai"
HEADERS = {"Authorization": f"Bearer {EXPLABS_KEY}", "Content-Type": "application/json"}

users = {}
jobs = {}

def load_soul():
    try:
        with open(os.path.join(VAULT, "SOUL.md")) as f:
            return f.read()
    except:
        return "EON10 DR DOOM"

def load_agents():
    try:
        with open(os.path.join(VAULT, "agents.md")) as f:
            return f.read()
    except:
        return ""

def load_memo():
    try:
        with open(os.path.join(VAULT, "memo.json")) as f:
            return json.load(f)
    except:
        return {}

def load_guardian():
    try:
        with open(os.path.join(VAULT, "guardian.md")) as f:
            return f.read()
    except:
        return ""

def call_jev(state_task, diff_summary="", test_summary=""):
    payload = {
        "model": "type-safe/jev-latest",
        "state": {"task": state_task, "diff_summary": diff_summary, "test_summary": test_summary},
        "questions": {
            "decision": {
                "type": "choice",
                "instructions": "Decide the best next action.",
                "criteria": {"proceed": "Safe to proceed.", "review": "Needs info.", "block": "Blocked."}
            }
        }
    }
    try:
        r = requests.post(f"{EXPLABS_BASE}/v1/systemone", headers=HEADERS, json=payload, timeout=15)
        if r.status_code == 200:
            return r.json().get("answers", {}).get("decision", "review")
    except Exception as e:
        return f"error: {e}"
    return "review"

def call_gpt6(messages, reasoning="low"):
    payload = {"model": "openai/gpt-6-luna", "messages": messages, "reasoning_effort": reasoning, "max_tokens": 1024}
    try:
        r = requests.post(f"{EXPLABS_BASE}/api/v1/chat/completions", headers=HEADERS, json=payload, timeout=15)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"error: {e}"
    return "Erreur GPT6"

def render_spot(duration=5, resolution="640x360"):
    job_id = f"spot_{int(time.time())}"
    jobs[job_id] = {"status": "rendering", "started": datetime.now().isoformat()}
    decision = call_jev(f"Render a {duration}s motion spot at {resolution}", "New render job", "No prior renders")
    if decision != "proceed":
        jobs[job_id]["status"] = "blocked"
        jobs[job_id]["reason"] = decision
        return job_id, "Blocked by jev"
    prompt = call_gpt6([
        {"role": "system", "content": "Tu es directeur artistique motion design."},
        {"role": "user", "content": "Spot motion design africain, couleurs vives, style publicitaire ivoirienne."}
    ], reasoning="low")
    jobs[job_id]["prompt"] = prompt
    jobs[job_id]["status"] = "rendered"
    jobs[job_id]["completed"] = datetime.now().isoformat()
    return job_id, prompt

def main_keyboard():
    return {"keyboard": [["🚀 SaaS-MCP", "👥 Community"], ["🧠 RAG Marché", "💰 Abonnement"], ["👤 Mon compte", "👥 Amis"], ["🎨 Render Spot", "📊 Jobs"], ["❓ FAQ", "🛠 Support"]], "resize_keyboard": True}

def account_keyboard():
    return {"keyboard": [["💳 Dépôt", "📊 Stats"], ["🔙 Menu principal"]], "resize_keyboard": True}

def handle_start(update, context):
    chat_id = update.message.chat_id
    users[chat_id] = {"created": datetime.now().isoformat(), "tokens": 100, "referrals": 0, "orders": 0, "plan": "Gratuit", "autoclaw": False}
    msg = "🚀 *EON10 DR DOOM — Autoclaw*\n\nCompte créé ✅\nMode : DÉMO\nPlan : Gratuit\nAutoclaw : ⏸️ OFF\n\n/utiliser → activer\n/render → spot Blender\n/status → mon status"
    update.message.reply_text(msg, parse_mode="Markdown", reply_markup=main_keyboard())

def handle_message(update, context):
    text = update.message.text.lower().strip()
    chat_id = update.message.chat_id
    user = users.get(chat_id, {})
    
    if text in ["/utiliser", "utiliser", "autoclaw", "autoclaw on"]:
        if chat_id in users: users[chat_id]["autoclaw"] = True
        update.message.reply_text("🤖 *Autoclaw activé*\n\njev (raisonnement) + gpt6 (contenu).\n/render → spot\n/jobs → status\n/stop → désactiver", parse_mode="Markdown", reply_markup=main_keyboard())
        return
    
    if text in ["/render", "render", "🎨 render spot"]:
        if not user.get("autoclaw"):
            update.message.reply_text("⚠️ Active d'abord l'autoclaw : /utiliser", parse_mode="Markdown", reply_markup=main_keyboard())
            return
        job_id, result = render_spot(duration=5, resolution="640x360")
        update.message.reply_text(f"🎨 *Render Spot*\n\nJob : `{job_id}`\nStatus : {jobs[job_id]['status']}\nPrompt : {result[:200]}...", parse_mode="Markdown", reply_markup=main_keyboard())
        return
    
    if text in ["/jobs", "jobs", "📊 jobs"]:
        active = [j for j in jobs.values() if j['status'] == 'rendering']
        done = [j for j in jobs.values() if j['status'] == 'rendered']
        msg = f"📊 *Jobs*\n\nEn cours : {len(active)}\nTerminés : {len(done)}"
        if done: msg += f"\n\nDernier : {done[-1].get('prompt', '')[:100]}..."
        update.message.reply_text(msg, parse_mode="Markdown", reply_markup=main_keyboard())
        return
    
    if text in ["/stop", "stop"]:
        if chat_id in users: users[chat_id]["autoclaw"] = False
        update.message.reply_text("⏸️ Autoclaw désactivé.", reply_markup=main_keyboard())
        return
    
    FAQ_DB = {
        "que peut faire": "🚀 *EON10 DR DOOM :*\n• Friendises afrodisiaques\n• Community management\n• RAG marché ivoirien\n• Motion design Blender\n• Autoclaw autonome",
        "comment gagner": "💰 Abonnement + commissions + parrainage.",
        "prix": "🆓 Gratuit | ⭐ Pro 5,000 FCFA | 👑 Premium 15,000 FCFA",
        "paiement": "💳 Wave / MTN / Orange Money",
        "commandes": "/start /menu /faq /compte /parrain /signal /auto /depot /bug",
        "support": "🛠 @DRDOOM_support",
    }
    for key, response in FAQ_DB.items():
        if key in text:
            update.message.reply_text(response, parse_mode="Markdown", reply_markup=main_keyboard())
            return
    
    if user.get("autoclaw"):
        ai_msg = call_gpt6([{"role": "system", "content": "Tu es DR DOOM, orchestrateur EON10. Réponds en français, concis, action."}, {"role": "user", "content": text}], reasoning="low")
        update.message.reply_text(ai_msg, parse_mode="Markdown", reply_markup=main_keyboard())
        return
    
    if text == "🚀 saas-mcp":
        update.message.reply_text("🚀 *SaaS-MCP*\nFriendises afrodisiaques.", parse_mode="Markdown", reply_markup=main_keyboard())
    elif text == "👥 community":
        update.message.reply_text("👥 *Community*\n/outreach → campagne", parse_mode="Markdown", reply_markup=main_keyboard())
    elif text == "🧠 rag marché":
        update.message.reply_text("🧠 *RAG Marché*\nTendances + prix.", parse_mode="Markdown", reply_markup=main_keyboard())
    elif text == "💰 abonnement":
        update.message.reply_text("💰 *Plans :*\n🆓 Gratuit | ⭐ Pro 5,000 FCFA | 👑 Premium 15,000 FCFA", parse_mode="Markdown", reply_markup=main_keyboard())
    elif text == "👤 mon compte":
        tokens = user.get("tokens", 0)
        plan = user.get("plan", "Gratuit")
        auto = "✅" if user.get("autoclaw") else "⏸️"
        update.message.reply_text(f"👤 *Compte*\nPlan : {plan}\nTokens : {tokens}\nAutoclaw : {auto}", parse_mode="Markdown", reply_markup=account_keyboard())
    elif text == "👥 amis":
        update.message.reply_text("👥 *Parrainage*\n/parrain → lien", parse_mode="Markdown", reply_markup=main_keyboard())
    elif text == "❓ faq":
        update.message.reply_text("❓ *FAQ*\n/commandes → liste", parse_mode="Markdown", reply_markup=main_keyboard())
    elif text == "🛠 support":
        update.message.reply_text("🛠 *Support*\n@DRDOOM_support", parse_mode="Markdown", reply_markup=main_keyboard())
    elif text == "💳 dépôt":
        update.message.reply_text("💳 *Dépôt*\nWave / MTN / Orange", parse_mode="Markdown", reply_markup=account_keyboard())
    elif text == "📊 stats":
        update.message.reply_text(f"📊 *Stats*\nTokens : {user.get('tokens', 0)}", parse_mode="Markdown", reply_markup=account_keyboard())
    elif text == "🔙 menu principal" or text == "menu":
        update.message.reply_text("🔙 Retour.", reply_markup=main_keyboard())
    else:
        update.message.reply_text("🤔 Question ? Utilise le menu ou /commandes.", parse_mode="Markdown", reply_markup=main_keyboard())

def handle_callback(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(f"✅ {query.data}")

def main():
    from telegram import Update
    from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_callback))
    print("EON10 DR DOOM Autoclaw démarré...")
    app.run_polling()

if __name__ == "__main__":
    main()

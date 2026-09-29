#!/usr/bin/env python3
"""
EON10 Bot — Telegram interface for DR DOOM SaaS-MCP stack.
Mirrors the Top PO Robot pattern: menu grid, account, deposit, friends, FAQ.
"""

import os
import json
import time
from datetime import datetime

BOT_TOKEN = os.environ.get("EON10_BOT_TOKEN", "8680913270:AAERwtVz1xpVz8xACgCZpWTeYmeNTqxZdn4")
ADMIN_CHAT_ID = os.environ.get("EON10_ADMIN_CHAT_ID", "6499054466")

# In-memory storage (replace with SQLite/Redis for production)
users = {}

def help_text():
    return """🤖 *EON10 DR DOOM* — Bot officiel

Menu principal :
""".strip()

def main_menu():
    return """🔥 *EON10 DR DOOM*

Sélectionne ton action :"""

def main_keyboard():
    return {
        "keyboard": [
            ["🚀 SaaS-MCP", "👥 Community"],
            ["🧠 RAG Marché", "💰 Abonnement"],
            ["👤 Mon compte", "👥 Amis"],
            ["❓ FAQ", "🛠 Support"],
        ],
        "resize_keyboard": True,
    }

def account_keyboard():
    return {
        "keyboard": [
            ["💳 Dépôt", "📊 Stats"],
            ["🔙 Menu principal"],
        ],
        "resize_keyboard": True,
    }

def faq_text():
    return """❓ *FAQ EON10*

Q: C'est quoi EON10 ?
R: Plateforme de friendises afrodisiaques pour commerçantes ivoiriennes.

Q: Comment ça marche ?
R: Abonnement + commissions sur les ventes.

Q: Paiement ?
R: Mobile Money, Wave, MTN.

Q: Support ?
R: @DRDOOM_support ou ce bot.
"""

def handle_start(update, context):
    chat_id = update.message.chat_id
    users[chat_id] = {"created": datetime.now().isoformat(), "tokens": 100, "referrals": 0}
    
    msg = f"""🚀 *Bienvenue sur EON10 DR DOOM*

Compte créé ! ✅
Mode : DÉMO
Tokens : 100

Tu es prêt pour les friendises afrodisiaques.
"""
    update.message.reply_text(msg, parse_mode="Markdown", reply_markup=main_keyboard())

def handle_message(update, context):
    text = update.message.text
    chat_id = update.message.chat_id
    
    if text == "🚀 SaaS-MCP":
        update.message.reply_text(
            "🚀 *SaaS-MCP*\n\nFriendises afrodisiaques — abonnement + commissions.\n\nCommandes :\n/friendise → lancer\n/status → voir status\n/stop → arrêter",
            parse_mode="Markdown", reply_markup=main_keyboard()
        )
    elif text == "👥 Community":
        update.message.reply_text(
            "👥 *Community AAAIAA*\n\nGestion communauté style Pierre-Evrard.\n\n/outreach → lancer campagne\n/reports → rapports",
            parse_mode="Markdown", reply_markup=main_keyboard()
        )
    elif text == "🧠 RAG Marché":
        update.message.reply_text(
            "🧠 *RAG MCP Marché*\n\nMémoire marché ivoirien.\n\n/market → tendances\n/prices → prix\n/clientes → base",
            parse_mode="Markdown", reply_markup=main_keyboard()
        )
    elif text == "💰 Abonnement":
        update.message.reply_text(
            "💰 *Abonnement*\n\nPlans :\n• Gratuit : 5 friendises/mois\n• Pro : 50 friendises/mois — 5,000 FCFA\n• Premium : illimité — 15,000 FCFA\n\n/depot → payer",
            parse_mode="Markdown", reply_markup=main_keyboard()
        )
    elif text == "👤 Mon compte":
        user = users.get(chat_id, {})
        tokens = user.get("tokens", 0)
        created = user.get("created", "N/A")
        update.message.reply_text(
            f"👤 *Mon compte*\n\nCompte : {chat_id}\nTokens : {tokens}\nCréé : {created}\nAmis : {user.get('referrals', 0)}",
            parse_mode="Markdown", reply_markup=account_keyboard()
        )
    elif text == "👥 Amis":
        update.message.reply_text(
            "👥 *Parrainage*\n\nInvite des amies → 10% de commission.\n\n/parrain → lien parrainage\n/classement → top parraineurs",
            parse_mode="Markdown", reply_markup=main_keyboard()
        )
    elif text == "❓ FAQ":
        update.message.reply_text(faq_text(), parse_mode="Markdown", reply_markup=main_keyboard())
    elif text == "🛠 Support":
        update.message.reply_text(
            "🛠 *Support*\n\nContacte @DRDOOM_support\nOu utilise /bug pour signaler un problème.",
            parse_mode="Markdown", reply_markup=main_keyboard()
        )
    elif text == "💳 Dépôt":
        update.message.reply_text(
            "💳 *Dépôt*\n\nModes :\n• Wave\n• MTN Mobile Money\n• ORANGE Money\n\n/envoyer <montant> → payer",
            parse_mode="Markdown", reply_markup=account_keyboard()
        )
    elif text == "📊 Stats":
        user = users.get(chat_id, {})
        update.message.reply_text(
            f"📊 *Stats*\n\nTokens : {user.get('tokens', 0)}\nAmis : {user.get('referrals', 0)}\nCommandes : {user.get('orders', 0)}",
            parse_mode="Markdown", reply_markup=account_keyboard()
        )
    elif text == "🔙 Menu principal":
        update.message.reply_text("🔙 Retour menu.", reply_markup=main_keyboard())
    else:
        update.message.reply_text("Commande inconnue. Utilise le menu.", reply_markup=main_keyboard())

def handle_callback(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(f"✅ Action : {query.data}")

def main():
    from telegram import Update, ReplyKeyboardMarkup
    from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_callback))
    
    print("EON10 Bot démarré...")
    app.run_polling()

if __name__ == "__main__":
    main()

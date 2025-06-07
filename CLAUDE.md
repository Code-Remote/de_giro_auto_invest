# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an automated investment application that integrates with DEGIRO to automatically invest in the Vanguard S&P 500 ETF (VUAA). The application calculates investment amounts based on available cash balance and sends notifications via Telegram.

## Communication Shortcuts

The user may use these prefixes to indicate the type of response needed:
- `q:` - Questions/explanations only, do NOT generate code
- `x:` - Explanations/discussions only, do NOT generate code  
- `c:` - Generate code/implementation as requested

When you see `q:` or `x:`, provide explanations, advice, and discussions but never generate code unless explicitly overridden. You are allowed to display short code snippets to make it easier to understand in your answer but not change any files

## Code Generation sounds

- When generating code, and you need my input, just before prompting for input can you run the `say "Need some input"` command so that my macBook will play a sound to notify me that you need my input. This is useful when I am not looking at the screen and I can hear the sound and come back to the screen to provide you with the input you need.
- When you are done generating code and at the end of updating your todos and after displaying the changes made (so at the total end), please run the `say "Done coding"` command so that I know you have finished generating the code and I can review it.

## Commands

### Setup and Run
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the investment script
python main.py
```

### Environment Variables Required
Create a `.env` file with:
- `DEGIRO_INT_ACCOUNT` - DEGIRO account number
- `DEGIRO_USERNAME` - DEGIRO username
- `DEGIRO_PASSWORD` - DEGIRO password
- `DEGIRO_2FA_SECRET_KEY` - TOTP secret for 2FA
- `TELEGRAM_TOKEN` - Telegram bot token
- `TELEGRAM_CHAT_ID` - Telegram chat ID for notifications

## Architecture

### Core Investment Logic (main.py)
- Retrieves available cash from DEGIRO (keeps €100 buffer for fees)
- Calculates share quantities based on current ETF price
- Places market orders through DEGIRO API
- Sends success/failure notifications via Telegram

### Service Layer
- **degiro_service.py**: Wrapper around degiro-connector library handling authentication, portfolio queries, and order placement
- **telegram_service.py**: Telegram notifications using aiogram
- **whatsapp_service.py**: Alternative notification channel (not currently used in main flow)

### Key Implementation Details
- Investment target: Vanguard S&P 500 ETF (VUAA) - DEGIRO ID: 16954338
- Only buys whole shares (uses floor calculation)
- Maintains €100 cash buffer for fees
- Handles DEGIRO 2FA automatically using TOTP
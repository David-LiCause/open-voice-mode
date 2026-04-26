CLAUDE_URL   = https://www.icloud.com/shortcuts/83c4ec4e95f24b4681d013748da4834f
CLAUDE_NAME  = Talk To Claude
CHATGPT_URL  = https://www.icloud.com/shortcuts/a243d6a0ef5148b181a7fa79265c7dae
CHATGPT_NAME = Talk To ChatGPT
GEMINI_URL   = https://www.icloud.com/shortcuts/fc080490d7bb4ae9bcefdd126ee6bdc9
GEMINI_NAME  = Talk To Gemini

CHECK = python3 tests/check_link.py

.PHONY: test test-claude test-chatgpt test-gemini

test: test-claude test-chatgpt test-gemini

test-claude:
	@$(CHECK) "$(CLAUDE_URL)" "$(CLAUDE_NAME)"

test-chatgpt:
	@$(CHECK) "$(CHATGPT_URL)" "$(CHATGPT_NAME)"

test-gemini:
	@$(CHECK) "$(GEMINI_URL)" "$(GEMINI_NAME)"

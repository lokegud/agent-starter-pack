#!/usr/bin/env python3
"""Test Claude API connection"""

import os
import sys
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_claude_api():
    """Test Claude API connection"""

    print("=" * 60)
    print("Testing Claude API Connection")
    print("=" * 60)

    # Check if API key is set
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        print("\n❌ ERROR: ANTHROPIC_API_KEY not found in environment")
        print("\nPlease:")
        print("1. Go to https://console.anthropic.com/")
        print("2. Create an API key")
        print("3. Add it to your .env file:")
        print("   ANTHROPIC_API_KEY=sk-ant-your-key-here")
        return False

    if api_key == "your-anthropic-key-here":
        print("\n⚠️  WARNING: You still have the placeholder API key")
        print("\nPlease:")
        print("1. Go to https://console.anthropic.com/")
        print("2. Create an API key")
        print("3. Replace the placeholder in your .env file")
        return False

    # Initialize client
    try:
        client = Anthropic(api_key=api_key)
        print(f"\n✓ API key loaded (starts with: {api_key[:20]}...)")
    except Exception as e:
        print(f"\n❌ Failed to initialize client: {e}")
        return False

    # Test API call
    print("\n🤖 Testing Claude API call...")
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say 'Hello from Agent City!' and confirm you're working. Keep it brief."
                }
            ]
        )

        response_text = message.content[0].text

        print("\n" + "=" * 60)
        print("✅ SUCCESS! Claude API is working!")
        print("=" * 60)
        print(f"\nClaude says:\n{response_text}")
        print("\n" + "=" * 60)
        print(f"Tokens used: {message.usage.input_tokens} input + {message.usage.output_tokens} output")
        print("=" * 60)

        return True

    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ ERROR: API call failed")
        print("=" * 60)
        print(f"\nError: {e}")
        print("\nPossible issues:")
        print("- Invalid API key")
        print("- Network connectivity")
        print("- API quota exceeded")
        print("- Anthropic service issue")
        return False


if __name__ == "__main__":
    success = test_claude_api()
    sys.exit(0 if success else 1)

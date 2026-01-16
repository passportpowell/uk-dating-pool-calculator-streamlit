#!/usr/bin/env python3
"""Test script to verify all imports work correctly."""

import sys
sys.path.insert(0, '.')

# Test imports
tests = []

print("Testing imports...\n")

try:
    from src.utils.styles import CUSTOM_CSS
    print('✓ Styles')
    tests.append(True)
except Exception as e:
    print(f'✗ Styles: {str(e)[:50]}')
    tests.append(False)

try:
    from src.data.constants import UK_ADULT_POPULATION
    print('✓ Data constants')
    tests.append(True)
except Exception as e:
    print(f'✗ Data: {str(e)[:50]}')
    tests.append(False)

try:
    from src.calculations.dating_pool import calculate_age_probability
    print('✓ Calculations')
    tests.append(True)
except Exception as e:
    print(f'✗ Calc: {str(e)[:50]}')
    tests.append(False)

try:
    from src.ai.assistant import AIAssistant
    print('✓ AI assistant')
    tests.append(True)
except Exception as e:
    print(f'✗ AI: {str(e)[:50]}')
    tests.append(False)

try:
    from src.ui.sidebar import create_sidebar
    print('✓ UI sidebar')
    tests.append(True)
except Exception as e:
    print(f'✗ UI: {str(e)[:50]}')
    tests.append(False)

success = sum(tests)
total = len(tests)
print('\n' + '='*50)
if success == total:
    print(f'✅ All {total} imports PASSED!')
    sys.exit(0)
else:
    print(f'⚠️  {success}/{total} imports passed')
    sys.exit(1)

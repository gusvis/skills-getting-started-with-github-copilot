#!/bin/bash

# Test script for Mergington High School API
echo "🧪 Running tests for Mergington High School API"
echo "================================================"

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=term-missing --cov-report=html -v

echo ""
echo "✅ Tests completed!"
echo "📊 Coverage report saved to htmlcov/index.html"
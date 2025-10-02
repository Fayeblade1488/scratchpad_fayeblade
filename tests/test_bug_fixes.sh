#!/bin/bash
#
# Meta Test Suite for Core Validation Scripts
#
# DESCRIPTION:
#   This script validates that the primary Python-based test suites
#   in the repository are executable and run without errors. It serves as
#   a regression test to ensure that the core testing infrastructure
#   remains functional.
#
# USAGE:
#   ./test_bug_fixes.sh
#
# EXIT CODES:
#   0 - All core test suites are healthy.
#   1 - One or more core test suites failed to execute.
#

set -euo pipefail

# Test configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
TEST_COUNT=0
PASS_COUNT=0
FAIL_COUNT=0

# Function to log test results
log_test_result() {
    local test_name="$1"
    local result="$2"
    local details="${3:-}"
    
    TEST_COUNT=$((TEST_COUNT + 1))
    echo -n "Test $TEST_COUNT: $test_name ... "
    
    if [ "$result" -eq 0 ]; then
        echo "PASS"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo "FAIL"
        [ -n "$details" ] && echo "  Details: $details"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
}

# Test 1: Validate the main YAML framework test suite
test_yaml_frameworks_suite() {
    local test_script="$BASE_DIR/tests/test_yaml_frameworks.py"
    
    if python3 "$test_script"; then
        log_test_result "YAML frameworks test suite executes successfully" 0
    else
        log_test_result "YAML frameworks test suite executes successfully" 1 "test_yaml_frameworks.py failed. Run it directly for details."
    fi
}

# Test 2: Validate the scripts test suite
test_scripts_suite() {
    local test_script="$BASE_DIR/tests/test_scripts.py"

    if python3 "$test_script"; then
        log_test_result "Utility scripts test suite executes successfully" 0
    else
        log_test_result "Utility scripts test suite executes successfully" 1 "test_scripts.py failed. Run it directly for details."
    fi
}

# Function to print the final summary
print_summary() {
    echo
    echo "=== Core Test Suite Validation Summary ==="
    echo "Total Tests: $TEST_COUNT"
    echo "Passed:      $PASS_COUNT"
    echo "Failed:      $FAIL_COUNT"
    echo
    
    if [ $FAIL_COUNT -eq 0 ]; then
        echo "All core test suites are healthy. ✓"
        return 0
    else
        echo "One or more core test suites are failing. ✗"
        return 1
    fi
}

# Main execution
main() {
    echo "=== Core Test Suite Validation ==="
    echo "Verifying that the main Python test suites are operational..."
    echo
    
    # Execute all test cases
    test_yaml_frameworks_suite
    test_scripts_suite
    
    # Print results and exit
    print_summary
}

main "$@"
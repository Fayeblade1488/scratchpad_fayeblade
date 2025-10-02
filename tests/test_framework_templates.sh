#!/bin/bash
#
# Framework Template Validation Test Suite
#
# DESCRIPTION:
#   Validates the integrity and completeness of the Scratchpad framework
#   repository structure and essential files.
#
# USAGE:
#   ./test_framework_templates.sh
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

# Test 1: Check for core framework directories
test_framework_directories_exist() {
    local missing_dirs=()
    local framework_dirs=("core" "purpose-built" "personas")
    
    for dir in "${framework_dirs[@]}"; do
        if [ ! -d "$BASE_DIR/frameworks/$dir" ]; then
            missing_dirs+=("$dir")
        fi
    done
    
    if [ ${#missing_dirs[@]} -eq 0 ]; then
        log_test_result "Framework directories exist" 0
        return 0
    else
        log_test_result "Framework directories exist" 1 "Missing: ${missing_dirs[*]}"
        return 1
    fi
}

# Test 2: Check that framework directories are not empty
test_framework_directories_not_empty() {
    local empty_dirs=()
    local framework_dirs=("core" "purpose-built" "personas")

    for dir in "${framework_dirs[@]}"; do
        file_count=$(find "$BASE_DIR/frameworks/$dir" -name "*.yml" -o -name "*.yaml" | wc -l)
        if [ "$file_count" -eq 0 ]; then
            empty_dirs+=("$dir")
        fi
    done

    if [ ${#empty_dirs[@]} -eq 0 ]; then
        log_test_result "Framework directories contain files" 0
        return 0
    else
        log_test_result "Framework directories contain files" 1 "Empty: ${empty_dirs[*]}"
        return 1
    fi
}

# Test 3: Check that framework files have content
test_frameworks_not_empty() {
    local small_files=()
    local min_size=100 # Minimum size in bytes
    
    while IFS= read -r -d '' file; do
        local size
        size=$(stat -c%s "$file" 2>/dev/null || echo 0)
        
        if [ "$size" -lt $min_size ]; then
            local rel_path="${file#$BASE_DIR/}"
            small_files+=("$rel_path ($size bytes)")
        fi
    done < <(find "$BASE_DIR/frameworks" -name "*.yml" -o -name "*.yaml" -print0)
    
    if [ ${#small_files[@]} -eq 0 ]; then
        log_test_result "Frameworks have adequate content" 0
        return 0
    else
        log_test_result "Frameworks have adequate content" 1 "Small files: ${small_files[*]}"
        return 1
    fi
}

# Test 4: Check for license file
test_license_file_exists() {
    local license_file="$BASE_DIR/license.txt"
    if [ -f "$license_file" ] && [ -s "$license_file" ]; then
        log_test_result "License file exists and has content" 0
    else
        log_test_result "License file exists and has content" 1 "license.txt not found or is empty"
    fi
}

# Function to print the final summary
print_summary() {
    echo
    echo "=== Framework Template Validation Summary ==="
    echo "Total Tests: $TEST_COUNT"
    echo "Passed:      $PASS_COUNT"
    echo "Failed:      $FAIL_COUNT"
    echo
    
    if [ $FAIL_COUNT -eq 0 ]; then
        echo "All framework validation tests PASSED! ✓"
        return 0
    else
        echo "Some framework validation tests FAILED! ✗"
        return 1
    fi
}

# Main execution
main() {
    echo "=== Framework Template Validation Test Suite ==="
    echo "Base directory: $BASE_DIR"
    echo
    
    # Execute all test cases
    test_framework_directories_exist
    test_framework_directories_not_empty
    test_frameworks_not_empty
    test_license_file_exists
    
    # Print results and exit
    print_summary
}

main "$@"
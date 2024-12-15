*** Settings ***
Library           parallel_execution_keyword.py
*** Variables ***
${LAST_GUESSED_NUMBER}    ${50}
*** Tasks ***
Run Parallel demo
    Log To Console   last guess: ${LAST_GUESSED_NUMBER}
    start_guess_number_1_to_100_parallel       10
    start_guess_number_1_to_100_parallel       20
    start_guess_number_1_to_100_parallel       30
    wait_for_completion_of_parallel_tasks
    Log    ${LAST_GUESSED_NUMBER}
    Log To Console   last guess: ${LAST_GUESSED_NUMBER}



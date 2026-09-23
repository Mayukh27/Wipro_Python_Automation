*** Settings ***
Library    libraries/custom_library.py
Library    String

*** Test Cases ***
Custom Keyword Calculates Sum
    ${result}=    Calculate Sum    12    30
    Should Be Equal As Numbers    ${result}    42

Built In String Operation Converts Case
    ${upper}=    Convert To Upper Case    robot framework
    Should Be Equal    ${upper}    ROBOT FRAMEWORK

Built In Math Operation Evaluates Expression
    ${total}=    Evaluate    15 + 27
    Should Be Equal As Integers    ${total}    42

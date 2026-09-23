*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Library    String
Library    Collections

*** Variables ***
${LOGIN_URL}    https://automationexercise.com/login
${BROWSER}    Chrome
${DATA_FILE}    ${CURDIR}/test_data/data.csv
${EMAIL_INPUT}    css:input[data-qa='login-email']
${PASSWORD_INPUT}    css:input[data-qa='login-password']
${LOGIN_BUTTON}    css:button[data-qa='login-button']
${ERROR_MESSAGE}    css:div.login-form p

*** Test Cases ***
Login Attempts Driven By External CSV Data
    Open Browser    about:blank    ${BROWSER}
    ${file_content}=    Get File    ${DATA_FILE}
    @{lines}=    Split To Lines    ${file_content}
    Remove From List    ${lines}    0
    FOR    ${line}    IN    @{lines}
        @{parts}=    Split String    ${line}    ,
        Attempt Login    ${parts}[0]    ${parts}[1]
    END
    [Teardown]    Close Browser

*** Keywords ***
Attempt Login
    [Arguments]    ${username}    ${password}
    Go To    ${LOGIN_URL}
    Wait Until Page Contains Element    ${EMAIL_INPUT}
    Input Text    ${EMAIL_INPUT}    ${username}
    Input Text    ${PASSWORD_INPUT}    ${password}
    Click Button    ${LOGIN_BUTTON}
    Wait Until Page Contains Element    ${ERROR_MESSAGE}
    Page Should Contain    incorrect

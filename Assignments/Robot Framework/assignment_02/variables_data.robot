*** Settings ***
Library    SeleniumLibrary
Library    DataDriver    file=${CURDIR}/test_data/data.csv    dialect=excel
Suite Setup    Open Browser    about:blank    ${BROWSER}
Suite Teardown    Close Browser
Test Template    Attempt Login

*** Variables ***
${LOGIN_URL}    https://automationexercise.com/login
${BROWSER}    Chrome
${EMAIL_INPUT}    css:input[data-qa='login-email']
${PASSWORD_INPUT}    css:input[data-qa='login-password']
${LOGIN_BUTTON}    css:button[data-qa='login-button']
${ERROR_MESSAGE}    css:div.login-form p

*** Test Cases ***
Login Attempt Using External CSV Data    username    password

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

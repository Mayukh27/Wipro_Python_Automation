*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${LOGIN_URL}    https://automationexercise.com/login
${BROWSER}    Chrome
${EMAIL_INPUT}    css:input[data-qa='login-email']
${PASSWORD_INPUT}    css:input[data-qa='login-password']
${LOGIN_BUTTON}    css:button[data-qa='login-button']

*** Test Cases ***
Open Login Page And Enter Credentials
    Open Browser    ${LOGIN_URL}    ${BROWSER}
    Page Should Contain Element    ${EMAIL_INPUT}
    Input Text    ${EMAIL_INPUT}    basic.syntax.user@example.com
    Page Should Contain Element    ${PASSWORD_INPUT}
    Input Text    ${PASSWORD_INPUT}    BasicSyntax!501
    Page Should Contain Element    ${LOGIN_BUTTON}
    [Teardown]    Close Browser

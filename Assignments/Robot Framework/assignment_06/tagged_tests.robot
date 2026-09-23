*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${SITE_URL}    https://automationexercise.com
${BROWSER}    Chrome

*** Test Cases ***
Home Page Loads Successfully
    [Tags]    smoke
    Open Browser    ${SITE_URL}    ${BROWSER}
    Page Should Contain Element    css:h2
    [Teardown]    Close Browser

Invalid Login Shows Error Message
    [Tags]    regression
    Open Browser    ${SITE_URL}/login    ${BROWSER}
    Input Text    css:input[data-qa='login-email']    tag.test.user@example.com
    Input Text    css:input[data-qa='login-password']    WrongPass!401
    Click Button    css:button[data-qa='login-button']
    Wait Until Page Contains Element    css:div.login-form p
    Page Should Contain    incorrect
    [Teardown]    Close Browser

Product Search Returns Results
    [Tags]    regression    smoke
    Open Browser    ${SITE_URL}/products    ${BROWSER}
    Input Text    css:input#search_product    Dress
    Click Button    css:button#submit_search
    Wait Until Page Contains Element    css:h2.title
    Page Should Contain    Searched Products
    [Teardown]    Close Browser

*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${SITE_URL}    https://automationexercise.com
${BROWSER}    Chrome

*** Test Cases ***
Log Page Title After Navigation
    Open Browser    ${SITE_URL}    ${BROWSER}
    Log    Navigating to the home page to verify the title
    ${title}=    Get Title
    Log    Retrieved page title: ${title}
    Should Be Equal As Strings    ${title}    Automation Exercise
    [Teardown]    Close Browser

Log Search Result Count
    Open Browser    ${SITE_URL}/products    ${BROWSER}
    Input Text    css:input#search_product    Jeans
    Click Button    css:button#submit_search
    Wait Until Page Contains Element    css:div.features_items
    @{results}=    Get WebElements    css:div.product-image-wrapper
    ${count}=    Get Length    ${results}
    Log    Found ${count} products matching 'Jeans'
    Should Be True    ${count} > 0
    [Teardown]    Close Browser

Feature: Home Page
  Tests for the 'https://yandex.ru/' home page
  
  Background: Open home page
    Given I open the browser and expand to the full screen

  Scenario: Tests yandex market
    When I have navigated to the 'ya' "home" page
    Then the page "home"  page opens
    And the if i click popup "all service" contains a "маркет"
    When I click the "маркет" opens a tab with the "маркет"  and go to it
    Then element "каталог" found of page 
    When I click "каталог" 
    Then select "smartphones"
    When Go to All Filters
    Then Search parameter 'price' to and set "20000" rubles
    And Screen diagonal from "3" inches
    Then Select at least "5" of any manufacturers
    When Click "Show..." (on filters)
    Then Count the smartphones on one page and great "10"
    Then Remember name the last smartphones of the list
    When Change Sort to another (by price)
    Then Find the page of exist the stored object
    And Click on the name of the stored object
    And Display the rating of the selected item

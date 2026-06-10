Feature: Manage Work Orders
  As a G2 service technician I want to open the Work Orders screen
  so that I can create and manage work orders for customers

  Background:
    Given G2 is running and the Navigator is open

  @smoke
  Scenario: Open Work Orders screen from the Service menu
    When I navigate to "Work Orders" from the Service menu
    Then the "Astra G2 - Service Manager" window is open and visible

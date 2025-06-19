package com.mrm.modelregistry.selenium;

import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.time.Duration;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class EndToEndSeleniumTest extends BaseSeleniumTest {
    
    @Test
    void testCompleteUserWorkflow() {
        driver.get(getFrontendUrl());
        
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(15));
        
        WebElement modelNameInput = wait.until(driver -> 
            driver.findElement(By.id("modelName")));
        WebElement modelVersionInput = driver.findElement(By.id("modelVersion"));
        WebElement modelSponsorInput = driver.findElement(By.id("modelSponsor"));
        WebElement businessLineSelect = driver.findElement(By.id("businessLine"));
        WebElement modelTypeSelect = driver.findElement(By.id("modelType"));
        WebElement riskRatingSelect = driver.findElement(By.id("riskRating"));
        WebElement statusSelect = driver.findElement(By.id("status"));
        
        modelNameInput.sendKeys("End-to-End Test Model");
        modelVersionInput.sendKeys("v2.0");
        modelSponsorInput.sendKeys("E2E Test Sponsor");
        
        Select businessLineDropdown = new Select(businessLineSelect);
        Select modelTypeDropdown = new Select(modelTypeSelect);
        Select riskRatingDropdown = new Select(riskRatingSelect);
        Select statusDropdown = new Select(statusSelect);
        
        assertTrue(businessLineDropdown.getOptions().size() > 1);
        assertTrue(modelTypeDropdown.getOptions().size() > 1);
        assertTrue(riskRatingDropdown.getOptions().size() > 1);
        assertTrue(statusDropdown.getOptions().size() > 1);
        
        businessLineDropdown.selectByIndex(1);
        modelTypeDropdown.selectByIndex(1);
        riskRatingDropdown.selectByIndex(1);
        statusDropdown.selectByIndex(1);
        
        WebElement submitButton = driver.findElement(By.cssSelector("button[type='submit']"));
        submitButton.click();
        
        WebElement successMessage = wait.until(driver -> 
            driver.findElement(By.className("alert-success")));
        
        assertTrue(successMessage.getText().contains("successfully registered"));
        
        WebElement inventoryLink = driver.findElement(By.linkText("Model Inventory"));
        inventoryLink.click();
        
        wait.until(driver -> driver.getCurrentUrl().contains("/inventory"));
        
        WebElement table = wait.until(driver -> 
            driver.findElement(By.tagName("table")));
        
        List<WebElement> rows = table.findElements(By.tagName("tr"));
        assertTrue(rows.size() > 1);
        
        boolean foundE2EModel = rows.stream().anyMatch(row -> 
            row.getText().contains("End-to-End Test Model"));
        
        assertTrue(foundE2EModel);
    }
    
    @Test
    void testFormValidation() {
        driver.get(getFrontendUrl());
        
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(20));
        
        WebElement submitButton = wait.until(driver -> {
            try {
                WebElement element = driver.findElement(By.cssSelector("button[type='submit']"));
                return element.isDisplayed() ? element : null;
            } catch (Exception e) {
                return null;
            }
        });
        
        submitButton.click();
        
        wait.until(driver -> {
            List<WebElement> errors = driver.findElements(By.className("text-danger"));
            return !errors.isEmpty() || 
                   !driver.findElements(By.className("invalid-feedback")).isEmpty() ||
                   !driver.findElements(By.className("error")).isEmpty();
        });
        
        List<WebElement> errorMessages = driver.findElements(By.className("text-danger"));
        List<WebElement> invalidFeedback = driver.findElements(By.className("invalid-feedback"));
        List<WebElement> errorElements = driver.findElements(By.className("error"));
        
        assertTrue(errorMessages.size() > 0 || invalidFeedback.size() > 0 || errorElements.size() > 0, 
                  "Expected validation errors to be displayed");
    }
    
    @Test
    void testDropdownDataFromDatabase() {
        driver.get(getFrontendUrl());
        
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(15));
        
        WebElement businessLineSelect = wait.until(driver -> 
            driver.findElement(By.id("businessLine")));
        WebElement modelTypeSelect = driver.findElement(By.id("modelType"));
        WebElement riskRatingSelect = driver.findElement(By.id("riskRating"));
        WebElement statusSelect = driver.findElement(By.id("status"));
        
        Select businessLineDropdown = new Select(businessLineSelect);
        Select modelTypeDropdown = new Select(modelTypeSelect);
        Select riskRatingDropdown = new Select(riskRatingSelect);
        Select statusDropdown = new Select(statusSelect);
        
        List<WebElement> businessLineOptions = businessLineDropdown.getOptions();
        List<WebElement> modelTypeOptions = modelTypeDropdown.getOptions();
        List<WebElement> riskRatingOptions = riskRatingDropdown.getOptions();
        List<WebElement> statusOptions = statusDropdown.getOptions();
        
        assertTrue(businessLineOptions.size() > 1);
        assertTrue(modelTypeOptions.size() > 1);
        assertTrue(riskRatingOptions.size() > 1);
        assertTrue(statusOptions.size() > 1);
        
        boolean hasRetailBanking = businessLineOptions.stream()
            .anyMatch(option -> option.getText().contains("Retail Banking"));
        boolean hasCreditRisk = modelTypeOptions.stream()
            .anyMatch(option -> option.getText().contains("Credit Risk"));
        boolean hasMediumRisk = riskRatingOptions.stream()
            .anyMatch(option -> option.getText().contains("Medium"));
        boolean hasInDevelopment = statusOptions.stream()
            .anyMatch(option -> option.getText().contains("In Development"));
        
        assertTrue(hasRetailBanking);
        assertTrue(hasCreditRisk);
        assertTrue(hasMediumRisk);
        assertTrue(hasInDevelopment);
    }
}

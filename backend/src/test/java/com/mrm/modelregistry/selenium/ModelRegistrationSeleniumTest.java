package com.mrm.modelregistry.selenium;

import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.time.Duration;

import static org.junit.jupiter.api.Assertions.*;

public class ModelRegistrationSeleniumTest extends BaseSeleniumTest {
    
    @Test
    void testModelRegistrationForm() {
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
        
        assertNotNull(modelNameInput);
        assertNotNull(modelVersionInput);
        assertNotNull(modelSponsorInput);
        assertNotNull(businessLineSelect);
        assertNotNull(modelTypeSelect);
        assertNotNull(riskRatingSelect);
        assertNotNull(statusSelect);
        
        Select businessLineDropdown = new Select(businessLineSelect);
        Select modelTypeDropdown = new Select(modelTypeSelect);
        Select riskRatingDropdown = new Select(riskRatingSelect);
        Select statusDropdown = new Select(statusSelect);
        
        assertTrue(businessLineDropdown.getOptions().size() > 1);
        assertTrue(modelTypeDropdown.getOptions().size() > 1);
        assertTrue(riskRatingDropdown.getOptions().size() > 1);
        assertTrue(statusDropdown.getOptions().size() > 1);
        
        modelNameInput.sendKeys("Selenium Test Model");
        modelVersionInput.sendKeys("v1.0");
        modelSponsorInput.sendKeys("Selenium Test Sponsor");
        
        businessLineDropdown.selectByIndex(1);
        modelTypeDropdown.selectByIndex(1);
        riskRatingDropdown.selectByIndex(1);
        statusDropdown.selectByIndex(1);
        
        WebElement submitButton = driver.findElement(By.cssSelector("button[type='submit']"));
        submitButton.click();
        
        WebElement successMessage = wait.until(driver -> 
            driver.findElement(By.className("alert-success")));
        
        assertTrue(successMessage.getText().contains("successfully registered"));
    }
    
    @Test
    void testBackendApiEndpoints() {
        driver.get(getBaseUrl() + "/api/models/enums");
        
        String pageSource = driver.getPageSource();
        assertTrue(pageSource.contains("businessLines"));
        assertTrue(pageSource.contains("modelTypes"));
        assertTrue(pageSource.contains("riskRatings"));
        assertTrue(pageSource.contains("statuses"));
    }
    
    @Test
    void testSwaggerDocumentation() {
        driver.get(getBaseUrl() + "/swagger-ui.html");
        
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(20));
        WebElement swaggerTitle = wait.until(driver -> {
            try {
                WebElement element = driver.findElement(By.className("title"));
                return element.isDisplayed() ? element : null;
            } catch (Exception e) {
                try {
                    return driver.findElement(By.tagName("h2"));
                } catch (Exception ex) {
                    try {
                        return driver.findElement(By.className("swagger-ui"));
                    } catch (Exception exc) {
                        return null;
                    }
                }
            }
        });
        
        assertNotNull(swaggerTitle);
    }
}

package com.mrm.modelregistry.selenium;

import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.time.Duration;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class ModelInventorySeleniumTest extends BaseSeleniumTest {
    
    @Test
    void testModelInventoryPageLoads() {
        driver.get(getFrontendUrl() + "/inventory");
        
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(20));
        WebElement inventoryTitle = wait.until(driver -> {
            try {
                WebElement element = driver.findElement(By.tagName("h2"));
                return element.isDisplayed() ? element : null;
            } catch (Exception e) {
                return null;
            }
        });
        
        assertTrue(inventoryTitle.getText().contains("Model Inventory"));
    }
    
    @Test
    void testInventoryTableStructure() {
        driver.get(getFrontendUrl() + "/inventory");
        
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(20));
        WebElement table = wait.until(driver -> {
            try {
                WebElement element = driver.findElement(By.tagName("table"));
                return element.isDisplayed() ? element : null;
            } catch (Exception e) {
                return null;
            }
        });
        
        assertNotNull(table);
        
        List<WebElement> headers = table.findElements(By.tagName("th"));
        assertTrue(headers.size() >= 3, "Expected at least 3 table headers, but found: " + headers.size());
        
        boolean hasIdColumn = headers.stream().anyMatch(h -> h.getText().contains("ID") || h.getText().contains("Id"));
        boolean hasNameColumn = headers.stream().anyMatch(h -> h.getText().contains("Name") || h.getText().contains("Model"));
        boolean hasVersionColumn = headers.stream().anyMatch(h -> h.getText().contains("Version"));
        
        assertTrue(hasIdColumn || hasNameColumn, "Expected to find ID or Name column");
    }
    
    @Test
    void testNavigationBetweenPages() {
        driver.get(getFrontendUrl());
        
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(20));
        
        WebElement inventoryLink = wait.until(driver -> {
            try {
                WebElement element = driver.findElement(By.linkText("Model Inventory"));
                return element.isDisplayed() ? element : null;
            } catch (Exception e) {
                try {
                    return driver.findElement(By.partialLinkText("Inventory"));
                } catch (Exception ex) {
                    return null;
                }
            }
        });
        
        inventoryLink.click();
        
        wait.until(driver -> driver.getCurrentUrl().contains("/inventory"));
        assertTrue(driver.getCurrentUrl().contains("/inventory"));
        
        WebElement registrationLink = wait.until(driver -> {
            try {
                WebElement element = driver.findElement(By.linkText("Register Model"));
                return element.isDisplayed() ? element : null;
            } catch (Exception e) {
                try {
                    return driver.findElement(By.partialLinkText("Register"));
                } catch (Exception ex) {
                    return null;
                }
            }
        });
        
        registrationLink.click();
        
        wait.until(driver -> !driver.getCurrentUrl().contains("/inventory"));
        assertFalse(driver.getCurrentUrl().contains("/inventory"));
    }
    
    @Test
    void testInventoryDisplaysRegisteredModels() {
        driver.get(getFrontendUrl() + "/inventory");
        
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(20));
        
        WebElement table = wait.until(driver -> {
            try {
                WebElement element = driver.findElement(By.tagName("table"));
                return element.isDisplayed() ? element : null;
            } catch (Exception e) {
                return null;
            }
        });
        
        List<WebElement> rows = table.findElements(By.tagName("tr"));
        
        assertTrue(rows.size() > 1, "Expected table to have more than just header row");
        
        boolean foundTestModel = rows.stream().anyMatch(row -> 
            row.getText().contains("Test Model") || row.getText().contains("Selenium"));
        
        assertTrue(foundTestModel, "Expected to find at least one test model in the inventory");
    }
}

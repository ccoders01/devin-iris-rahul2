package com.mrm.modelregistry.controller;

import com.mrm.modelregistry.service.DataGenerationService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/load-test")
@CrossOrigin(origins = "*")
@Tag(name = "Load Testing", description = "APIs for Load Testing Data Generation")
@Slf4j
public class LoadTestController {
    
    @Autowired
    private DataGenerationService dataGenerationService;
    
    @Autowired
    private JdbcTemplate jdbcTemplate;
    
    @PostMapping("/generate-million")
    @Operation(summary = "Generate 1 million test records", description = "Generate 1 million model records for load testing")
    @ApiResponse(responseCode = "200", description = "Successfully generated 1 million records")
    public ResponseEntity<Map<String, Object>> generateMillionRecords() {
        log.info("POST /api/load-test/generate-million - Starting generation of 1 million records");
        
        try {
            long startTime = System.currentTimeMillis();
            dataGenerationService.generateMillionRecords();
            long endTime = System.currentTimeMillis();
            
            Long finalCount = jdbcTemplate.queryForObject("SELECT COUNT(*) FROM models", Long.class);
            
            Map<String, Object> response = Map.of(
                "success", true,
                "message", "Successfully generated 1 million records",
                "recordCount", finalCount,
                "generationTimeMs", endTime - startTime,
                "generationTimeMinutes", (endTime - startTime) / 60000.0
            );
            
            log.info("POST /api/load-test/generate-million - Successfully completed in {} ms", endTime - startTime);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            log.error("POST /api/load-test/generate-million - Error generating records: {}", e.getMessage(), e);
            Map<String, Object> response = Map.of(
                "success", false,
                "message", "Failed to generate records: " + e.getMessage()
            );
            return ResponseEntity.status(500).body(response);
        }
    }
    
    @PostMapping("/generate-sample/{count}")
    @Operation(summary = "Generate sample test records", description = "Generate a specified number of sample records for testing")
    @ApiResponse(responseCode = "200", description = "Successfully generated sample records")
    public ResponseEntity<Map<String, Object>> generateSampleRecords(@PathVariable int count) {
        log.info("POST /api/load-test/generate-sample/{} - Starting generation of {} sample records", count, count);
        
        try {
            long startTime = System.currentTimeMillis();
            dataGenerationService.generateSampleData(count);
            long endTime = System.currentTimeMillis();
            
            Long finalCount = jdbcTemplate.queryForObject("SELECT COUNT(*) FROM models", Long.class);
            
            Map<String, Object> response = Map.of(
                "success", true,
                "message", "Successfully generated " + count + " sample records",
                "recordCount", finalCount,
                "generationTimeMs", endTime - startTime
            );
            
            log.info("POST /api/load-test/generate-sample/{} - Successfully completed in {} ms", count, endTime - startTime);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            log.error("POST /api/load-test/generate-sample/{} - Error generating records: {}", count, e.getMessage(), e);
            Map<String, Object> response = Map.of(
                "success", false,
                "message", "Failed to generate records: " + e.getMessage()
            );
            return ResponseEntity.status(500).body(response);
        }
    }
    
    @GetMapping("/database-stats")
    @Operation(summary = "Get database statistics", description = "Get current database record counts and statistics")
    @ApiResponse(responseCode = "200", description = "Successfully retrieved database statistics")
    public ResponseEntity<Map<String, Object>> getDatabaseStats() {
        log.info("GET /api/load-test/database-stats - Retrieving database statistics");
        
        try {
            Long modelCount = jdbcTemplate.queryForObject("SELECT COUNT(*) FROM models", Long.class);
            Long businessLineCount = jdbcTemplate.queryForObject("SELECT COUNT(*) FROM business_lines", Long.class);
            Long modelTypeCount = jdbcTemplate.queryForObject("SELECT COUNT(*) FROM model_types", Long.class);
            Long riskRatingCount = jdbcTemplate.queryForObject("SELECT COUNT(*) FROM risk_ratings", Long.class);
            Long statusCount = jdbcTemplate.queryForObject("SELECT COUNT(*) FROM statuses", Long.class);
            
            Map<String, Object> response = Map.of(
                "modelCount", modelCount,
                "businessLineCount", businessLineCount,
                "modelTypeCount", modelTypeCount,
                "riskRatingCount", riskRatingCount,
                "statusCount", statusCount,
                "totalLookupRecords", businessLineCount + modelTypeCount + riskRatingCount + statusCount
            );
            
            log.info("GET /api/load-test/database-stats - Retrieved stats: {} models, {} lookup records", 
                    modelCount, businessLineCount + modelTypeCount + riskRatingCount + statusCount);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            log.error("GET /api/load-test/database-stats - Error retrieving stats: {}", e.getMessage(), e);
            Map<String, Object> response = Map.of(
                "success", false,
                "message", "Failed to retrieve database statistics: " + e.getMessage()
            );
            return ResponseEntity.status(500).body(response);
        }
    }
    
    @DeleteMapping("/clear-data")
    @Operation(summary = "Clear all model data", description = "Clear all model records from the database")
    @ApiResponse(responseCode = "200", description = "Successfully cleared all model data")
    public ResponseEntity<Map<String, Object>> clearData() {
        log.info("DELETE /api/load-test/clear-data - Clearing all model data");
        
        try {
            jdbcTemplate.update("DELETE FROM models");
            jdbcTemplate.update("ALTER TABLE models AUTO_INCREMENT = 1");
            
            Long finalCount = jdbcTemplate.queryForObject("SELECT COUNT(*) FROM models", Long.class);
            
            Map<String, Object> response = Map.of(
                "success", true,
                "message", "Successfully cleared all model data",
                "remainingRecords", finalCount
            );
            
            log.info("DELETE /api/load-test/clear-data - Successfully cleared data, remaining records: {}", finalCount);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            log.error("DELETE /api/load-test/clear-data - Error clearing data: {}", e.getMessage(), e);
            Map<String, Object> response = Map.of(
                "success", false,
                "message", "Failed to clear data: " + e.getMessage()
            );
            return ResponseEntity.status(500).body(response);
        }
    }
}

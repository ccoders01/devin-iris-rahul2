package com.mrm.modelregistry.service;

import com.mrm.modelregistry.entity.*;
import com.mrm.modelregistry.repository.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Random;

@Service
@Slf4j
public class DataGenerationService {
    
    @Autowired
    private JdbcTemplate jdbcTemplate;
    
    @Autowired
    private BusinessLineRepository businessLineRepository;
    
    @Autowired
    private ModelTypeRepository modelTypeRepository;
    
    @Autowired
    private RiskRatingRepository riskRatingRepository;
    
    @Autowired
    private StatusRepository statusRepository;
    
    private static final String[] MODEL_PREFIXES = {
        "Credit", "Market", "Operational", "Liquidity", "Interest", "Currency", 
        "Equity", "Bond", "Derivative", "Portfolio", "Risk", "Compliance",
        "Regulatory", "Capital", "Stress", "Scenario", "Monte", "VaR",
        "Expected", "Probability", "Default", "Loss", "Recovery", "Exposure"
    };
    
    private static final String[] MODEL_SUFFIXES = {
        "Model", "Engine", "Calculator", "Predictor", "Analyzer", "Estimator",
        "Simulator", "Optimizer", "Validator", "Monitor", "Tracker", "Framework",
        "System", "Platform", "Tool", "Algorithm", "Methodology", "Approach"
    };
    
    private static final String[] SPONSOR_DEPARTMENTS = {
        "Risk Management", "Quantitative Analytics", "Model Validation", 
        "Credit Risk", "Market Risk", "Operational Risk", "Treasury",
        "Investment Banking", "Retail Banking", "Commercial Banking",
        "Wealth Management", "Asset Management", "Compliance", "Audit"
    };
    
    private static final String[] SPONSOR_NAMES = {
        "John Smith", "Sarah Johnson", "Michael Brown", "Emily Davis", "David Wilson",
        "Jessica Miller", "Christopher Moore", "Amanda Taylor", "Matthew Anderson", "Ashley Thomas",
        "Joshua Jackson", "Stephanie White", "Andrew Harris", "Melissa Martin", "Daniel Thompson",
        "Nicole Garcia", "Ryan Martinez", "Lauren Robinson", "Kevin Clark", "Rachel Rodriguez"
    };
    
    @Transactional
    public void generateMillionRecords() {
        log.info("Starting generation of 1 million model records...");
        
        List<BusinessLineEntity> businessLines = businessLineRepository.findAll();
        List<ModelTypeEntity> modelTypes = modelTypeRepository.findAll();
        List<RiskRatingEntity> riskRatings = riskRatingRepository.findAll();
        List<StatusEntity> statuses = statusRepository.findAll();
        
        log.info("Found {} business lines, {} model types, {} risk ratings, {} statuses", 
                businessLines.size(), modelTypes.size(), riskRatings.size(), statuses.size());
        
        log.info("Clearing existing model data...");
        jdbcTemplate.update("DELETE FROM models");
        jdbcTemplate.update("ALTER TABLE models AUTO_INCREMENT = 1");
        
        int batchSize = 10000;
        int totalRecords = 1000000;
        int batches = totalRecords / batchSize;
        
        Random random = new Random();
        LocalDateTime baseTime = LocalDateTime.now().minusYears(2);
        
        for (int batch = 0; batch < batches; batch++) {
            log.info("Processing batch {} of {} ({} records)", batch + 1, batches, (batch + 1) * batchSize);
            
            StringBuilder sql = new StringBuilder();
            sql.append("INSERT INTO models (model_name, model_version, model_sponsor, business_line_id, model_type_id, risk_rating_id, status_id, created_at, updated_at) VALUES ");
            
            for (int i = 0; i < batchSize; i++) {
                if (i > 0) sql.append(", ");
                
                String modelName = generateModelName(random);
                String modelVersion = generateVersion(random);
                String modelSponsor = generateSponsor(random);
                
                BusinessLineEntity businessLine = businessLines.get(random.nextInt(businessLines.size()));
                ModelTypeEntity modelType = modelTypes.get(random.nextInt(modelTypes.size()));
                RiskRatingEntity riskRating = riskRatings.get(random.nextInt(riskRatings.size()));
                StatusEntity status = statuses.get(random.nextInt(statuses.size()));
                
                LocalDateTime createdAt = baseTime.plusDays(random.nextInt(730)).plusHours(random.nextInt(24)).plusMinutes(random.nextInt(60));
                LocalDateTime updatedAt = createdAt.plusDays(random.nextInt(30)).plusHours(random.nextInt(24));
                
                sql.append(String.format("('%s', '%s', '%s', %d, %d, %d, %d, '%s', '%s')",
                    escapeString(modelName),
                    escapeString(modelVersion),
                    escapeString(modelSponsor),
                    businessLine.getId(),
                    modelType.getId(),
                    riskRating.getId(),
                    status.getId(),
                    createdAt.toString(),
                    updatedAt.toString()
                ));
            }
            
            jdbcTemplate.update(sql.toString());
            
            if ((batch + 1) % 10 == 0) {
                log.info("Completed {} batches ({} records)", batch + 1, (batch + 1) * batchSize);
            }
        }
        
        log.info("Successfully generated 1 million model records!");
        
        Long count = jdbcTemplate.queryForObject("SELECT COUNT(*) FROM models", Long.class);
        log.info("Final record count: {}", count);
    }
    
    private String generateModelName(Random random) {
        String prefix = MODEL_PREFIXES[random.nextInt(MODEL_PREFIXES.length)];
        String suffix = MODEL_SUFFIXES[random.nextInt(MODEL_SUFFIXES.length)];
        int number = random.nextInt(9999) + 1;
        return prefix + " " + suffix + " " + number;
    }
    
    private String generateVersion(Random random) {
        int major = random.nextInt(5) + 1;
        int minor = random.nextInt(10);
        int patch = random.nextInt(20);
        return "v" + major + "." + minor + "." + patch;
    }
    
    private String generateSponsor(Random random) {
        if (random.nextBoolean()) {
            return SPONSOR_NAMES[random.nextInt(SPONSOR_NAMES.length)];
        } else {
            return SPONSOR_DEPARTMENTS[random.nextInt(SPONSOR_DEPARTMENTS.length)];
        }
    }
    
    private String escapeString(String str) {
        return str.replace("'", "''");
    }
    
    public void generateSampleData(int recordCount) {
        log.info("Generating {} sample records for testing...", recordCount);
        
        List<BusinessLineEntity> businessLines = businessLineRepository.findAll();
        List<ModelTypeEntity> modelTypes = modelTypeRepository.findAll();
        List<RiskRatingEntity> riskRatings = riskRatingRepository.findAll();
        List<StatusEntity> statuses = statusRepository.findAll();
        
        Random random = new Random();
        LocalDateTime baseTime = LocalDateTime.now().minusMonths(6);
        
        StringBuilder sql = new StringBuilder();
        sql.append("INSERT INTO models (model_name, model_version, model_sponsor, business_line_id, model_type_id, risk_rating_id, status_id, created_at, updated_at) VALUES ");
        
        for (int i = 0; i < recordCount; i++) {
            if (i > 0) sql.append(", ");
            
            String modelName = generateModelName(random);
            String modelVersion = generateVersion(random);
            String modelSponsor = generateSponsor(random);
            
            BusinessLineEntity businessLine = businessLines.get(random.nextInt(businessLines.size()));
            ModelTypeEntity modelType = modelTypes.get(random.nextInt(modelTypes.size()));
            RiskRatingEntity riskRating = riskRatings.get(random.nextInt(riskRatings.size()));
            StatusEntity status = statuses.get(random.nextInt(statuses.size()));
            
            LocalDateTime createdAt = baseTime.plusDays(random.nextInt(180)).plusHours(random.nextInt(24));
            LocalDateTime updatedAt = createdAt.plusDays(random.nextInt(30));
            
            sql.append(String.format("('%s', '%s', '%s', %d, %d, %d, %d, '%s', '%s')",
                escapeString(modelName),
                escapeString(modelVersion),
                escapeString(modelSponsor),
                businessLine.getId(),
                modelType.getId(),
                riskRating.getId(),
                status.getId(),
                createdAt.toString(),
                updatedAt.toString()
            ));
        }
        
        jdbcTemplate.update(sql.toString());
        log.info("Successfully generated {} sample records", recordCount);
    }
}

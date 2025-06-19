package com.mrm.modelregistry.service;

import com.mrm.modelregistry.entity.*;
import com.mrm.modelregistry.repository.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import jakarta.annotation.PostConstruct;

@Service
public class DataInitializationService {
    
    @Autowired
    private BusinessLineRepository businessLineRepository;
    
    @Autowired
    private ModelTypeRepository modelTypeRepository;
    
    @Autowired
    private RiskRatingRepository riskRatingRepository;
    
    @Autowired
    private StatusRepository statusRepository;
    
    @PostConstruct
    public void initializeData() {
        initializeBusinessLines();
        initializeModelTypes();
        initializeRiskRatings();
        initializeStatuses();
    }
    
    private void initializeBusinessLines() {
        if (businessLineRepository.count() == 0) {
            businessLineRepository.save(new BusinessLineEntity("RETAIL_BANKING", "Retail Banking"));
            businessLineRepository.save(new BusinessLineEntity("WHOLESALE_LENDING", "Wholesale Lending"));
            businessLineRepository.save(new BusinessLineEntity("INVESTMENT_BANKING", "Investment Banking"));
            businessLineRepository.save(new BusinessLineEntity("RISK_MANAGEMENT", "Risk Management"));
        }
    }
    
    private void initializeModelTypes() {
        if (modelTypeRepository.count() == 0) {
            modelTypeRepository.save(new ModelTypeEntity("CREDIT_RISK", "Credit Risk"));
            modelTypeRepository.save(new ModelTypeEntity("MARKET_RISK", "Market Risk"));
            modelTypeRepository.save(new ModelTypeEntity("OPERATIONAL_RISK", "Operational Risk"));
            modelTypeRepository.save(new ModelTypeEntity("AML", "AML"));
            modelTypeRepository.save(new ModelTypeEntity("CAPITAL_CALCULATION", "Capital Calculation"));
            modelTypeRepository.save(new ModelTypeEntity("VALUATION", "Valuation"));
        }
    }
    
    private void initializeRiskRatings() {
        if (riskRatingRepository.count() == 0) {
            riskRatingRepository.save(new RiskRatingEntity("HIGH", "High"));
            riskRatingRepository.save(new RiskRatingEntity("MEDIUM", "Medium"));
            riskRatingRepository.save(new RiskRatingEntity("LOW", "Low"));
        }
    }
    
    private void initializeStatuses() {
        if (statusRepository.count() == 0) {
            statusRepository.save(new StatusEntity("IN_DEVELOPMENT", "In Development"));
            statusRepository.save(new StatusEntity("VALIDATED", "Validated"));
            statusRepository.save(new StatusEntity("PRODUCTION", "Production"));
            statusRepository.save(new StatusEntity("RETIRED", "Retired"));
        }
    }
}

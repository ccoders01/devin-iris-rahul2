package com.mrm.modelregistry.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.time.LocalDateTime;

@Entity
@Table(name = "models")
public class Model {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotBlank(message = "Model name is required")
    @Column(nullable = false)
    private String modelName;
    
    @NotBlank(message = "Model version is required")
    @Column(nullable = false)
    private String modelVersion;
    
    @NotBlank(message = "Model sponsor is required")
    @Column(nullable = false)
    private String modelSponsor;
    
    @NotNull(message = "Business line is required")
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private BusinessLine businessLine;
    
    @NotNull(message = "Model type is required")
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private ModelType modelType;
    
    @NotNull(message = "Risk rating is required")
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private RiskRating riskRating;
    
    @NotNull(message = "Status is required")
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Status status;
    
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @Column(nullable = false)
    private LocalDateTime updatedAt;
    
    public enum BusinessLine {
        RETAIL_BANKING("Retail Banking"),
        WHOLESALE_LENDING("Wholesale Lending"),
        INVESTMENT_BANKING("Investment Banking"),
        RISK_MANAGEMENT("Risk Management");
        
        private final String displayName;
        
        BusinessLine(String displayName) {
            this.displayName = displayName;
        }
        
        public String getDisplayName() {
            return displayName;
        }
    }
    
    public enum ModelType {
        CREDIT_RISK("Credit Risk"),
        MARKET_RISK("Market Risk"),
        OPERATIONAL_RISK("Operational Risk"),
        AML("AML"),
        CAPITAL_CALCULATION("Capital Calculation"),
        VALUATION("Valuation");
        
        private final String displayName;
        
        ModelType(String displayName) {
            this.displayName = displayName;
        }
        
        public String getDisplayName() {
            return displayName;
        }
    }
    
    public enum RiskRating {
        HIGH("High"),
        MEDIUM("Medium"),
        LOW("Low");
        
        private final String displayName;
        
        RiskRating(String displayName) {
            this.displayName = displayName;
        }
        
        public String getDisplayName() {
            return displayName;
        }
    }
    
    public enum Status {
        IN_DEVELOPMENT("In Development"),
        VALIDATED("Validated"),
        PRODUCTION("Production"),
        RETIRED("Retired");
        
        private final String displayName;
        
        Status(String displayName) {
            this.displayName = displayName;
        }
        
        public String getDisplayName() {
            return displayName;
        }
    }
    
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }
    
    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
    
    public Model() {}
    
    public Model(String modelName, String modelVersion, String modelSponsor, 
                BusinessLine businessLine, ModelType modelType, RiskRating riskRating, Status status) {
        this.modelName = modelName;
        this.modelVersion = modelVersion;
        this.modelSponsor = modelSponsor;
        this.businessLine = businessLine;
        this.modelType = modelType;
        this.riskRating = riskRating;
        this.status = status;
    }
    
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public String getModelName() {
        return modelName;
    }
    
    public void setModelName(String modelName) {
        this.modelName = modelName;
    }
    
    public String getModelVersion() {
        return modelVersion;
    }
    
    public void setModelVersion(String modelVersion) {
        this.modelVersion = modelVersion;
    }
    
    public String getModelSponsor() {
        return modelSponsor;
    }
    
    public void setModelSponsor(String modelSponsor) {
        this.modelSponsor = modelSponsor;
    }
    
    public BusinessLine getBusinessLine() {
        return businessLine;
    }
    
    public void setBusinessLine(BusinessLine businessLine) {
        this.businessLine = businessLine;
    }
    
    public ModelType getModelType() {
        return modelType;
    }
    
    public void setModelType(ModelType modelType) {
        this.modelType = modelType;
    }
    
    public RiskRating getRiskRating() {
        return riskRating;
    }
    
    public void setRiskRating(RiskRating riskRating) {
        this.riskRating = riskRating;
    }
    
    public Status getStatus() {
        return status;
    }
    
    public void setStatus(Status status) {
        this.status = status;
    }
    
    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
    
    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
    
    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }
    
    public void setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
    }
}

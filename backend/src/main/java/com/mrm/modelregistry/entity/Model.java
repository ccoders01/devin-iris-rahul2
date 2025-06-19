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
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "business_line_id", nullable = false)
    private BusinessLineEntity businessLine;
    
    @NotNull(message = "Model type is required")
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "model_type_id", nullable = false)
    private ModelTypeEntity modelType;
    
    @NotNull(message = "Risk rating is required")
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "risk_rating_id", nullable = false)
    private RiskRatingEntity riskRating;
    
    @NotNull(message = "Status is required")
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "status_id", nullable = false)
    private StatusEntity status;
    
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @Column(nullable = false)
    private LocalDateTime updatedAt;
    

    
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
                BusinessLineEntity businessLine, ModelTypeEntity modelType, RiskRatingEntity riskRating, StatusEntity status) {
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
    
    public BusinessLineEntity getBusinessLine() {
        return businessLine;
    }
    
    public void setBusinessLine(BusinessLineEntity businessLine) {
        this.businessLine = businessLine;
    }
    
    public ModelTypeEntity getModelType() {
        return modelType;
    }
    
    public void setModelType(ModelTypeEntity modelType) {
        this.modelType = modelType;
    }
    
    public RiskRatingEntity getRiskRating() {
        return riskRating;
    }
    
    public void setRiskRating(RiskRatingEntity riskRating) {
        this.riskRating = riskRating;
    }
    
    public StatusEntity getStatus() {
        return status;
    }
    
    public void setStatus(StatusEntity status) {
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

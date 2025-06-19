package com.mrm.modelregistry.dto;

import com.mrm.modelregistry.entity.Model;
import java.time.LocalDateTime;

public class ModelResponse {
    
    private Long id;
    private String modelName;
    private String modelVersion;
    private String modelSponsor;
    private Model.BusinessLine businessLine;
    private Model.ModelType modelType;
    private Model.RiskRating riskRating;
    private Model.Status status;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    
    public ModelResponse() {}
    
    public ModelResponse(Model model) {
        this.id = model.getId();
        this.modelName = model.getModelName();
        this.modelVersion = model.getModelVersion();
        this.modelSponsor = model.getModelSponsor();
        this.businessLine = model.getBusinessLine();
        this.modelType = model.getModelType();
        this.riskRating = model.getRiskRating();
        this.status = model.getStatus();
        this.createdAt = model.getCreatedAt();
        this.updatedAt = model.getUpdatedAt();
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
    
    public Model.BusinessLine getBusinessLine() {
        return businessLine;
    }
    
    public void setBusinessLine(Model.BusinessLine businessLine) {
        this.businessLine = businessLine;
    }
    
    public Model.ModelType getModelType() {
        return modelType;
    }
    
    public void setModelType(Model.ModelType modelType) {
        this.modelType = modelType;
    }
    
    public Model.RiskRating getRiskRating() {
        return riskRating;
    }
    
    public void setRiskRating(Model.RiskRating riskRating) {
        this.riskRating = riskRating;
    }
    
    public Model.Status getStatus() {
        return status;
    }
    
    public void setStatus(Model.Status status) {
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

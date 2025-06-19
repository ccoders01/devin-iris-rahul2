package com.mrm.modelregistry.dto;

import com.mrm.modelregistry.entity.Model;
import java.time.LocalDateTime;

public class ModelResponse {
    
    private Long id;
    private String modelName;
    private String modelVersion;
    private String modelSponsor;
    private String businessLine;
    private String businessLineDisplayName;
    private String modelType;
    private String modelTypeDisplayName;
    private String riskRating;
    private String riskRatingDisplayName;
    private String status;
    private String statusDisplayName;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    
    public ModelResponse() {}
    
    public ModelResponse(Model model) {
        this.id = model.getId();
        this.modelName = model.getModelName();
        this.modelVersion = model.getModelVersion();
        this.modelSponsor = model.getModelSponsor();
        this.businessLine = model.getBusinessLine().getCode();
        this.businessLineDisplayName = model.getBusinessLine().getDisplayName();
        this.modelType = model.getModelType().getCode();
        this.modelTypeDisplayName = model.getModelType().getDisplayName();
        this.riskRating = model.getRiskRating().getCode();
        this.riskRatingDisplayName = model.getRiskRating().getDisplayName();
        this.status = model.getStatus().getCode();
        this.statusDisplayName = model.getStatus().getDisplayName();
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
    
    public String getBusinessLine() {
        return businessLine;
    }
    
    public void setBusinessLine(String businessLine) {
        this.businessLine = businessLine;
    }
    
    public String getBusinessLineDisplayName() {
        return businessLineDisplayName;
    }
    
    public void setBusinessLineDisplayName(String businessLineDisplayName) {
        this.businessLineDisplayName = businessLineDisplayName;
    }
    
    public String getModelType() {
        return modelType;
    }
    
    public void setModelType(String modelType) {
        this.modelType = modelType;
    }
    
    public String getModelTypeDisplayName() {
        return modelTypeDisplayName;
    }
    
    public void setModelTypeDisplayName(String modelTypeDisplayName) {
        this.modelTypeDisplayName = modelTypeDisplayName;
    }
    
    public String getRiskRating() {
        return riskRating;
    }
    
    public void setRiskRating(String riskRating) {
        this.riskRating = riskRating;
    }
    
    public String getRiskRatingDisplayName() {
        return riskRatingDisplayName;
    }
    
    public void setRiskRatingDisplayName(String riskRatingDisplayName) {
        this.riskRatingDisplayName = riskRatingDisplayName;
    }
    
    public String getStatus() {
        return status;
    }
    
    public void setStatus(String status) {
        this.status = status;
    }
    
    public String getStatusDisplayName() {
        return statusDisplayName;
    }
    
    public void setStatusDisplayName(String statusDisplayName) {
        this.statusDisplayName = statusDisplayName;
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

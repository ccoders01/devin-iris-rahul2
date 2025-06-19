package com.mrm.modelregistry.dto;

import com.mrm.modelregistry.entity.Model;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public class ModelRequest {
    
    @NotBlank(message = "Model name is required")
    private String modelName;
    
    @NotBlank(message = "Model version is required")
    private String modelVersion;
    
    @NotBlank(message = "Model sponsor is required")
    private String modelSponsor;
    
    @NotBlank(message = "Business line is required")
    private String businessLine;
    
    @NotBlank(message = "Model type is required")
    private String modelType;
    
    @NotBlank(message = "Risk rating is required")
    private String riskRating;
    
    @NotBlank(message = "Status is required")
    private String status;
    
    public ModelRequest() {}
    
    public ModelRequest(String modelName, String modelVersion, String modelSponsor,
                       String businessLine, String modelType,
                       String riskRating, String status) {
        this.modelName = modelName;
        this.modelVersion = modelVersion;
        this.modelSponsor = modelSponsor;
        this.businessLine = businessLine;
        this.modelType = modelType;
        this.riskRating = riskRating;
        this.status = status;
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
    
    public String getModelType() {
        return modelType;
    }
    
    public void setModelType(String modelType) {
        this.modelType = modelType;
    }
    
    public String getRiskRating() {
        return riskRating;
    }
    
    public void setRiskRating(String riskRating) {
        this.riskRating = riskRating;
    }
    
    public String getStatus() {
        return status;
    }
    
    public void setStatus(String status) {
        this.status = status;
    }
}

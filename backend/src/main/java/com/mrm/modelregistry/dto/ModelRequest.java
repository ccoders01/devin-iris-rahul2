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
    
    @NotNull(message = "Business line is required")
    private Model.BusinessLine businessLine;
    
    @NotNull(message = "Model type is required")
    private Model.ModelType modelType;
    
    @NotNull(message = "Risk rating is required")
    private Model.RiskRating riskRating;
    
    @NotNull(message = "Status is required")
    private Model.Status status;
    
    public ModelRequest() {}
    
    public ModelRequest(String modelName, String modelVersion, String modelSponsor,
                       Model.BusinessLine businessLine, Model.ModelType modelType,
                       Model.RiskRating riskRating, Model.Status status) {
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
}

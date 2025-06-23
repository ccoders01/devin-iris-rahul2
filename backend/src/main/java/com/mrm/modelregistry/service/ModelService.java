package com.mrm.modelregistry.service;

import com.mrm.modelregistry.dto.ModelRequest;
import com.mrm.modelregistry.dto.ModelResponse;
import com.mrm.modelregistry.entity.*;
import com.mrm.modelregistry.repository.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
@Slf4j
public class ModelService {
    
    @Autowired
    private ModelRepository modelRepository;
    
    @Autowired
    private BusinessLineRepository businessLineRepository;
    
    @Autowired
    private ModelTypeRepository modelTypeRepository;
    
    @Autowired
    private RiskRatingRepository riskRatingRepository;
    
    @Autowired
    private StatusRepository statusRepository;
    
    public ModelResponse registerModel(ModelRequest request) {
        log.info("Registering model: {} version: {}", request.getModelName(), request.getModelVersion());
        
        BusinessLineEntity businessLine = businessLineRepository.findByCode(request.getBusinessLine())
            .orElseThrow(() -> new RuntimeException("Business line not found: " + request.getBusinessLine()));
        
        ModelTypeEntity modelType = modelTypeRepository.findByCode(request.getModelType())
            .orElseThrow(() -> new RuntimeException("Model type not found: " + request.getModelType()));
        
        RiskRatingEntity riskRating = riskRatingRepository.findByCode(request.getRiskRating())
            .orElseThrow(() -> new RuntimeException("Risk rating not found: " + request.getRiskRating()));
        
        StatusEntity status = statusRepository.findByCode(request.getStatus())
            .orElseThrow(() -> new RuntimeException("Status not found: " + request.getStatus()));
        
        Model model = new Model(
            request.getModelName(),
            request.getModelVersion(),
            request.getModelSponsor(),
            businessLine,
            modelType,
            riskRating,
            status
        );
        
        Model savedModel = modelRepository.save(model);
        log.info("Successfully registered model with ID: {}", savedModel.getId());
        return new ModelResponse(savedModel);
    }
    
    public List<ModelResponse> getAllModels() {
        log.info("Retrieving all models from database");
        List<Model> models = modelRepository.findAll();
        List<ModelResponse> modelResponses = models.stream()
                .map(ModelResponse::new)
                .collect(Collectors.toList());
        log.info("Retrieved {} models from database", modelResponses.size());
        return modelResponses;
    }
    
    public ModelResponse getModelById(Long id) {
        log.info("Retrieving model by ID: {}", id);
        Model model = modelRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Model not found with id: " + id));
        log.info("Found model: {}", model.getModelName());
        return new ModelResponse(model);
    }
    
    public ModelResponse updateModel(Long id, ModelRequest request) {
        log.info("Updating model with ID: {} to name: {}", id, request.getModelName());
        
        Model existingModel = modelRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Model not found with id: " + id));
        
        BusinessLineEntity businessLine = businessLineRepository.findByCode(request.getBusinessLine())
            .orElseThrow(() -> new RuntimeException("Business line not found: " + request.getBusinessLine()));
        
        ModelTypeEntity modelType = modelTypeRepository.findByCode(request.getModelType())
            .orElseThrow(() -> new RuntimeException("Model type not found: " + request.getModelType()));
        
        RiskRatingEntity riskRating = riskRatingRepository.findByCode(request.getRiskRating())
            .orElseThrow(() -> new RuntimeException("Risk rating not found: " + request.getRiskRating()));
        
        StatusEntity status = statusRepository.findByCode(request.getStatus())
            .orElseThrow(() -> new RuntimeException("Status not found: " + request.getStatus()));
        
        existingModel.setModelName(request.getModelName());
        existingModel.setModelVersion(request.getModelVersion());
        existingModel.setModelSponsor(request.getModelSponsor());
        existingModel.setBusinessLine(businessLine);
        existingModel.setModelType(modelType);
        existingModel.setRiskRating(riskRating);
        existingModel.setStatus(status);
        
        Model updatedModel = modelRepository.save(existingModel);
        log.info("Successfully updated model with ID: {}", updatedModel.getId());
        return new ModelResponse(updatedModel);
    }
}

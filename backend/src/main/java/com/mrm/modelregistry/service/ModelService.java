package com.mrm.modelregistry.service;

import com.mrm.modelregistry.dto.ModelRequest;
import com.mrm.modelregistry.dto.ModelResponse;
import com.mrm.modelregistry.entity.*;
import com.mrm.modelregistry.repository.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
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
        return new ModelResponse(savedModel);
    }
    
    public List<ModelResponse> getAllModels() {
        List<Model> models = modelRepository.findAll();
        return models.stream()
                .map(ModelResponse::new)
                .collect(Collectors.toList());
    }
    
    public ModelResponse getModelById(Long id) {
        Model model = modelRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Model not found with id: " + id));
        return new ModelResponse(model);
    }
}

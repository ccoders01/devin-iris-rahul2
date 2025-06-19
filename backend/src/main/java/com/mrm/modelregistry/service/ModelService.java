package com.mrm.modelregistry.service;

import com.mrm.modelregistry.dto.ModelRequest;
import com.mrm.modelregistry.dto.ModelResponse;
import com.mrm.modelregistry.entity.Model;
import com.mrm.modelregistry.repository.ModelRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class ModelService {
    
    @Autowired
    private ModelRepository modelRepository;
    
    public ModelResponse registerModel(ModelRequest request) {
        Model model = new Model(
            request.getModelName(),
            request.getModelVersion(),
            request.getModelSponsor(),
            request.getBusinessLine(),
            request.getModelType(),
            request.getRiskRating(),
            request.getStatus()
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

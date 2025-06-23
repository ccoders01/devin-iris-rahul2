package com.mrm.modelregistry.controller;

import com.mrm.modelregistry.dto.ModelRequest;
import com.mrm.modelregistry.dto.ModelResponse;
import com.mrm.modelregistry.entity.*;
import com.mrm.modelregistry.repository.*;
import com.mrm.modelregistry.service.ModelService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/models")
@CrossOrigin(origins = "*")
@Tag(name = "Model Management", description = "APIs for Model Registration and Inventory Management")
@Slf4j
public class ModelController {
    
    @Autowired
    private ModelService modelService;
    
    @Autowired
    private BusinessLineRepository businessLineRepository;
    
    @Autowired
    private ModelTypeRepository modelTypeRepository;
    
    @Autowired
    private RiskRatingRepository riskRatingRepository;
    
    @Autowired
    private StatusRepository statusRepository;
    
    @PostMapping
    @Operation(summary = "Register a new model", description = "Register a new model with all required attributes")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "201", description = "Model successfully registered"),
        @ApiResponse(responseCode = "400", description = "Invalid input data")
    })
    public ResponseEntity<ModelResponse> registerModel(@Valid @RequestBody ModelRequest request) {
        log.info("POST /api/models - Registering new model: {}", request.getModelName());
        log.debug("Registration request payload: modelName={}, modelVersion={}, modelSponsor={}, businessLine={}, modelType={}, riskRating={}, status={}", 
                 request.getModelName(), request.getModelVersion(), request.getModelSponsor(), 
                 request.getBusinessLine(), request.getModelType(), request.getRiskRating(), request.getStatus());
        try {
            ModelResponse response = modelService.registerModel(request);
            log.info("POST /api/models - Successfully registered model with ID: {}, name: {}", response.getId(), response.getModelName());
            return new ResponseEntity<>(response, HttpStatus.CREATED);
        } catch (Exception e) {
            log.error("POST /api/models - Failed to register model: {}, error: {}", request.getModelName(), e.getMessage(), e);
            throw e;
        }
    }
    
    @GetMapping
    @Operation(summary = "Get all models", description = "Retrieve all registered models for inventory display")
    @ApiResponse(responseCode = "200", description = "Successfully retrieved all models")
    public ResponseEntity<List<ModelResponse>> getAllModels() {
        log.info("GET /api/models - Retrieving all models");
        try {
            List<ModelResponse> models = modelService.getAllModels();
            log.info("GET /api/models - Successfully retrieved {} models", models.size());
            return ResponseEntity.ok(models);
        } catch (Exception e) {
            log.error("GET /api/models - Failed to retrieve models, error: {}", e.getMessage(), e);
            throw e;
        }
    }
    
    @GetMapping("/{id}")
    @Operation(summary = "Get model by ID", description = "Retrieve a specific model by its unique ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Model found"),
        @ApiResponse(responseCode = "404", description = "Model not found")
    })
    public ResponseEntity<ModelResponse> getModelById(@PathVariable Long id) {
        log.info("GET /api/models/{} - Retrieving model with ID: {}", id, id);
        try {
            ModelResponse model = modelService.getModelById(id);
            log.info("GET /api/models/{} - Successfully retrieved model: {}", id, model.getModelName());
            return ResponseEntity.ok(model);
        } catch (RuntimeException e) {
            log.warn("GET /api/models/{} - Model not found with ID: {}, error: {}", id, id, e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }
    
    @GetMapping("/enums")
    @Operation(summary = "Get enum values", description = "Get all possible values for dropdown fields")
    @ApiResponse(responseCode = "200", description = "Successfully retrieved enum values")
    public ResponseEntity<Map<String, List<Map<String, String>>>> getEnumValues() {
        log.info("GET /api/models/enums - Retrieving enum values for dropdowns");
        try {
            Map<String, List<Map<String, String>>> enums = Map.of(
                "businessLines", businessLineRepository.findAll().stream()
                    .map(bl -> Map.of("value", bl.getCode(), "displayName", bl.getDisplayName()))
                    .collect(Collectors.toList()),
                "modelTypes", modelTypeRepository.findAll().stream()
                    .map(mt -> Map.of("value", mt.getCode(), "displayName", mt.getDisplayName()))
                    .collect(Collectors.toList()),
                "riskRatings", riskRatingRepository.findAll().stream()
                    .map(rr -> Map.of("value", rr.getCode(), "displayName", rr.getDisplayName()))
                    .collect(Collectors.toList()),
                "statuses", statusRepository.findAll().stream()
                    .map(s -> Map.of("value", s.getCode(), "displayName", s.getDisplayName()))
                    .collect(Collectors.toList())
            );
            log.info("GET /api/models/enums - Successfully retrieved enum values: {} business lines, {} model types, {} risk ratings, {} statuses", 
                    enums.get("businessLines").size(), enums.get("modelTypes").size(), 
                    enums.get("riskRatings").size(), enums.get("statuses").size());
            return ResponseEntity.ok(enums);
        } catch (Exception e) {
            log.error("GET /api/models/enums - Failed to retrieve enum values, error: {}", e.getMessage(), e);
            throw e;
        }
    }
    
    @PutMapping("/{id}")
    @Operation(summary = "Update an existing model", description = "Update an existing model with new attributes")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Model successfully updated"),
        @ApiResponse(responseCode = "404", description = "Model not found"),
        @ApiResponse(responseCode = "400", description = "Invalid input data")
    })
    public ResponseEntity<ModelResponse> updateModel(@PathVariable Long id, @Valid @RequestBody ModelRequest request) {
        log.info("PUT /api/models/{} - Updating model with ID: {} to name: {}", id, id, request.getModelName());
        log.debug("Update request payload: modelName={}, modelVersion={}, modelSponsor={}, businessLine={}, modelType={}, riskRating={}, status={}", 
                 request.getModelName(), request.getModelVersion(), request.getModelSponsor(), 
                 request.getBusinessLine(), request.getModelType(), request.getRiskRating(), request.getStatus());
        try {
            ModelResponse response = modelService.updateModel(id, request);
            log.info("PUT /api/models/{} - Successfully updated model with ID: {}, new name: {}", id, response.getId(), response.getModelName());
            return ResponseEntity.ok(response);
        } catch (RuntimeException e) {
            log.error("PUT /api/models/{} - Failed to update model with ID: {}, error: {}", id, id, e.getMessage(), e);
            return ResponseEntity.badRequest().build();
        }
    }
}

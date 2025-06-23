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
        log.info("Registering new model: {}", request.getModelName());
        ModelResponse response = modelService.registerModel(request);
        log.info("Successfully registered model with ID: {}", response.getId());
        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }
    
    @GetMapping
    @Operation(summary = "Get all models", description = "Retrieve all registered models for inventory display")
    @ApiResponse(responseCode = "200", description = "Successfully retrieved all models")
    public ResponseEntity<List<ModelResponse>> getAllModels() {
        log.info("Retrieving all models");
        List<ModelResponse> models = modelService.getAllModels();
        log.info("Retrieved {} models", models.size());
        return ResponseEntity.ok(models);
    }
    
    @GetMapping("/{id}")
    @Operation(summary = "Get model by ID", description = "Retrieve a specific model by its unique ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Model found"),
        @ApiResponse(responseCode = "404", description = "Model not found")
    })
    public ResponseEntity<ModelResponse> getModelById(@PathVariable Long id) {
        log.info("Retrieving model with ID: {}", id);
        try {
            ModelResponse model = modelService.getModelById(id);
            log.info("Successfully retrieved model: {}", model.getModelName());
            return ResponseEntity.ok(model);
        } catch (RuntimeException e) {
            log.warn("Model not found with ID: {}", id);
            return ResponseEntity.notFound().build();
        }
    }
    
    @GetMapping("/enums")
    @Operation(summary = "Get enum values", description = "Get all possible values for dropdown fields")
    @ApiResponse(responseCode = "200", description = "Successfully retrieved enum values")
    public ResponseEntity<Map<String, List<Map<String, String>>>> getEnumValues() {
        log.info("Retrieving enum values for dropdowns");
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
        log.info("Successfully retrieved enum values");
        return ResponseEntity.ok(enums);
    }
    
    @PutMapping("/{id}")
    @Operation(summary = "Update an existing model", description = "Update an existing model with new attributes")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Model successfully updated"),
        @ApiResponse(responseCode = "404", description = "Model not found"),
        @ApiResponse(responseCode = "400", description = "Invalid input data")
    })
    public ResponseEntity<ModelResponse> updateModel(@PathVariable Long id, @Valid @RequestBody ModelRequest request) {
        log.info("Updating model with ID: {} to name: {}", id, request.getModelName());
        try {
            ModelResponse response = modelService.updateModel(id, request);
            log.info("Successfully updated model with ID: {}", response.getId());
            return ResponseEntity.ok(response);
        } catch (RuntimeException e) {
            log.error("Failed to update model with ID: {}, error: {}", id, e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }
}

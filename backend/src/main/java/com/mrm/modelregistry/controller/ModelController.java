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
        ModelResponse response = modelService.registerModel(request);
        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }
    
    @GetMapping
    @Operation(summary = "Get all models", description = "Retrieve all registered models for inventory display")
    @ApiResponse(responseCode = "200", description = "Successfully retrieved all models")
    public ResponseEntity<List<ModelResponse>> getAllModels() {
        List<ModelResponse> models = modelService.getAllModels();
        return ResponseEntity.ok(models);
    }
    
    @GetMapping("/{id}")
    @Operation(summary = "Get model by ID", description = "Retrieve a specific model by its unique ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Model found"),
        @ApiResponse(responseCode = "404", description = "Model not found")
    })
    public ResponseEntity<ModelResponse> getModelById(@PathVariable Long id) {
        try {
            ModelResponse model = modelService.getModelById(id);
            return ResponseEntity.ok(model);
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }
    
    @GetMapping("/enums")
    @Operation(summary = "Get enum values", description = "Get all possible values for dropdown fields")
    @ApiResponse(responseCode = "200", description = "Successfully retrieved enum values")
    public ResponseEntity<Map<String, List<Map<String, String>>>> getEnumValues() {
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
        return ResponseEntity.ok(enums);
    }
}

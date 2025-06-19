package com.mrm.modelregistry.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.mrm.modelregistry.dto.ModelRequest;
import com.mrm.modelregistry.dto.ModelResponse;
import com.mrm.modelregistry.entity.Model;
import com.mrm.modelregistry.service.ModelService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(ModelController.class)
class ModelControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private ModelService modelService;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void registerModel_ValidRequest_ReturnsCreated() throws Exception {
        ModelRequest request = new ModelRequest(
            "Test Model",
            "v1.0",
            "Test Sponsor",
            Model.BusinessLine.RETAIL_BANKING,
            Model.ModelType.CREDIT_RISK,
            Model.RiskRating.MEDIUM,
            Model.Status.IN_DEVELOPMENT
        );

        ModelResponse response = new ModelResponse();
        response.setId(1L);
        response.setModelName("Test Model");
        response.setModelVersion("v1.0");
        response.setModelSponsor("Test Sponsor");
        response.setBusinessLine(Model.BusinessLine.RETAIL_BANKING);
        response.setModelType(Model.ModelType.CREDIT_RISK);
        response.setRiskRating(Model.RiskRating.MEDIUM);
        response.setStatus(Model.Status.IN_DEVELOPMENT);
        response.setCreatedAt(LocalDateTime.now());
        response.setUpdatedAt(LocalDateTime.now());

        when(modelService.registerModel(any(ModelRequest.class))).thenReturn(response);

        mockMvc.perform(post("/api/models")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1L))
                .andExpect(jsonPath("$.modelName").value("Test Model"))
                .andExpect(jsonPath("$.modelVersion").value("v1.0"))
                .andExpect(jsonPath("$.modelSponsor").value("Test Sponsor"));
    }

    @Test
    void registerModel_InvalidRequest_ReturnsBadRequest() throws Exception {
        ModelRequest request = new ModelRequest();

        mockMvc.perform(post("/api/models")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest());
    }

    @Test
    void getAllModels_ReturnsModelList() throws Exception {
        ModelResponse response1 = new ModelResponse();
        response1.setId(1L);
        response1.setModelName("Model 1");
        response1.setModelVersion("v1.0");

        ModelResponse response2 = new ModelResponse();
        response2.setId(2L);
        response2.setModelName("Model 2");
        response2.setModelVersion("v2.0");

        List<ModelResponse> models = Arrays.asList(response1, response2);

        when(modelService.getAllModels()).thenReturn(models);

        mockMvc.perform(get("/api/models"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(2))
                .andExpect(jsonPath("$[0].id").value(1L))
                .andExpect(jsonPath("$[0].modelName").value("Model 1"))
                .andExpect(jsonPath("$[1].id").value(2L))
                .andExpect(jsonPath("$[1].modelName").value("Model 2"));
    }

    @Test
    void getModelById_ExistingId_ReturnsModel() throws Exception {
        ModelResponse response = new ModelResponse();
        response.setId(1L);
        response.setModelName("Test Model");
        response.setModelVersion("v1.0");

        when(modelService.getModelById(1L)).thenReturn(response);

        mockMvc.perform(get("/api/models/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1L))
                .andExpect(jsonPath("$.modelName").value("Test Model"))
                .andExpect(jsonPath("$.modelVersion").value("v1.0"));
    }

    @Test
    void getModelById_NonExistingId_ReturnsNotFound() throws Exception {
        when(modelService.getModelById(999L)).thenThrow(new RuntimeException("Model not found with id: 999"));

        mockMvc.perform(get("/api/models/999"))
                .andExpect(status().isNotFound());
    }

    @Test
    void getEnumValues_ReturnsAllEnums() throws Exception {
        mockMvc.perform(get("/api/models/enums"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.businessLines").exists())
                .andExpect(jsonPath("$.modelTypes").exists())
                .andExpect(jsonPath("$.riskRatings").exists())
                .andExpect(jsonPath("$.statuses").exists())
                .andExpect(jsonPath("$.businessLines.length()").value(4))
                .andExpect(jsonPath("$.modelTypes.length()").value(6))
                .andExpect(jsonPath("$.riskRatings.length()").value(3))
                .andExpect(jsonPath("$.statuses.length()").value(4));
    }
}

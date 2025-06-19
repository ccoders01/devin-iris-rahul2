package com.mrm.modelregistry.service;

import com.mrm.modelregistry.dto.ModelRequest;
import com.mrm.modelregistry.dto.ModelResponse;
import com.mrm.modelregistry.entity.Model;
import com.mrm.modelregistry.repository.ModelRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class ModelServiceTest {

    @Mock
    private ModelRepository modelRepository;

    @InjectMocks
    private ModelService modelService;

    @Test
    void registerModel_ValidRequest_ReturnsModelResponse() {
        ModelRequest request = new ModelRequest(
            "Test Model",
            "v1.0",
            "Test Sponsor",
            Model.BusinessLine.RETAIL_BANKING,
            Model.ModelType.CREDIT_RISK,
            Model.RiskRating.MEDIUM,
            Model.Status.IN_DEVELOPMENT
        );

        Model savedModel = new Model(
            "Test Model",
            "v1.0",
            "Test Sponsor",
            Model.BusinessLine.RETAIL_BANKING,
            Model.ModelType.CREDIT_RISK,
            Model.RiskRating.MEDIUM,
            Model.Status.IN_DEVELOPMENT
        );
        savedModel.setId(1L);
        savedModel.setCreatedAt(LocalDateTime.now());
        savedModel.setUpdatedAt(LocalDateTime.now());

        when(modelRepository.save(any(Model.class))).thenReturn(savedModel);

        ModelResponse response = modelService.registerModel(request);

        assertNotNull(response);
        assertEquals(1L, response.getId());
        assertEquals("Test Model", response.getModelName());
        assertEquals("v1.0", response.getModelVersion());
        assertEquals("Test Sponsor", response.getModelSponsor());
        assertEquals(Model.BusinessLine.RETAIL_BANKING, response.getBusinessLine());
        assertEquals(Model.ModelType.CREDIT_RISK, response.getModelType());
        assertEquals(Model.RiskRating.MEDIUM, response.getRiskRating());
        assertEquals(Model.Status.IN_DEVELOPMENT, response.getStatus());

        verify(modelRepository, times(1)).save(any(Model.class));
    }

    @Test
    void getAllModels_ReturnsModelResponseList() {
        Model model1 = new Model(
            "Model 1",
            "v1.0",
            "Sponsor 1",
            Model.BusinessLine.RETAIL_BANKING,
            Model.ModelType.CREDIT_RISK,
            Model.RiskRating.HIGH,
            Model.Status.PRODUCTION
        );
        model1.setId(1L);

        Model model2 = new Model(
            "Model 2",
            "v2.0",
            "Sponsor 2",
            Model.BusinessLine.INVESTMENT_BANKING,
            Model.ModelType.MARKET_RISK,
            Model.RiskRating.LOW,
            Model.Status.VALIDATED
        );
        model2.setId(2L);

        List<Model> models = Arrays.asList(model1, model2);

        when(modelRepository.findAll()).thenReturn(models);

        List<ModelResponse> responses = modelService.getAllModels();

        assertNotNull(responses);
        assertEquals(2, responses.size());
        assertEquals("Model 1", responses.get(0).getModelName());
        assertEquals("Model 2", responses.get(1).getModelName());

        verify(modelRepository, times(1)).findAll();
    }

    @Test
    void getModelById_ExistingId_ReturnsModelResponse() {
        Model model = new Model(
            "Test Model",
            "v1.0",
            "Test Sponsor",
            Model.BusinessLine.RETAIL_BANKING,
            Model.ModelType.CREDIT_RISK,
            Model.RiskRating.MEDIUM,
            Model.Status.IN_DEVELOPMENT
        );
        model.setId(1L);

        when(modelRepository.findById(1L)).thenReturn(Optional.of(model));

        ModelResponse response = modelService.getModelById(1L);

        assertNotNull(response);
        assertEquals(1L, response.getId());
        assertEquals("Test Model", response.getModelName());

        verify(modelRepository, times(1)).findById(1L);
    }

    @Test
    void getModelById_NonExistingId_ThrowsException() {
        when(modelRepository.findById(999L)).thenReturn(Optional.empty());

        RuntimeException exception = assertThrows(RuntimeException.class, () -> {
            modelService.getModelById(999L);
        });

        assertEquals("Model not found with id: 999", exception.getMessage());
        verify(modelRepository, times(1)).findById(999L);
    }
}
